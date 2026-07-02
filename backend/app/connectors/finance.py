"""Financial data connector — parses bank-statement CSVs into normalized
transactions, categorizes spending, and computes summary insights
(category totals, recurring subscriptions, monthly cash flow + forecast).

Mock-first: no bank API needed. Upload any CSV with date/description and
either debit/credit columns or a single signed amount column, or seed the
bundled demo statement (backend/mock_data/bank_statement.csv).
"""

import csv
import hashlib
import io
import re
from collections import defaultdict
from datetime import datetime

# Ordered: first match wins, so specific merchants come before generic ones
# (e.g. "uber eats" must resolve to food & drink, not transport).
CATEGORY_RULES = [
    ("salary", ["payroll", "salary", "stipend"]),
    ("rent", ["rent", "apartments", "landlord"]),
    ("groceries", ["whole foods", "trader joe", "safeway", "grocery", "supermarket"]),
    ("food & drink", ["uber eats", "doordash", "swiggy", "zomato", "blue bottle",
                      "starbucks", "coffee", "restaurant", "cafe"]),
    ("transport", ["uber", "lyft", "ola", "shell", "chevron", "clipper", "metro", "fuel"]),
    ("subscriptions", ["netflix", "spotify", "notion", "icloud", "openai", "chatgpt",
                       "youtube premium", "prime video", "subscr"]),
    ("utilities", ["pg&e", "pge", "verizon", "comcast", "at&t", "jio", "airtel",
                   "electricity", "water bill", "internet", "broadband", "utilities"]),
    ("health", ["equinox", "gym", "fitness", "pharmacy", "cvs", "walgreens",
                "therapy", "clinic", "hospital"]),
    ("shopping", ["amazon", "flipkart", "target", "best buy", "apple store", "myntra"]),
    ("travel", ["united airlines", "delta", "indigo", "airbnb", "hotel", "airlines", "makemytrip"]),
    ("transfer", ["zelle", "venmo", "upi", "imps", "neft", "wire", "transfer"]),
]

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%d %b %Y", "%b %d, %Y"]

_COLUMN_ALIASES = {
    "date": {"date", "transaction date", "txn date", "value date", "posted date"},
    "description": {"description", "narration", "details", "particulars", "memo", "payee"},
    "debit": {"debit", "withdrawal", "withdrawal amt", "debit amount"},
    "credit": {"credit", "deposit", "deposit amt", "credit amount"},
    "amount": {"amount", "transaction amount"},
}


def categorize(description: str, kind: str = "debit") -> str:
    d = description.lower()
    for category, keywords in CATEGORY_RULES:
        if any(k in d for k in keywords):
            return category
    return "income" if kind == "credit" else "other"


def _parse_date(raw: str) -> str | None:
    raw = (raw or "").strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _clean_number(raw: str) -> float | None:
    raw = (raw or "").strip().replace(",", "").replace("$", "").replace("₹", "")
    if not raw:
        return None
    negative = raw.startswith("(") and raw.endswith(")")
    if negative:
        raw = raw[1:-1]
    try:
        value = float(raw)
    except ValueError:
        return None
    return -value if negative else value


def parse_statement_csv(text: str) -> list[dict]:
    """Parse a bank-statement CSV into normalized transaction dicts.

    Supports separate debit/credit columns, or a single amount column where
    negatives are spending and positives are income.
    """
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("Empty CSV")

    cols: dict[str, str] = {}
    for field in reader.fieldnames:
        key = (field or "").strip().lower()
        for canon, aliases in _COLUMN_ALIASES.items():
            if key in aliases and canon not in cols:
                cols[canon] = field
    if "date" not in cols or "description" not in cols:
        raise ValueError("CSV needs a date column and a description/narration column")
    if not ({"debit", "credit", "amount"} & cols.keys()):
        raise ValueError("CSV needs debit/credit columns or an amount column")

    txns = []
    seen: dict[str, int] = defaultdict(int)  # occurrence counter → ids stable across re-uploads
    for row in reader:
        date = _parse_date(row.get(cols["date"], ""))
        desc = (row.get(cols["description"]) or "").strip()
        if not date or not desc:
            continue

        amount, kind = None, None
        debit = _clean_number(row.get(cols["debit"], "")) if "debit" in cols else None
        credit = _clean_number(row.get(cols["credit"], "")) if "credit" in cols else None
        if debit:
            amount, kind = abs(debit), "debit"
        elif credit:
            amount, kind = abs(credit), "credit"
        elif "amount" in cols:
            signed = _clean_number(row.get(cols["amount"], ""))
            if signed:
                amount, kind = abs(signed), ("debit" if signed < 0 else "credit")
        if not amount:
            continue

        key = f"{date}|{desc.lower()}|{amount:.2f}|{kind}"
        seen[key] += 1
        txns.append({
            "id": "txn-" + hashlib.md5(f"{key}|{seen[key]}".encode()).hexdigest()[:12],
            "date": date,
            "description": desc,
            "amount": round(amount, 2),
            "type": kind,
            "category": categorize(desc, kind),
        })
    return txns


def _normalize_merchant(description: str) -> str:
    # "WHOLE FOODS MARKET #1234" and "#5678" are the same merchant.
    return re.sub(r"\s+", " ", re.sub(r"[#*\d]+", " ", description.lower())).strip()


def detect_subscriptions(txns: list[dict]) -> list[dict]:
    """Recurring debits: same merchant, near-identical amount, charged
    roughly once a month across at least two months."""
    groups: dict[str, list[dict]] = defaultdict(list)
    for t in txns:
        if t["type"] == "debit" and t["category"] not in ("rent", "salary", "income", "transfer"):
            groups[_normalize_merchant(t["description"])].append(t)

    all_months = {t["date"][:7] for t in txns}
    subs = []
    for merchant, items in groups.items():
        months = {t["date"][:7] for t in items}
        amounts = [t["amount"] for t in items]
        if (len(months) >= 2
                and len(items) <= len(all_months) + 1  # ~once a month, not habitual spending
                and max(amounts) - min(amounts) <= 0.05):  # fixed price, unlike ad-hoc orders
            monthly = round(sum(amounts) / len(amounts), 2)
            subs.append({
                "merchant": merchant,
                "monthly_cost": monthly,
                "annual_cost": round(monthly * 12, 2),
                "months_seen": len(months),
                "category": items[0]["category"],
            })
    subs.sort(key=lambda s: s["monthly_cost"], reverse=True)
    return subs


def summarize(txns: list[dict]) -> dict:
    total_in = round(sum(t["amount"] for t in txns if t["type"] == "credit"), 2)
    total_out = round(sum(t["amount"] for t in txns if t["type"] == "debit"), 2)

    by_category: dict[str, float] = defaultdict(float)
    for t in txns:
        if t["type"] == "debit":
            by_category[t["category"]] += t["amount"]

    monthly: dict[str, dict] = defaultdict(lambda: {"in": 0.0, "out": 0.0})
    for t in txns:
        m = monthly[t["date"][:7]]
        m["in" if t["type"] == "credit" else "out"] += t["amount"]
    months = [
        {"month": k, "in": round(v["in"], 2), "out": round(v["out"], 2),
         "net": round(v["in"] - v["out"], 2)}
        for k, v in sorted(monthly.items())
    ]

    subs = detect_subscriptions(txns)
    forecast_net = round(sum(m["net"] for m in months) / len(months), 2) if months else 0.0

    return {
        "transactions": len(txns),
        "total_in": total_in,
        "total_out": total_out,
        "net": round(total_in - total_out, 2),
        "by_category": [
            {"category": c, "total": round(v, 2)}
            for c, v in sorted(by_category.items(), key=lambda x: x[1], reverse=True)
        ],
        "monthly": months,
        "subscriptions": {
            "items": subs,
            "monthly_cost": round(sum(s["monthly_cost"] for s in subs), 2),
            "annual_cost": round(sum(s["annual_cost"] for s in subs), 2),
        },
        "forecast": {"next_month_net": forecast_net},
    }

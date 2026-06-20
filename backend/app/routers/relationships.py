import json
import re
from collections import defaultdict
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.connectors import chroma, llm

router = APIRouter()

CACHE = Path("relationships.json")

SYSTEM = (
    "You characterise the people and organizations in someone's inbox. For "
    "each contact given (with the subjects they've sent), classify the kind of "
    "relationship and write one perceptive sentence about its nature. "
    'Respond ONLY with strict JSON: {"relationships": [{"name": "exact name '
    'given", "kind": "1-2 word label e.g. Recruiter, Service, Newsletter, '
    'Friend, Institution", "note": "one sentence"}]}. '
    "No markdown, no text outside the JSON."
)


def _sender_name(frm: str) -> str:
    m = re.match(r'^\s*"?([^"<]+?)"?\s*<', frm)
    return (m.group(1) if m else frm).strip() or frm


def _extract_json(s: str) -> dict:
    s = re.sub(r"^```(?:json)?|```$", "", s.strip(), flags=re.MULTILINE).strip()
    a, b = s.find("{"), s.rfind("}")
    if a != -1 and b != -1:
        s = s[a : b + 1]
    return json.loads(s)


@router.get("/relationships")
def get_relationships():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {"generated": False, "relationships": []}


@router.post("/relationships/build")
def build_relationships():
    emails = chroma.sample(limit=200)
    if not emails:
        raise HTTPException(status_code=400, detail="Archive is empty — sync first.")

    grouped: dict[str, list[str]] = defaultdict(list)
    for e in emails:
        grouped[_sender_name(e["from"])].append(e["subject"])

    top = sorted(grouped.items(), key=lambda kv: len(kv[1]), reverse=True)[:10]
    counts = {name: len(subs) for name, subs in top}

    catalogue = "\n\n".join(
        f"{name} ({len(subs)} emails):\n" + "\n".join(f"  - {s}" for s in subs[:6])
        for name, subs in top
    )
    raw = llm.chat(
        [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Contacts:\n\n{catalogue}"},
        ],
        max_tokens=1400,
        temperature=0.5,
    )
    try:
        rels = _extract_json(raw).get("relationships", [])
    except (json.JSONDecodeError, ValueError):
        rels = [{"name": n, "kind": "Contact", "note": ""} for n in counts]

    for r in rels:
        r["count"] = counts.get(r.get("name", ""), 0)
    rels.sort(key=lambda r: r["count"], reverse=True)

    result = {"generated": True, "relationships": rels}
    CACHE.write_text(json.dumps(result), encoding="utf-8")
    return result

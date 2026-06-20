import json
import re
from pathlib import Path
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from app.connectors import chroma, llm

router = APIRouter()

CACHE = Path("ego_insights.json")

SYSTEM = (
    "You are Ego, the self-reflection layer of a personal archive. You speak "
    "directly TO the person whose archive this is, as a perceptive mirror — "
    'always second person ("you", "your"), never third person, never their '
    "name. Given a sample of their emails (senders + subjects), reflect their "
    "current focus, recurring themes, what's demanding their attention, and the "
    "overall texture of their inbox life. Be perceptive but grounded — only "
    "infer from what's present. "
    'Respond ONLY with strict JSON of this shape: '
    '{"summary": "2-3 sentence reflection addressed to you, in plain prose", '
    '"themes": [{"title": "short label", "detail": "one sentence addressed to you"}]}. '
    "Give 4-6 themes. No markdown, no text outside the JSON."
)


def _extract_json(s: str) -> dict:
    s = re.sub(r"^```(?:json)?|```$", "", s.strip(), flags=re.MULTILINE).strip()
    start, end = s.find("{"), s.rfind("}")
    if start != -1 and end != -1:
        s = s[start : end + 1]
    return json.loads(s)


@router.get("/ego/insights")
def ego_insights():
    if CACHE.exists():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {"generated": False}


@router.post("/ego/analyze")
def ego_analyze():
    emails = chroma.sample(limit=60)
    if not emails:
        raise HTTPException(status_code=400, detail="Archive is empty — sync first.")

    catalogue = "\n".join(
        f"- From {e['from']}: {e['subject']}" for e in emails
    )
    raw = llm.chat(
        [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Emails ({len(emails)}):\n{catalogue}"},
        ],
        max_tokens=1200,
        temperature=0.6,
    )

    try:
        parsed = _extract_json(raw)
    except (json.JSONDecodeError, ValueError):
        parsed = {"summary": raw, "themes": []}

    result = {
        "generated": True,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sample_size": len(emails),
        "summary": parsed.get("summary", ""),
        "themes": parsed.get("themes", []),
    }
    CACHE.write_text(json.dumps(result), encoding="utf-8")
    return result

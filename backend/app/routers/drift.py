import json
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.connectors import chroma, llm

router = APIRouter()

GOALS_FILE = Path("goals.json")

SYSTEM = (
    "You are Drift, the accountability layer of a personal archive. Given a "
    "person's stated goals and a sample of their recent email activity, judge "
    "how well their actual activity reflects each goal. Be honest, not "
    "flattering. For each goal pick a status of exactly 'on-track', 'drifting', "
    "or 'stalled', and give one grounded sentence of evidence. "
    'Respond ONLY with strict JSON: {"alignment": [{"goal": "...", '
    '"status": "on-track|drifting|stalled", "note": "..."}]}. '
    "No markdown, no text outside the JSON."
)


class Goals(BaseModel):
    goals: list[str]


def _extract_json(s: str) -> dict:
    s = re.sub(r"^```(?:json)?|```$", "", s.strip(), flags=re.MULTILINE).strip()
    start, end = s.find("{"), s.rfind("}")
    if start != -1 and end != -1:
        s = s[start : end + 1]
    return json.loads(s)


@router.get("/drift/goals")
def get_goals():
    if GOALS_FILE.exists():
        return json.loads(GOALS_FILE.read_text(encoding="utf-8"))
    return {"goals": []}


@router.put("/drift/goals")
def set_goals(body: Goals):
    cleaned = [g.strip() for g in body.goals if g.strip()]
    GOALS_FILE.write_text(json.dumps({"goals": cleaned}), encoding="utf-8")
    return {"goals": cleaned}


@router.post("/drift/check")
def drift_check():
    if not GOALS_FILE.exists():
        raise HTTPException(status_code=400, detail="Set some goals first.")
    goals = json.loads(GOALS_FILE.read_text(encoding="utf-8")).get("goals", [])
    if not goals:
        raise HTTPException(status_code=400, detail="Set some goals first.")

    emails = chroma.sample(limit=60)
    activity = "\n".join(f"- From {e['from']}: {e['subject']}" for e in emails)
    goal_list = "\n".join(f"- {g}" for g in goals)

    raw = llm.chat(
        [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Goals:\n{goal_list}\n\nRecent activity ({len(emails)} emails):\n{activity}",
            },
        ],
        max_tokens=1000,
        temperature=0.5,
    )
    try:
        parsed = _extract_json(raw)
        alignment = parsed.get("alignment", [])
    except (json.JSONDecodeError, ValueError):
        alignment = [{"goal": g, "status": "drifting", "note": raw[:200]} for g in goals]

    return {"alignment": alignment, "sample_size": len(emails)}

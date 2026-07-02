import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.connectors import chroma
from app.connectors import sentiment as sentiment_connector

router = APIRouter(prefix="/sentiment")

DEMO_FILE = Path(__file__).resolve().parents[2] / "mock_data" / "manglish_messages.json"


@router.post("/score")
def score(payload: dict):
    """Score one text: {"text": "..."} → score, mood, language, matched terms."""
    text = (payload or {}).get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Send {\"text\": \"...\"}")
    return sentiment_connector.score_text(text)


@router.get("/archive")
def archive(limit: int = 200):
    """Per-day sentiment over the email archive — emotion-timeline-shaped
    ({date, score, mood, count}), scored by the code-mixed engine instead
    of the LLM so Malayalam/Manglish text is read correctly."""
    emails = chroma.sample(limit=limit)
    if not emails:
        raise HTTPException(status_code=400, detail="Archive is empty — sync first.")
    days = sentiment_connector.score_days(emails)
    if not days:
        raise HTTPException(status_code=400, detail="No dated messages to score.")
    return {"generated": True, "engine": "code-mixed", "days": days}


@router.get("/demo")
def demo():
    """Score the bundled Manglish group-chat week — per-message and per-day."""
    data = json.loads(DEMO_FILE.read_text(encoding="utf-8"))
    messages = data["messages"]
    scored = [
        {**m, **sentiment_connector.score_text(m["text"])}
        for m in messages
    ]
    return {
        "messages": scored,
        "days": sentiment_connector.score_days(messages),
    }

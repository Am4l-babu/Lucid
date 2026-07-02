"""Malayalam / Manglish sentiment — code-mixed scoring for archive text.

Standard LLM sentiment misses romanized Malayalam ("Manglish") and cultural
idiom entirely — "adipoli" reads as noise, "pani kitti" reads neutral. This
module scores Malayalam script, Manglish, and mixed English text.

Dual-mode, same pattern as chroma.py / llm.py:
- If the `transformers` package is installed, an Indic sentiment model is
  used (set SENTIMENT_MODEL to a HuggingFace id, e.g. an ai4bharat or
  l3cube-pune Malayalam checkpoint). Loaded lazily on first call.
- Otherwise (this repo's default mock mode) a rule-based lexicon engine
  runs: no dependencies, instant, and good enough to demo the concept.

Output is timeline-compatible: score_days() returns the same
{date, score, mood, count} day records the emotion timeline renders.
"""
import importlib.util
import os
import re
from collections import defaultdict
from email.utils import parsedate_to_datetime

TRANSFORMER_AVAILABLE = importlib.util.find_spec("transformers") is not None
_PIPELINE = None

MALAYALAM_CHARS = re.compile(r"[ഀ-ൿ]")
_TOKEN = re.compile(r"[a-zഀ-ൿ]+")

# Weighted lexicon: Malayalam script + romanized Manglish + the English words
# that dominate Kerala code-mixed chat. Weights in [-1, 1].
LEXICON = {
    # --- positive: Malayalam script ---
    "അടിപൊളി": 1.0, "കിടു": 0.9, "കൊള്ളാം": 0.7, "സന്തോഷം": 0.9,
    "നല്ലത്": 0.7, "നന്നായി": 0.7, "സൂപ്പർ": 0.9, "ഇഷ്ടം": 0.7,
    "സ്നേഹം": 0.8, "സമാധാനം": 0.6, "രസം": 0.6, "ചിരി": 0.5,
    # --- positive: Manglish / code-mixed ---
    "adipoli": 1.0, "kidu": 0.9, "kidilan": 0.9, "kollam": 0.7,
    "poli": 0.8, "pwoli": 0.9, "santhosham": 0.9, "nannayi": 0.7,
    "nalla": 0.6, "ishtam": 0.7, "ishtamayi": 0.8, "sneham": 0.8,
    "rasam": 0.5, "chiri": 0.5, "sugham": 0.6, "sughamano": 0.3,
    "mass": 0.7, "thara": 0.5, "vere": 0.0, "level": 0.4,
    "super": 0.8, "great": 0.7, "happy": 0.7, "love": 0.7,
    "awesome": 0.8, "congrats": 0.8, "thanks": 0.5, "nandi": 0.5,
    # --- negative: Malayalam script ---
    "മോശം": -0.8, "കഷ്ടം": -0.7, "സങ്കടം": -0.8, "വിഷമം": -0.8,
    "ദേഷ്യം": -0.8, "പേടി": -0.7, "ബോറടി": -0.6, "വെറുപ്പ്": -0.9,
    "പണി": -0.6, "ചതി": -0.9, "കരച്ചിൽ": -0.8, "ക്ഷീണം": -0.5,
    # --- negative: Manglish / code-mixed ---
    "mosham": -0.8, "kashtam": -0.7, "sankadam": -0.8, "vishamam": -0.8,
    "deshyam": -0.8, "pedi": -0.7, "boradi": -0.6, "bore": -0.5,
    "veruppu": -0.9, "pani": -0.6, "chathi": -0.9, "karachil": -0.8,
    "ksheenam": -0.5, "thallu": -0.4, "waste": -0.7, "chatha": -0.7,
    "kolamayi": -0.8, "nashtam": -0.7, "tension": -0.6, "pressure": -0.5,
    "sad": -0.7, "angry": -0.7, "tired": -0.5, "stress": -0.6,
    "terrible": -0.8, "worst": -0.9, "problem": -0.5, "prashnam": -0.5,
}

# Standalone negators flip the nearest scored word ("nalla alla"), and fused
# suffix negation flips the stem ("ishtamalla", "sughamilla").
NEGATORS = {"alla", "illa", "അല്ല", "ഇല്ല", "not", "no", "never", "illatha"}
NEGATION_SUFFIXES = ("ayilla", "amilla", "illa", "alla")

# Multipliers applied to the following sentiment word ("valare mosham").
INTENSIFIERS = {
    "valare": 1.5, "orupadu": 1.5, "othiri": 1.5, "nalloru": 1.3,
    "full": 1.3, "very": 1.4, "so": 1.2, "totally": 1.4,
    "വളരെ": 1.5, "ഒരുപാട്": 1.5, "ഒത്തിരി": 1.5,
}

# Manglish function words — used only for language detection, not scoring.
MANGLISH_MARKERS = {
    "aanu", "aano", "alle", "allo", "undu", "illa", "njan", "ente", "ninte",
    "enthu", "entha", "engane", "eppo", "evide", "cheyyam", "cheythu",
    "mathi", "venam", "vende", "machane", "macha", "chetta", "chechi",
    "ketto", "aayi", "onnum", "kure", "ippo", "pinne", "athu", "ithu",
}


def detect_language(text: str) -> str:
    """'ml' (Malayalam script), 'manglish' (romanized), or 'en'."""
    if MALAYALAM_CHARS.search(text):
        return "ml"
    tokens = set(_TOKEN.findall(text.lower()))
    markers = tokens & (MANGLISH_MARKERS | {w for w in LEXICON if not MALAYALAM_CHARS.search(w)})
    manglish_only = markers - {
        "super", "great", "happy", "love", "awesome", "congrats", "thanks",
        "mass", "level", "bore", "waste", "tension", "pressure", "sad",
        "angry", "tired", "stress", "terrible", "worst", "problem",
        "not", "no", "never", "full", "very", "so", "totally",
    }
    return "manglish" if manglish_only else "en"


def _rule_score(text: str) -> tuple[float, list[str]]:
    tokens = _TOKEN.findall(text.lower())
    hits: list[tuple[float, str]] = []
    multiplier = 1.0
    for tok in tokens:
        if tok in INTENSIFIERS:
            multiplier = INTENSIFIERS[tok]
            continue
        if tok in NEGATORS:
            if hits:  # "nalla alla" — flip the word just scored
                w, t = hits[-1]
                hits[-1] = (-w, f"{t} +neg")
            multiplier = 1.0
            continue
        weight = LEXICON.get(tok)
        matched = tok
        if weight is None:
            # fused negation: "ishtamalla" → flip "ishtam"
            for suffix in NEGATION_SUFFIXES:
                stem = tok.removesuffix(suffix)
                if stem != tok and stem in LEXICON:
                    weight, matched = -LEXICON[stem], f"{stem}+{suffix}"
                    break
        if weight is not None:
            hits.append((weight * multiplier, matched))
            multiplier = 1.0

    if not hits:
        return 0.0, []
    score = sum(w for w, _ in hits) / len(hits)
    return max(-1.0, min(1.0, round(score, 3))), [t for _, t in hits]


def _transformer_score(text: str) -> float | None:
    """Indic-model path; any failure falls back to rules."""
    global _PIPELINE
    try:
        if _PIPELINE is None:
            from transformers import pipeline
            _PIPELINE = pipeline(
                "sentiment-analysis",
                model=os.getenv("SENTIMENT_MODEL", "l3cube-pune/malayalam-sentiment-roberta"),
            )
        result = _PIPELINE(text[:512])[0]
        signed = {"positive": 1, "negative": -1}.get(result["label"].lower(), 0)
        return round(signed * float(result["score"]), 3)
    except Exception:
        return None


def _mood(score: float) -> str:
    if score >= 0.5:
        return "adipoli"
    if score >= 0.15:
        return "kollam"
    if score > -0.15:
        return "neutral"
    if score > -0.5:
        return "mosham"
    return "kashtam"


def score_text(text: str) -> dict:
    """Score one message: {score, mood, language, engine, matched}."""
    text = text or ""
    language = detect_language(text)
    engine = "rules"
    score, matched = _rule_score(text)
    if TRANSFORMER_AVAILABLE:
        t_score = _transformer_score(text)
        if t_score is not None:
            score, engine = t_score, "transformer"
    return {
        "score": score,
        "mood": _mood(score),
        "language": language,
        "engine": engine,
        "matched": matched,
    }


def _day(date_str: str) -> str | None:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(date_str)[:10]):
        return str(date_str)[:10]
    try:
        return parsedate_to_datetime(date_str).date().isoformat()
    except (TypeError, ValueError):
        return None


def score_days(messages: list[dict]) -> list[dict]:
    """Aggregate per-day scores over dated messages ({text, date}).
    Returns emotion-timeline-shaped records: {date, score, mood, count}."""
    by_day: dict[str, list[float]] = defaultdict(list)
    for m in messages:
        day = _day(m.get("date", ""))
        text = m.get("text") or m.get("subject", "")
        if day and text:
            by_day[day].append(score_text(text)["score"])
    return [
        {
            "date": day,
            "score": round(sum(scores) / len(scores), 3),
            "mood": _mood(sum(scores) / len(scores)),
            "count": len(scores),
        }
        for day, scores in sorted(by_day.items())
    ]

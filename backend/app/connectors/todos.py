"""Shared todo list — editable from the Telegram bot, the REST API and the web app.

Items can carry a reminder (`remind_at`, ISO datetime) and delivery channels
(`notify_via`: telegram / whatsapp / email). A background scheduler in
reminders.py fires them; browser notifications are handled by the web page.
"""

import json
import threading
from datetime import datetime, timezone
from pathlib import Path

TODO_FILE = Path("todos.json")
_LOCK = threading.Lock()

# "browser" is fired by the /todos web page itself; the server scheduler
# only delivers the first three.
CHANNELS = ("telegram", "whatsapp", "email", "browser")


def _read() -> dict:
    if TODO_FILE.exists():
        try:
            return json.loads(TODO_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"next_id": 1, "items": []}


def _write(data: dict):
    TODO_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def all_todos() -> list[dict]:
    return _read()["items"]


def _validate_reminder(remind_at: str | None, notify_via: list[str] | None):
    if remind_at is not None:
        try:
            datetime.fromisoformat(remind_at)
        except ValueError:
            raise ValueError(f"remind_at is not an ISO datetime: {remind_at!r}")
    for ch in notify_via or []:
        if ch not in CHANNELS:
            raise ValueError(f"Unknown channel {ch!r} — use {', '.join(CHANNELS)}.")


def add(text: str, remind_at: str | None = None, notify_via: list[str] | None = None) -> dict:
    text = text.strip()
    if not text:
        raise ValueError("Todo text is empty.")
    _validate_reminder(remind_at, notify_via)
    with _LOCK:
        data = _read()
        item = {
            "id": data["next_id"],
            "text": text,
            "done": False,
            "created": datetime.now(timezone.utc).isoformat(),
            "remind_at": remind_at,
            "notify_via": notify_via or [],
            "reminded": False,
        }
        data["items"].append(item)
        data["next_id"] += 1
        _write(data)
    return item


# ── id-based ops (REST / web) ────────────────────────────────────────────────

def update(item_id: int, **fields) -> dict:
    """Update text/done/remind_at/notify_via on the item with this id."""
    _validate_reminder(fields.get("remind_at"), fields.get("notify_via"))
    if "text" in fields and not str(fields["text"]).strip():
        raise ValueError("Todo text is empty.")
    with _LOCK:
        data = _read()
        item = next((i for i in data["items"] if i["id"] == item_id), None)
        if item is None:
            raise ValueError(f"No todo with id {item_id}.")
        for key in ("text", "done", "remind_at", "notify_via"):
            if key in fields:
                item[key] = fields[key]
        if "remind_at" in fields:  # a re-scheduled reminder should fire again
            item["reminded"] = False
        _write(data)
    return item


def delete_by_id(item_id: int) -> dict:
    with _LOCK:
        data = _read()
        item = next((i for i in data["items"] if i["id"] == item_id), None)
        if item is None:
            raise ValueError(f"No todo with id {item_id}.")
        data["items"].remove(item)
        _write(data)
    return item


def mark_reminded(item_id: int):
    with _LOCK:
        data = _read()
        item = next((i for i in data["items"] if i["id"] == item_id), None)
        if item is not None:
            item["reminded"] = True
            _write(data)


def due_reminders() -> list[dict]:
    """Items whose reminder time has passed and hasn't fired yet."""
    now = datetime.now(timezone.utc)
    due = []
    for item in all_todos():
        if item.get("done") or item.get("reminded") or not item.get("remind_at"):
            continue
        try:
            when = datetime.fromisoformat(item["remind_at"])
        except ValueError:
            continue
        if when.tzinfo is None:  # naive timestamps are treated as local time
            when = when.astimezone()
        if when <= now:
            due.append(item)
    return due


# ── position-based ops (Telegram commands use list numbers) ──────────────────

def _id_at(number: int) -> int:
    items = all_todos()
    if not 1 <= number <= len(items):
        raise ValueError(f"No todo #{number} — the list has {len(items)} item(s).")
    return items[number - 1]["id"]


def set_done(number: int, done: bool = True) -> dict:
    return update(_id_at(number), done=done)


def edit(number: int, text: str) -> dict:
    return update(_id_at(number), text=text.strip())


def delete(number: int) -> dict:
    return delete_by_id(_id_at(number))


def clear_done() -> int:
    with _LOCK:
        data = _read()
        before = len(data["items"])
        data["items"] = [i for i in data["items"] if not i["done"]]
        _write(data)
        return before - len(data["items"])


def render() -> str:
    """Plain-text listing for Telegram."""
    items = all_todos()
    if not items:
        return "Your todo list is empty. Add one with:\n/add buy milk"
    lines = ["📝 Your todos:"]
    for n, item in enumerate(items, 1):
        mark = "✅" if item["done"] else "◻️"
        extra = ""
        if item.get("remind_at") and not item.get("done"):
            extra = f"  ⏰ {item['remind_at'][:16].replace('T', ' ')}"
        lines.append(f"{n}. {mark} {item['text']}{extra}")
    lines.append("\n/add <text> · /done <n> · /undo <n> · /edit <n> <text> · /del <n> · /clear")
    return "\n".join(lines)

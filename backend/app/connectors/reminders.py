"""Reminder scheduler — checks the todo list and delivers due reminders.

Channels:
  telegram — bot message to your chat (needs Telegram connected)
  whatsapp — via the Node bridge at WA_SERVICE_URL (best-effort, skipped if down)
  email    — Gmail send-to-self (needs Google connected with the gmail.send scope)

Browser notifications are not sent from here — the /todos web page polls and
fires them itself. Each reminder fires once; re-scheduling re-arms it.
"""

import os
import threading
import time

import requests

CHECK_INTERVAL = 30  # seconds

_THREAD: threading.Thread | None = None
_STOP = threading.Event()


def _deliver(item: dict) -> list[str]:
    text = f"⏰ Reminder: {item['text']}"
    delivered = []

    for channel in item.get("notify_via", []):
        try:
            if channel == "telegram":
                from app.connectors import telegram
                telegram.send_message(text)
                delivered.append("telegram")
            elif channel == "whatsapp":
                base = os.getenv("WA_SERVICE_URL", "http://localhost:3001")
                r = requests.post(f"{base}/send", json={"text": text}, timeout=10)
                if r.ok:
                    delivered.append("whatsapp")
            elif channel == "email":
                from app.connectors import gmail
                gmail.send_to_self(f"Lucid reminder: {item['text']}", text)
                delivered.append("email")
        except Exception:
            pass  # one dead channel must not block the others
    return delivered


def _loop():
    from app.connectors import todos

    while not _STOP.is_set():
        try:
            for item in todos.due_reminders():
                _deliver(item)
                # Mark fired even if every channel failed — retrying forever
                # would spam the working channels once one recovers.
                todos.mark_reminded(item["id"])
        except Exception:
            pass
        _STOP.wait(CHECK_INTERVAL)


def start():
    global _THREAD
    if _THREAD and _THREAD.is_alive():
        return
    _STOP.clear()
    _THREAD = threading.Thread(target=_loop, name="reminder-scheduler", daemon=True)
    _THREAD.start()


def stop():
    _STOP.set()


def running() -> bool:
    return bool(_THREAD and _THREAD.is_alive())

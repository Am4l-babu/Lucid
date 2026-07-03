import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.readonly",
]
TOKENS_FILE = Path("tokens.json")

CLIENT_CONFIG = {
    "web": {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [os.environ["GOOGLE_REDIRECT_URI"]],
    }
}


def get_flow():
    return Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
    )


def get_auth_url() -> str:
    auth_url, _ = get_flow().authorization_url(prompt="consent", access_type="offline")
    return auth_url


def handle_callback(code: str):
    flow = get_flow()
    flow.fetch_token(code=code)
    _save_creds(flow.credentials)


def is_connected() -> bool:
    return TOKENS_FILE.exists()


def load_creds() -> Credentials | None:
    if not TOKENS_FILE.exists():
        return None
    data = json.loads(TOKENS_FILE.read_text())
    creds = Credentials(
        token=data["token"],
        refresh_token=data["refresh_token"],
        token_uri=data["token_uri"],
        client_id=data["client_id"],
        client_secret=data["client_secret"],
        scopes=data["scopes"],
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        _save_creds(creds)
    return creds


def fetch_emails(max_results: int = 100) -> list[dict]:
    creds = load_creds()
    service = build("gmail", "v1", credentials=creds)
    result = service.users().messages().list(userId="me", maxResults=max_results).execute()
    messages = result.get("messages", [])

    emails = []
    for msg in messages:
        full = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
        headers = {h["name"]: h["value"] for h in full["payload"]["headers"]}
        emails.append({
            "id": msg["id"],
            "subject": headers.get("Subject", ""),
            "from": headers.get("From", ""),
            "date": headers.get("Date", ""),
            "snippet": full.get("snippet", ""),
        })
    return emails


def send_to_self(subject: str, body: str):
    """Email the connected account's own address — used for todo reminders.
    Requires the gmail.send scope (reconnect Google if authorized before it
    was added)."""
    import base64
    from email.mime.text import MIMEText

    creds = load_creds()
    if creds is None:
        raise RuntimeError("Google not connected")
    service = build("gmail", "v1", credentials=creds)
    me = service.users().getProfile(userId="me").execute()["emailAddress"]
    msg = MIMEText(body)
    msg["to"] = me
    msg["from"] = me
    msg["subject"] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    service.users().messages().send(userId="me", body={"raw": raw}).execute()


def _save_creds(creds: Credentials):
    TOKENS_FILE.write_text(json.dumps({
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }))

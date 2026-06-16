import os
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

router = APIRouter()

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
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


def _get_flow():
    return Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=os.environ["GOOGLE_REDIRECT_URI"],
    )


def _load_creds():
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


def _save_creds(creds: Credentials):
    TOKENS_FILE.write_text(json.dumps({
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
    }))


@router.get("/auth/google")
def auth_google():
    flow = _get_flow()
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return RedirectResponse(auth_url)


@router.get("/auth/google/callback")
def auth_google_callback(code: str):
    flow = _get_flow()
    flow.fetch_token(code=code)
    _save_creds(flow.credentials)
    return {"status": "gmail connected"}


@router.get("/gmail/status")
def gmail_status():
    return {"connected": TOKENS_FILE.exists()}


@router.get("/gmail/sync")
def gmail_sync(max_results: int = 100):
    creds = _load_creds()
    if not creds:
        raise HTTPException(status_code=401, detail="Gmail not connected")

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

    return {"count": len(emails), "emails": emails}

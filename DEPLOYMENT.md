# Lucid — Deployment

Split deploy: **frontend on Vercel (free), backend on Azure (B1s)**. Chosen so the
₹9,569 Azure credit lasts past April and the frontend stays fast/global.

---

## Frontend → Vercel (free)

1. Push the repo to GitHub (done).
2. On Vercel: **New Project** → import the repo → set **Root Directory** to `frontend`.
3. Add an env var:
   - `NEXT_PUBLIC_API_URL` = `https://<your-azure-backend-url>`
4. Deploy. Vercel auto-builds on every push to the branch you select.

No Dockerfile needed — Vercel detects Next.js.

---

## Backend → Azure (B1s VM)

The backend is plain FastAPI + a local ChromaDB folder. Simplest reliable path is a
small Linux VM.

1. Create a **B1s** Ubuntu VM (~$8/mo; fits the credit for a year). Open ports 22 and 443 (or 8000 for a quick start).
2. SSH in, install Python 3.11 and the deps:
   ```bash
   sudo apt update && sudo apt install -y python3.11 python3.11-venv git
   git clone <repo> && cd lucid/backend
   python3.11 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Create `.env` on the server (never committed):
   ```
   ALLOWED_ORIGINS=https://<your-vercel-app>.vercel.app
   FRONTEND_URL=https://<your-vercel-app>.vercel.app
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   GOOGLE_REDIRECT_URI=https://<your-backend-domain>/auth/google/callback
   NVIDIA_API_KEY=...
   ```
4. Run it (behind a process manager so it survives reboots):
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   For production, put it behind **Caddy** (auto-HTTPS in ~3 lines) and run uvicorn via `systemd`.

### Two things that MUST change for production

- **Google OAuth needs HTTPS.** Add the new `https://<backend>/auth/google/callback`
  to the GCP OAuth client's authorized redirect URIs, and update `GOOGLE_REDIRECT_URI`.
- **CORS:** `ALLOWED_ORIGINS` must list the Vercel URL exactly.

---

## Memory note (B1s is 1GB RAM)

FastAPI + the MiniLM embedding model + ChromaDB fit on 1GB for a demo with curated
data. If it OOMs under real volume, either size up to B1ms (~$15/mo) or move embeddings
to **Qdrant Cloud** (free tier) so the VM only runs the API. See `PROGRESS.md` notes.

---

## Persisted state on the backend

These files live next to the backend and hold runtime state (all gitignored):
`tokens.json`, `chroma_data/`, `ego_insights.json`, `goals.json`, `graph.json`,
`relationships.json`, `timeline.json`, `briefing.json`. Back up `chroma_data/` if the
indexed archive matters; the rest regenerate.

# Lucid — Project Progress

> Single source of truth for what's being built, who's on it, and where things stand.
> Update this file directly on `main` before starting or finishing any component.

---

## Status Legend

| Symbol | Meaning |
|---|---|
| 📋 Todo | Not started |
| 🔄 Ongoing | Someone is actively working on this right now |
| 👀 In Review | PR open, waiting for merge |
| ✅ Done | Merged into `development` |
| 🚫 Blocked | Waiting on something else |

---

## Core Infrastructure

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| Project setup & folder structure | ✅ Done | Atul013 | feature/project-setup | Next.js + FastAPI scaffold |
| ChromaDB setup | 🔄 Ongoing | Atul013 | feature/chromadb-ingestion | Local vector DB |
| Ingestion pipeline (chunk + embed) | 🔄 Ongoing | Atul013 | feature/chromadb-ingestion | Depends on ChromaDB |
| Google OAuth | ✅ Done | Atul013 | feature/gmail-connector | Needed for Gmail, Keep, Calendar |

---

## Data Connectors

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| WhatsApp (`whatsapp-web.js`) | 📋 Todo | — | — | QR scan → real-time message stream (spare SIM for bot output) |
| Gmail | 🔄 Ongoing | Atul013 | feature/gmail-connector | Gmail API + Google OAuth |
| Telegram | 📋 Todo | — | — | Official Telegram API — dual role: data source + briefing output channel |
| Google Keep | 📋 Todo | — | — | Google API |
| Notion | 📋 Todo | — | — | Notion API |
| Discord | 📋 Todo | — | — | Discord bot API |
| Google Calendar | 📋 Todo | — | — | Google API |
| Local Notes (Obsidian etc.) | 📋 Todo | — | — | Watch local folder for .md files |

---

## AI Layers

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| Archive — semantic search | 📋 Todo | — | — | Query vector DB via LLM |
| Archive — chat UI | 📋 Todo | — | — | Depends on semantic search |
| Archive — voice interface | 📋 Todo | — | — | Whisper STT → piped into Archive query |
| Ego — analysis job | 📋 Todo | — | — | Scheduled LLM pattern finder |
| Ego — insights dashboard | 📋 Todo | — | — | Depends on analysis job |
| Ego — emotion timeline | 📋 Todo | — | — | Sentiment tracking across sources visualized over time |
| Drift — goals input | 📋 Todo | — | — | User sets goals once |
| Drift — deviation alerts | 📋 Todo | — | — | Depends on Ego + goals input |
| Relationship Intelligence | 📋 Todo | — | — | 4th AI layer — tracks how relationships evolve over time across sources |
| Morning Briefing | 📋 Todo | — | — | Telegram bot delivers daily AI-generated briefing from Archive + Ego + Drift |

---

## Frontend

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| Dashboard layout | 📋 Todo | — | — | Main shell, navigation |
| Connectors page | 📋 Todo | — | — | Connect/disconnect data sources |
| Archive chat page | 📋 Todo | — | — | |
| Ego insights page | 📋 Todo | — | — | |
| Drift goals page | 📋 Todo | — | — | |
| Relationship Intelligence page | 📋 Todo | — | — | |
| Emotion Timeline page | 📋 Todo | — | — | Sentiment graph over time |
| Visual Knowledge Graph | 📋 Todo | — | — | Animated constellation of topics/people/connections — expo showstopper |

---

## Final

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| UI polish | 📋 Todo | — | — | |
| Expo demo prep | 📋 Todo | — | — | Script + mock data |

---

## Activity Log

| Date | User | Action |
|---|---|---|
| 2026-06-15 | Atul013 | Project initialized |
| 2026-06-16 | Atul013 | Started project setup & folder structure |
| 2026-06-16 | Atul013 | Started Gmail connector |
| 2026-06-16 | Atul013 | Started ChromaDB setup + ingestion pipeline |


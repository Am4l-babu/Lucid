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
| Project setup & folder structure | 📋 Todo | — | — | Next.js + FastAPI scaffold |
| ChromaDB setup | 📋 Todo | — | — | Local vector DB |
| Ingestion pipeline (chunk + embed) | 📋 Todo | — | — | Depends on ChromaDB |
| Google OAuth | 📋 Todo | — | — | Needed for Gmail, Keep, Calendar |

---

## Data Connectors

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| WhatsApp (`whatsapp-web.js`) | 📋 Todo | — | — | QR scan → real-time message stream |
| Gmail | 📋 Todo | — | — | Gmail API + Google OAuth |
| Telegram | 📋 Todo | — | — | Official Telegram API |
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
| Ego — analysis job | 📋 Todo | — | — | Scheduled LLM pattern finder |
| Ego — insights dashboard | 📋 Todo | — | — | Depends on analysis job |
| Drift — goals input | 📋 Todo | — | — | User sets goals once |
| Drift — deviation alerts | 📋 Todo | — | — | Depends on Ego + goals input |

---

## Frontend

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| Dashboard layout | 📋 Todo | — | — | Main shell, navigation |
| Connectors page | 📋 Todo | — | — | Connect/disconnect data sources |
| Archive chat page | 📋 Todo | — | — | |
| Ego insights page | 📋 Todo | — | — | |
| Drift goals page | 📋 Todo | — | — | |

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


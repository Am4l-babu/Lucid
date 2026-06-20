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
| ChromaDB setup | ✅ Done | Atul013 | feature/chromadb-ingestion | Local vector DB (PersistentClient) |
| Ingestion pipeline (chunk + embed) | ✅ Done | Atul013 | feature/chromadb-ingestion | Embeds via MiniLM, stores in ChromaDB |
| Google OAuth | ✅ Done | Atul013 | feature/gmail-connector | Needed for Gmail, Keep, Calendar |
| Deployment — Vercel (FE) + Azure (BE) | 📋 Todo | — | — | Split deploy: FE free on Vercel, BE on Azure B1s. Budget: ₹9,569 Azure credit must last until Apr 2027. FE reads NEXT_PUBLIC_API_URL; BE CORS via ALLOWED_ORIGINS |
| Dockerization | 📋 Todo | — | — | Deferred. backend/Dockerfile + compose exist but unused for split deploy; revisit if BE needs containerizing on Azure |

---

## Data Connectors

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| WhatsApp (`whatsapp-web.js`) | 📋 Todo | — | — | QR scan → real-time message stream (spare SIM for bot output) |
| Gmail | ✅ Done | Atul013 | feature/gmail-connector | Gmail API + Google OAuth + sync |
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
| Archive — semantic search | 🔄 Ongoing | Atul013 | feature/archive-llm-chat | RAG: vector search + NVIDIA NIM (minimax-m3) |
| Archive — chat UI | 🔄 Ongoing | Atul013 | feature/archive-llm-chat | Ask-mode answers w/ sources |
| Archive — voice interface | 📋 Todo | — | — | Whisper STT → piped into Archive query |
| Ego — analysis job | 🔄 Ongoing | Atul013 | feature/ego-insights | On-demand LLM pattern finder over archive |
| Ego — insights dashboard | 🔄 Ongoing | Atul013 | feature/ego-insights | Renders Ego analysis output |
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
| Connectors page | 👀 In Review | Atul013 | feature/connectors-onboarding | Connect Gmail + sync flow (first-run onboarding) |
| Archive chat page | ✅ Done | Atul013 | feature/archive-search-ui | Editorial minimalist search UI over /gmail/search |
| Ego insights page | 🔄 Ongoing | Atul013 | feature/ego-insights | /ego route |
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
| 2026-06-20 | Atul013 | Decided split deploy (Vercel FE + Azure BE); dockerization deferred |
| 2026-06-20 | Atul013 | Started Connect Gmail + sync onboarding flow |
| 2026-06-20 | Atul013 | Started Archive LLM (RAG via NVIDIA NIM) + chat/ask UI |
| 2026-06-20 | Atul013 | Started Ego analysis job + insights page |


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
| WhatsApp (`whatsapp-web.js`) | 🔄 Ongoing | Atul013 | feature/whatsapp-connector | Node.js microservice bridge; spare SIM Business account set up |
| Gmail | ✅ Done | Atul013 | feature/gmail-connector | Gmail API + Google OAuth + sync |
| Telegram | 🔄 Ongoing | Atul013 | feature/telegram-connector | Official Telegram API — dual role: data source + briefing output channel |
| Financial data (mock CSV) | 👀 In Review | Am4l-babu | feature/financial-ingestion | Bank-statement CSV parser → categorize spending → ChromaDB (PR #23) |
| Health data (mock smartwatch JSON) | 👀 In Review | Am4l-babu | feature/health-ingestion | Sleep, HRV, steps → ChromaDB + sentiment correlation (PR #25) |
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
| Archive — voice interface | 🔄 Ongoing | Atul013 | feature/archive-voice | Browser-native speech → Archive query (no key) |
| Ego — analysis job | 🔄 Ongoing | Atul013 | feature/ego-insights | On-demand LLM pattern finder over archive |
| Ego — insights dashboard | 🔄 Ongoing | Atul013 | feature/ego-insights | Renders Ego analysis output |
| Ego — emotion timeline | 🔄 Ongoing | Atul013 | feature/emotion-timeline | LLM sentiment per day → SVG timeline |
| Drift — goals input | 🔄 Ongoing | Atul013 | feature/drift-goals | User sets goals once |
| Drift — deviation alerts | 🔄 Ongoing | Atul013 | feature/drift-goals | LLM aligns goals vs archive activity |
| Relationship Intelligence | 🔄 Ongoing | Atul013 | feature/relationship-intelligence | LLM over top senders → relationship notes |
| Morning Briefing | 🔄 Ongoing | Atul013 | feature/morning-briefing | LLM briefing (Archive+Ego+Drift) + Today view; Telegram delivery deferred (needs bot token) |

---

## Digital Twin Track

> Long-range phases from [ROADMAP.md](ROADMAP.md); working plan in [PLAN.md](PLAN.md). Software phases first — hardware waits.

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| Malayalam/Manglish sentiment | 🔄 Ongoing | Am4l-babu | feature/malayalam-sentiment | Indic-transformer sentiment over archive text; feeds emotion timeline |
| Digital Twin — simulation engine | 📋 Todo | Am4l-babu | — | simulate_workload(): goal-drift/stress probability from calendar + health history |
| Autonomous agent loop | 📋 Todo | — | — | LangChain tool-use: draft follow-ups, calendar optimization |
| SNN tripwire | 📋 Todo | — | — | LIF/Norse spiking net over temporal metadata; wakes LLM on anomaly |
| Edge deployment (Pi Zero 2 W) | 📋 Todo | — | — | FastAPI + ChromaDB on Pi, low-RAM tuning |
| ESP32 environment nodes | 📋 Todo | — | — | BME680 + mic dB via MQTT → productivity correlation |
| FOV camera + assistive interaction | 📋 Todo | — | — | MediaPipe posture/presence; faster-whisper offline STT; sign language |

---

## Frontend

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| UI Redesign — dark console theme | 🔄 Ongoing | ZayedBH | feature/ui-dark-console | Full dark redesign: WebGL shader hero, GSAP animations, Lenis scroll, 8-route landing |
| Dashboard layout | 🔄 Ongoing | Atul013 | feature/dashboard-layout | Shared nav across Archive · Ego · Drift |
| Connectors page | 👀 In Review | Atul013 | feature/connectors-onboarding | Connect Gmail + sync flow (first-run onboarding) |
| Archive chat page | ✅ Done | Atul013 | feature/archive-search-ui | Editorial minimalist search UI over /gmail/search |
| Ego insights page | 🔄 Ongoing | Atul013 | feature/ego-insights | /ego route |
| Drift goals page | 🔄 Ongoing | Atul013 | feature/drift-goals | /drift route |
| Relationship Intelligence page | 🔄 Ongoing | Atul013 | feature/relationship-intelligence | /relationships route |
| Emotion Timeline page | 🔄 Ongoing | Atul013 | feature/emotion-timeline | /timeline route |
| Visual Knowledge Graph | 🔄 Ongoing | Atul013 | feature/knowledge-graph | Animated force-directed constellation (canvas) |

---

## Final

| Component | Status | Assigned To | Branch | Notes |
|---|---|---|---|---|
| UI polish | 🔄 Ongoing | Atul013 | feature/ui-polish | Mobile-safe nav, consistency pass |
| Expo demo prep | 🔄 Ongoing | Atul013 | feature/expo-prep | Demo script + mock-data seed + deployment guide |

---

## Activity Log

| Date | User | Action |
|---|---|---|
| 2026-06-15 | Atul013 | Project initialized |
| 2026-06-16 | Atul013 | Started project setup & folder structure |
| 2026-06-16 | Atul013 | Started Gmail connector |
| 2026-06-16 | Atul013 | Started ChromaDB setup + ingestion pipeline |
| 2026-06-28 | Atul013 | Opened PR #22 (connectors page) → development |
| 2026-06-28 | Atul013 | Started Telegram connector |
| 2026-06-20 | Atul013 | Decided split deploy (Vercel FE + Azure BE); dockerization deferred |
| 2026-06-20 | Atul013 | UI polish — mobile-safe nav |
| 2026-06-20 | Atul013 | Started Connect Gmail + sync onboarding flow |
| 2026-06-20 | Atul013 | Started Archive LLM (RAG via NVIDIA NIM) + chat/ask UI |
| 2026-06-20 | Atul013 | Started Ego analysis job + insights page |
| 2026-06-20 | Atul013 | Started Drift goals input + alignment check |
| 2026-06-20 | Atul013 | Started Dashboard layout (shared nav) |
| 2026-06-20 | ZayedBH | Started UI redesign — dark console theme (feature/ui-dark-console) |
| 2026-06-20 | Atul013 | Batch: voice, knowledge graph, relationships, emotion timeline, briefing, expo prep |
| 2026-06-21 | Atul013 | Started WhatsApp connector (Node.js bridge, Business account on spare SIM) |
| 2026-07-02 | Am4l-babu | Started financial data connector (mock CSV ingestion) |
| 2026-07-02 | Am4l-babu | Opened PR #23 (financial ingestion) → development |
| 2026-07-02 | Am4l-babu | Added digital-twin roadmap: ROADMAP.md, PLAN.md + new planned components |
| 2026-07-02 | Am4l-babu | Started health data connector (mock smartwatch JSON) |
| 2026-07-02 | Am4l-babu | Opened PR #25 (health ingestion) → development |
| 2026-07-02 | Am4l-babu | Started Malayalam/Manglish sentiment module |


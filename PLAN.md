# Lucid — Working Plan (Am4l-babu's track)

> What's done, what's next, and where this could go. Vision and phase detail in
> [ROADMAP.md](ROADMAP.md); live team status in [PROGRESS.md](PROGRESS.md).
> Last updated: 2026-07-02

---

## ✅ Done

| When | What |
|---|---|
| 2026-07-02 | **Offline mock mode** committed to main: `chroma.py` falls back to a JSON store when chromadb can't compile (Windows, no C++ build tools); `llm.py` returns Maya-Chen-persona canned replies when `NVIDIA_API_KEY` is unset. App now runs fully out of the box |
| 2026-07-02 | **Financial data connector** — [PR #23](https://github.com/Atul013/Lucid/pull/23) to `development`. CSV parser (debit/credit or signed-amount formats), keyword categorizer, recurring-subscription detector ($315/mo found in demo data), monthly cash-flow summary + next-month forecast. Endpoints: `POST /finance/upload`, `POST /finance/seed`, `GET /finance/summary`, `GET /finance/search`. 3-month mock statement aligned with the expo persona |

Team foundation already in place (Atul013 & ZayedBH): FastAPI + Next.js scaffold, ChromaDB ingestion, Google OAuth, Gmail connector, Archive/Ego/Drift AI layers, dark-console UI — see PROGRESS.md.

## 🔜 Next up (Phase 1 remainder, in order)

1. **Health ingestion** (`feature/health-ingestion`) — mock smartwatch JSON (sleep stages, HRV, resting HR, steps) → `health` collection in ChromaDB + mock mode; `/health-data/seed`, `/health-data/summary` endpoints; correlation hook against email sentiment. Mirrors the finance connector's mock-first shape.
2. **Malayalam / Manglish sentiment** (`feature/malayalam-sentiment`) — Indic-transformer model (e.g. `ai4bharat/indic-bert` or `l3cube-pune/malayalam-sentiment`) with a lightweight rule-based Manglish fallback for mock mode; score archive text per message/day; feeds the emotion timeline.
3. **Google Calendar connector** (`feature/calendar-connector`) — OAuth already done; sync events into ChromaDB. This is the prerequisite for the Digital Twin's workload history.
4. **Phase 2 gate:** with finance + health + calendar + sentiment landed, build `simulate_workload()` (scikit-learn over calendar density × sleep/HRV) and the LangChain agent loop.

Every component follows the CLAUDE.md workflow: PROGRESS.md → feature branch → PR to `development`.

## 💡 Future suggestions & feature ideas

**Near-term, high value**
- **Budget alerts in Morning Briefing** — surface subscription waste and cash-flow forecast from `/finance/summary` in the existing briefing (cheap win, connectors already share ChromaDB).
- **Telegram briefing delivery** — Atul013's Telegram connector is dual-role; the briefing already exists, only the bot-token wiring is deferred.
- **Tests + CI** — the finance parser has clear input/output contracts; a pytest suite + GitHub Actions would protect all connectors as they multiply.
- **Unified `/ingest` metadata registry** — one place listing every collection (emails, transactions, health, events) with counts and last-sync, for the connectors page.

**Medium-term**
- **Cross-domain correlation engine** — the real differentiator: join health × finance × sentiment × calendar by date ("spending spikes follow low-sleep weeks").
- **On-device embeddings** — swap MiniLM in via `sentence-transformers` ONNX/quantized so mock mode gets true vector search (also the path to Pi deployment).
- **Data export / right-to-delete** — one endpoint that dumps or purges everything; personal data deserves it and it's an expo talking point.
- **Drift ↔ Twin merge** — Drift's goal-deviation alerts become the Twin's training signal; don't build them as silos.

**Long-term (Phases 3–4)**
- **SNN tripwire prototype in pure NumPy first** — a leaky integrate-and-fire layer over message-timestamp streams needs no new deps and proves the wake-the-LLM trigger before adopting Norse.
- **Privacy tiering for edge** — classify collections as cloud-ok vs. local-only, so the Pi Zero migration is a config change, not a rewrite.
- **Assistive mode as a first-class product** — offline Malayalam voice + sign-language interaction could stand alone; keep the STT interface decoupled from the twin.

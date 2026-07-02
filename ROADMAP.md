# Lucid — Digital Twin Roadmap

> The long-range vision: Lucid starts as a software-based personal intelligence
> aggregator and evolves into a hardware-backed, edge-computing **Omniscient
> Personal Digital Twin**. This file tracks the phases and the full idea backlog.
> Day-to-day status lives in [PROGRESS.md](PROGRESS.md); the working plan is in [PLAN.md](PLAN.md).

Rule of thumb: **do not jump to hardware until the software foundation is solid.**

---

## Phase 1 — Core Software & API Foundation (The Data Foundation)

*Goal: expand data ingestion and immediate utility using cloud APIs and mock-first pipelines.*

| # | Idea | Detail |
|---|---|---|
| 1.1 | **Financial insights** | Mock bank-statement CSV ingestion → categorize spending, detect subscription waste, forecast monthly cash flow. Later: Plaid / Razorpay APIs. ✅ *Shipped as PR #23* |
| 1.2 | **Health monitoring** | Mock smartwatch JSON (sleep, HRV, steps) → ChromaDB. Later: Apple Health / Google Fit APIs. Correlate sleep/HRV with communication sentiment |
| 1.3 | **Email & calendar** | Gmail sync (✅ done, team) + Google Calendar connector. Smart email assistant: thread summaries, priority scores (1–5), auto-drafted follow-up reminders |
| 1.4 | **Malayalam / Manglish sentiment** | Indic-transformer sentiment module — standard LLMs miss Malayalam sarcasm and cultural context. Insights like *"നിങ്ങൾ ഏറ്റവും productive സമയം രാവിലെ 9–11 ആണ്"* |
| 1.5 | **Personal life coach** | Analyze calendar + app usage to find peak productivity windows; block distracting apps inside them |
| 1.6 | **Team memory (enterprise mode)** | Multi-tenant vector DB indexing Slack / MS Teams / meeting transcripts as shared searchable knowledge |
| 1.7 | **Smart home integration** | Home Assistant API: trigger IoT routines (dim lights, phone DND) from detected stress level or calendar status |
| 1.8 | **Predictive analytics** | Time-series forecasting (Prophet / ARIMA) for future workload, stress peaks, goal-miss probability |

## Phase 2 — Predictive Digital Twin & Autonomous Agent (The Brain)

*Goal: shift from retrospective analysis to predictive simulation.*

| # | Idea | Detail |
|---|---|---|
| 2.1 | **Digital Twin simulation engine** | NumPy + scikit-learn (or Prophet) over historical calendar + health data. `simulate_workload(new_task)` → probability of goal-drift or stress: *"If I take this task, 80% chance I miss my gym goals next week"* |
| 2.2 | **Autonomous agent loop** | LangChain agent with tool use: auto-draft email follow-ups, suggest/reorder calendar blocks, auto-schedule meetings, draft routine tasks |
| 2.3 | **Cultural nuance training** | Deepen the Indic-model sentiment from 1.4 so insights are personal, not generic |

## Phase 3 — Neural Architecture Optimization (The Nervous System)

*Goal: computationally efficient, highly responsive monitoring.*

| # | Idea | Detail |
|---|---|---|
| 3.1 | **Event-driven SNN tripwire** | Spiking neural network (`Norse`, or a custom NumPy leaky integrate-and-fire model) ingesting temporal metadata: message timestamps, typing speed, frequency gaps. Cheap to run 24/7 |
| 3.2 | **Wake-the-LLM trigger** | When the SNN spikes on an anomaly (e.g. sudden late-night messaging density), a callback wakes the heavy LLM for deep semantic analysis — massive compute savings vs. always-on LLM |

## Phase 4 — Edge Hardware & Physical Context (The Physical Body)

*Goal: ultimate privacy and physical contextual awareness.*

| # | Idea | Detail |
|---|---|---|
| 4.1 | **Edge node (Raspberry Pi Zero 2 W)** | Deploy FastAPI + ChromaDB locally; low-RAM optimization. The memory bank never touches the cloud |
| 4.2 | **3D-printed enclosure** | Vented desk "Home Intelligence Hub" shell for the Pi |
| 4.3 | **ESP32 environment nodes** | MicroPython on ESP32 reading BME680 (temp/humidity/CO2) + mic decibels → MQTT → backend correlation: *"coding errors up 40% when CO2 > 1000 ppm"* |
| 4.4 | **FOV camera & physical context** | OpenCV + MediaPipe on a FOV camera: desk presence, posture/slouch detection |
| 4.5 | **Offline assistive interaction** | `faster-whisper` for local private voice-to-text; sign-language-to-speech models — talk to the twin with no internet |

---

## Stack notes

- Python 3.10, FastAPI backend, Next.js frontend, ChromaDB vector store (JSON mock fallback on machines without C++ build tools)
- LLM: NVIDIA NIM (minimax-m3) with a keyless mock mode for demos
- ML: NumPy (installed), scikit-learn / Prophet for forecasting, Norse for SNNs
- Hardware targets: Raspberry Pi Zero 2 W, ESP32 + BME680, FOV camera module

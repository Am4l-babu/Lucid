# Lucid — Expo Demo Script

A 4–5 minute walkthrough. The story: **one inbox, five kinds of intelligence.**

---

## Before the demo

1. Backend running with `NVIDIA_API_KEY` set, frontend on Vercel (or `localhost:3000`).
2. Seed the demo persona (Maya, an AI founder) so the story is crisp and reproducible:
   ```bash
   cd backend
   python seed_demo.py
   ```
3. Pre-warm the LLM caches so nothing is generated live on stage (optional but recommended):
   ```bash
   curl -X POST $API/ego/analyze
   curl -X POST $API/relationships/build
   curl -X POST $API/graph/build
   curl -X POST $API/ego/timeline/build
   curl -X POST $API/briefing/build
   ```
4. Set Drift goals once (so the briefing + drift check have something to align against):
   - On `/drift`, add: *"Close the seed round by July"* and *"Ship Lumen v1"*.

---

## The walkthrough

**1. Today (15s) — the hook.**
Open `/today`. Read two lines of the briefing aloud. "This is generated from her inbox this morning — it knows her raise is closing, that a customer is down, and that she keeps cancelling on her mom." Lead with the payoff.

**2. Archive (60s) — ask, don't search.**
Go to `/`. In **Ask** mode, type or *speak* (mic button): **"what's blocking the v1 launch?"** → grounded answer with sources. Then **"who have I been ignoring?"** → it surfaces the family + friend threads. Toggle to **Search** to show the semantic layer underneath.

**3. Ego (45s) — the mirror.**
`/ego` → the themes. "It read 24 emails and saw the shape of her life: fundraising, hiring, a launch crunch, and a personal life getting squeezed."

**4. Drift (45s) — the conscience.**
`/drift` → "Check my drift." Her goals vs her actual activity — honest verdicts with evidence.

**5. Graph (60s) — the showstopper.**
`/graph` → "Build constellation." Let it settle, then hover a node to light up its connections. "People and themes, and how they pull on each other."

**6. Timeline + People (30s) — the breadth.**
`/timeline` shows the emotional weather (the launch-crunch day dips). `/relationships` shows who matters and how often. Quick passes — these prove depth.

**Close:** "Every screen is the *same* data, asked a different question. Lucid is one place that actually understands your life — and it runs locally, on your machine."

---

## If something breaks

- **A page says "couldn't reach the backend":** the API is down or `NEXT_PUBLIC_API_URL` is wrong. Fall back to a screen recording.
- **An LLM call is slow on stage:** you pre-warmed the caches, so just refresh — it serves the cached result instantly.
- **Voice doesn't work:** it needs Chrome/Edge and mic permission. Type instead.

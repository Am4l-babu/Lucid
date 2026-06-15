# Lucid — AI-Powered Personal Intelligence System

> *You already know yourself. You just can't see it yet.*

Lucid is an AI agent that connects to your digital life — WhatsApp, Gmail, Telegram, Notion, Discord, Google Keep, and Calendar — and passively builds a living portrait of who you are. No journaling. No manual input. Just connect once and Lucid watches, learns, and reflects you back to yourself.

---

## The Problem

Your real personality is scattered across thousands of messages, emails, notes and calendar events you've already created. But there's no tool that pulls it all together and tells you the truth about yourself — your actual habits, real patterns, and whether your actions match your stated goals.

We think we know ourselves. We almost never do.

---

## What Lucid Does

Lucid is built around three layers that stack on top of each other:

### Archive
Query your own memory in plain English.
- *"What was I stressed about last month?"*
- *"When did I last talk to [person] about [topic]?"*
- *"What projects was I working on in May?"*

Your messages, emails and notes are indexed into a vector database. The AI searches them semantically and answers in context — like ChatGPT, but trained on you.

### Ego
Behavioral pattern recognition, fully autonomous.

Lucid runs a background analysis job periodically and surfaces patterns you'd never notice yourself:
- *"You abandon projects consistently on day 3-5."*
- *"You're 3x more agreeable in messages sent after 11pm."*
- *"You've mentioned wanting to learn design in 6 different conversations. Zero action taken."*

No input needed. It just shows up on your dashboard.

### Drift
Accountability without effort.

You state your goals once. Lucid compares Ego's findings against them and flags whenever your behavior is drifting away from what you said you wanted.

---

## Data Sources

| Source | Connection |
|---|---|
| WhatsApp | `whatsapp-web.js` — scan QR once, stays connected |
| Gmail | Gmail API + Google OAuth |
| Telegram | Official Telegram API |
| Google Keep | Google API |
| Notion | Notion API |
| Discord | Discord bot API |
| Google Calendar | Google API |
| Local Notes (Obsidian etc.) | Watch local folder |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + Tailwind CSS |
| Backend | Node.js + FastAPI (Python) |
| WhatsApp Bridge | `whatsapp-web.js` |
| Embeddings | OpenAI / Claude API |
| Vector Database | ChromaDB |
| LLM | Claude API (Anthropic) |
| Auth | Google OAuth 2.0 |

---

## Architecture

```
Data Sources (WhatsApp, Gmail, Telegram, Notion...)
        ↓
    Ingestion Layer
        ↓
  Chunk + Embed → Vector DB (ChromaDB)
        ↓
  ┌─────────────────────────────┐
  │         AI Layer            │
  │  Archive  │  Ego  │  Drift  │
  └─────────────────────────────┘
        ↓
    Web Dashboard (Next.js)
```

---

## Roadmap (14 Days)

| Days | Milestone |
|---|---|
| 1-2 | Project setup, WhatsApp integration via `whatsapp-web.js` |
| 3-4 | Ingestion pipeline — chunk, embed, store in ChromaDB |
| 5-6 | Archive — semantic search + chat UI |
| 7-8 | Gmail + Telegram connectors |
| 9-10 | Ego — scheduled analysis jobs + insights dashboard |
| 11-12 | Drift — goals input + deviation alerts |
| 13 | UI polish + additional connectors (Notion, Discord, Keep) |
| 14 | Final testing + expo prep |

---

## Getting Started

> Setup instructions coming soon as the project progresses.

---

## Team

Built during semester break for **Build-A-Project 14** by IEEE CS SBC ASIET.
Theme: *Technology for Real-World Impact*

---

*Lucid — because clarity about yourself is the most useful thing AI can give you.*

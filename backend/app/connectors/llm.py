import os
import json
import requests

# NVIDIA NIM — OpenAI-compatible chat completions.
NIM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = os.getenv("LLM_MODEL", "minimaxai/minimax-m3")


def chat(messages: list[dict], max_tokens: int = 1024, temperature: float = 0.4) -> str:
    key = os.getenv("NVIDIA_API_KEY")
    if not key:
        # Mock LLM mode: returns high-quality, persona-aligned responses matching
        # the seeded Maya Chen founder demo so the app runs fully out-of-the-box.
        sys_msg = next((m["content"] for m in messages if m["role"] == "system"), "")
        user_msg = next((m["content"] for m in messages if m["role"] == "user"), "")
        
        # 1. Ego insights
        if "Ego" in sys_msg:
            return json.dumps({
                "summary": "You are operating under intense launch-crunch and fundraising pressure. While you are close to wrapping up your $1.5M seed round with Priya Nair and Daniel Roth, your personal life (family and friends) is taking a back seat. There is a clear pattern of prioritizing product deployment over your personal health and relationships.",
                "themes": [
                    {"title": "Seed Raising", "detail": "You are actively negotiating with Priya Nair (Northstar) and Daniel Roth, managing investor decks and SAFE transfers."},
                    {"title": "Launch Crunch", "detail": "You and Nina Adler are working towards the Lumen v1 launch on Tuesday, resolving onboarding issues and billing webhooks."},
                    {"title": "Ops Escalations", "detail": "Carlos Mendez reported 500 server errors, and AWS billing alerts flag a 240% GPU bill surge."},
                    {"title": "Neglected Circles", "detail": "Your family (Grace Chen) and friends (Dev Patel) have reached out noting your weeks-long silence and cancellations."}
                ]
            }, indent=2)

        # 2. Drift check
        elif "Drift" in sys_msg:
            return json.dumps({
                "alignment": [
                    {
                        "goal": "Close the seed round by July",
                        "status": "on-track",
                        "note": "Term sheet of $1.5M received from Northstar VC (Priya Nair) and SAFE wire of $50k cleared from Aileen Park."
                    },
                    {
                        "goal": "Ship Lumen v1",
                        "status": "drifting",
                        "note": "Launch checklist has 6 items remaining, but recent API outages (500s from Carlos Mendez) and 240% AWS cost hikes are distracting the core team."
                    }
                ]
            }, indent=2)

        # 3. Morning Briefing
        elif "morning briefing" in sys_msg or "Lucid, writing a brief" in sys_msg:
            return (
                "Good morning, Maya. Priya Nair from Northstar VC sent over the term sheet for the $1.5M seed round, "
                "and Aileen Park's $50k SAFE wire has cleared. However, Carlos Mendez reported server 500 errors blocking "
                "their launch, and your AWS GPU bill is up 240%. On the personal front, Grace Chen sent a reminder that "
                "your mother's birthday dinner is this Sunday at 7 PM. You've canceled the last two family dinners; "
                "please make it a priority to attend. Work will still be there on Monday."
            )

        # 4. Knowledge Graph
        elif "knowledge graph" in sys_msg or "nodes" in sys_msg:
            return json.dumps({
                "nodes": [
                    {"id": "maya-chen", "label": "Maya Chen", "type": "person", "weight": 9},
                    {"id": "priya-nair", "label": "Priya Nair", "type": "person", "weight": 8},
                    {"id": "nina-adler", "label": "Nina Adler", "type": "person", "weight": 7},
                    {"id": "carlos-mendez", "label": "Carlos Mendez", "type": "person", "weight": 5},
                    {"id": "grace-chen", "label": "Grace Chen", "type": "person", "weight": 6},
                    {"id": "dev-patel", "label": "Dev Patel", "type": "person", "weight": 6},
                    {"id": "seed-funding", "label": "Seed Raise ($1.5M)", "type": "topic", "weight": 8},
                    {"id": "lumen-launch", "label": "Lumen v1 Launch", "type": "topic", "weight": 9},
                    {"id": "operational-costs", "label": "AWS & GPU Bills", "type": "topic", "weight": 5},
                    {"id": "personal-life", "label": "Family & Runs", "type": "topic", "weight": 7}
                ],
                "edges": [
                    {"source": "priya-nair", "target": "seed-funding"},
                    {"source": "maya-chen", "target": "seed-funding"},
                    {"source": "maya-chen", "target": "lumen-launch"},
                    {"source": "nina-adler", "target": "lumen-launch"},
                    {"source": "carlos-mendez", "target": "lumen-launch"},
                    {"source": "maya-chen", "target": "operational-costs"},
                    {"source": "maya-chen", "target": "personal-life"},
                    {"source": "grace-chen", "target": "personal-life"},
                    {"source": "dev-patel", "target": "personal-life"}
                ]
            }, indent=2)

        # 5. Relationships
        elif "relationships" in sys_msg:
            return json.dumps({
                "relationships": [
                    {"name": "Priya Nair", "kind": "Lead Investor", "note": "Sent term sheet for the seed round and is advising on launch pricing strategy."},
                    {"name": "Nina Adler", "kind": "Co-founder / Ops", "note": "Managing candidate offers and coordinating launch blockers."},
                    {"name": "Grace Chen", "kind": "Family", "note": "Concerned about you missing family events; reminder about Sunday birthday."},
                    {"name": "Dev Patel", "kind": "Friend", "note": "Holding you accountable for running and checking in on your quietness."},
                    {"name": "Carlos Mendez", "kind": "Beta User", "note": "Encountering critical API 500 error blocking their launch."}
                ]
            }, indent=2)

        # 6. Emotion Timeline
        elif "emotional tone" in sys_msg or "sentiment score" in sys_msg:
            return json.dumps({
                "days": [
                    {"date": "2026-06-15", "score": 0.4, "mood": "Relieved"},
                    {"date": "2026-06-16", "score": 0.6, "mood": "Excited"},
                    {"date": "2026-06-17", "score": 0.1, "mood": "Hectic"},
                    {"date": "2026-06-18", "score": 0.3, "mood": "Luminous"},
                    {"date": "2026-06-19", "score": -0.5, "mood": "Stressed"}
                ]
            }, indent=2)

        # 7. RAG / Archive Search fallback
        else:
            q = user_msg.lower()
            if "blocking" in q or "block" in q or "v1" in q:
                return "According to Nina Adler, the launch checklist has 6 items left: rate limiting, the onboarding flow, billing webhooks, docs, the status page, and one P0 bug. She estimates a Tuesday launch. In addition, Carlos Mendez is complaining about 500 errors."
            elif "ignoring" in q or "ignore" in q or "people" in q or "quiet" in q or "dev" in q or "family" in q:
                return "Grace Chen emailed to remind you of your Mom's birthday on Sunday at 7 PM and noted that you canceled the last two dinners. Dev Patel also checked in expressing concern because you haven't responded to his texts in weeks."
            else:
                return "Your inbox contains information regarding the Lumen seed round ($1.5M term sheet led by Priya Nair, $50k safe wire from Aileen Park), hiring candidate Priyanka, recent API outages, and an AWS bill surge."

    r = requests.post(
        NIM_URL,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.95,
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


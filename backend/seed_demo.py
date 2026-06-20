"""Seed ChromaDB with a curated demo persona so the expo demo is crisp and
reproducible without a real inbox.

Persona: Maya Chen, founder of an early-stage AI startup (Lumen) — juggling a
seed raise, hiring, shipping v1, and a life outside it. The mix is designed to
produce rich Ego themes, Relationships, a Graph, a stressful Timeline day, and
a pointed Morning Briefing.

Run from the backend/ directory:  python seed_demo.py
"""

from app.connectors import chroma

DEMO_EMAILS = [
    # --- Fundraising ---
    ("d01", "Re: Lumen seed round — term sheet attached", "Priya Nair <priya@northstar.vc>",
     "Tue, 16 Jun 2026 09:12:00 +0000", "Great meeting the team. Attached is our term sheet for the $1.5M seed. We'd love to lead. Can you hop on a call Thursday to walk through the cap table and the 18-month plan?"),
    ("d02", "Following up on our conversation", "Daniel Roth <daniel@founders-capital.com>",
     "Wed, 17 Jun 2026 14:40:00 +0000", "Enjoyed the demo. We're interested but want to see the retention numbers from the last cohort before committing. Could you send the dashboard export?"),
    ("d03", "Intro: Maya <> Aileen (angel, ex-Stripe)", "Sam Okoye <sam@sequoia-scout.com>",
     "Mon, 15 Jun 2026 08:05:00 +0000", "Connecting you two — Aileen has written 30+ checks into AI infra and loved your positioning. Aileen, Maya is building Lumen. I'll let you both take it from here."),
    ("d04", "Wire confirmation — SAFE $50k", "AngelList <notifications@angellist.com>",
     "Thu, 18 Jun 2026 11:30:00 +0000", "The SAFE for your investment from Aileen Park has been countersigned and the $50,000 wire has cleared. Documents are in your AngelList dashboard."),
    # --- Hiring ---
    ("d05", "Application: Founding Engineer — Lumen", "Jordan Lee <jordan.lee.dev@gmail.com>",
     "Tue, 16 Jun 2026 19:22:00 +0000", "I've been following Lumen since your Show HN. 7 years on inference infra at Scale. Would love to be your founding engineer — resume + a side project that's relevant attached."),
    ("d06", "Re: Final round — offer decision by Friday", "Nina Adler <nina@lumen.ai>",
     "Wed, 17 Jun 2026 16:10:00 +0000", "Maya — the candidate from the final round (Priyanka) has a competing offer and needs our decision by Friday. She's excellent. We should move. Comp ask is at the top of our band."),
    ("d07", "Recruiter outreach — sorry to bother", "Tom Briggs <tom@talenthouse.io>",
     "Fri, 19 Jun 2026 10:00:00 +0000", "I have three senior ML engineers actively looking who'd be a fit for an early team. Happy to send profiles, no fee until a hire sticks 90 days."),
    # --- Product / users ---
    ("d08", "Lumen is down — 500s on every request", "Carlos Mendez <carlos@brightpath.io>",
     "Fri, 19 Jun 2026 08:47:00 +0000", "Hey, we've been getting 500s across the API for the last 20 minutes and it's blocking our launch. Can someone look urgently? This is becoming a problem for us."),
    ("d09", "Loving the new dashboard 🎉", "Hannah Wu <hannah@deltacode.dev>",
     "Thu, 18 Jun 2026 13:05:00 +0000", "Just wanted to say the v0.9 dashboard is a huge step up. The latency view alone saved us hours. Whatever you shipped, keep going."),
    ("d10", "Feature request: SSO + audit logs", "Marcus Hale <marcus@ironclad-sec.com>",
     "Wed, 17 Jun 2026 09:33:00 +0000", "We'd roll out Lumen across the org but security needs SAML SSO and exportable audit logs before we can. Any timeline? Happy to be a design partner."),
    ("d11", "Your AWS bill is up 240% this month", "AWS Billing <no-reply@aws.amazon.com>",
     "Thu, 18 Jun 2026 06:00:00 +0000", "Your estimated charges for June are $4,812, up from $1,415 last month. The increase is concentrated in GPU instances. Review your usage in Cost Explorer."),
    # --- Product team ---
    ("d12", "v1 launch checklist — 6 items left", "Nina Adler <nina@lumen.ai>",
     "Fri, 19 Jun 2026 17:45:00 +0000", "We're close. Remaining blockers: rate limiting, the onboarding flow, billing webhooks, docs, the status page, and one P0 bug. Realistically we ship Tuesday if today goes well."),
    ("d13", "Re: Pricing — should we raise before launch?", "Priya Nair <priya@northstar.vc>",
     "Thu, 18 Jun 2026 20:15:00 +0000", "My two cents: you're underpricing. Launch at the higher tier; it's far easier to grandfather early users down than to raise on them later. Don't leave money on the table."),
    # --- Personal / life ---
    ("d14", "Mom's birthday is Sunday — are you coming?", "Grace Chen <grace.chen.family@gmail.com>",
     "Wed, 17 Jun 2026 21:30:00 +0000", "Maya, you've cancelled the last two. Mom won't say it but she misses you. Dinner is Sunday at 7. Please try to be there — work will still be there Monday."),
    ("d15", "still on for our run saturday?", "Dev Patel <dev.patel.runs@gmail.com>",
     "Thu, 18 Jun 2026 18:00:00 +0000", "6am at the park like usual? You said last week you needed to get back to it. No pressure but I'm holding you to it 😄"),
    ("d16", "Re: therapy — moving your Thursday slot", "Dr. Ellis Office <office@ellis-therapy.com>",
     "Mon, 15 Jun 2026 12:00:00 +0000", "Dr. Ellis needs to move your standing Thursday 5pm session this week. We have Wednesday 4pm or Friday 11am open. Let us know what works."),
    # --- Noise / promos ---
    ("d17", "🔥 Your weekly AI roundup: 14 must-reads", "The Batch <newsletter@deeplearning.ai>",
     "Wed, 17 Jun 2026 07:00:00 +0000", "This week: a new open-weights model tops the leaderboards, agents that book their own infra, and why eval is the new moat. Plus 11 more links."),
    ("d18", "You left items in your cart", "Amazon.com <store-news@amazon.com>",
     "Tue, 16 Jun 2026 22:14:00 +0000", "The mechanical keyboard and the standing desk mat in your cart are still available. Complete your order before they sell out."),
    ("d19", "Last chance: 40% off annual plans", "Notion <team@makenotion.com>",
     "Thu, 18 Jun 2026 15:00:00 +0000", "Your trial ends in 3 days. Upgrade now and save 40% on the annual Team plan. Keep your workspace, integrations, and history."),
    ("d20", "LinkedIn: Priya Nair and 8 others viewed your profile", "LinkedIn <notifications@linkedin.com>",
     "Fri, 19 Jun 2026 09:00:00 +0000", "Your profile is getting attention. See who's been looking and grow your network with people in AI and venture."),
    # --- Calendar / ops ---
    ("d21", "Reminder: Board sync tomorrow 10am", "Google Calendar <calendar-notification@google.com>",
     "Wed, 17 Jun 2026 22:00:00 +0000", "Board sync with Priya and Daniel tomorrow at 10:00. Agenda: runway, hiring plan, launch date. You haven't shared the deck yet."),
    ("d22", "Security alert: new sign-in to your account", "Google <no-reply@accounts.google.com>",
     "Thu, 18 Jun 2026 03:12:00 +0000", "A new device signed into your Google Account from San Francisco. If this was you, no action is needed. If not, secure your account now."),
    ("d23", "Invoice from your law firm — formation + SAFEs", "Wilson & Park LLP <billing@wilsonpark.legal>",
     "Tue, 16 Jun 2026 16:40:00 +0000", "Attached is invoice #2041 for $3,200 covering entity formation amendments and SAFE paperwork for the current round. Net 30."),
    ("d24", "you ok? haven't heard from you in weeks", "Dev Patel <dev.patel.runs@gmail.com>",
     "Mon, 15 Jun 2026 23:50:00 +0000", "Not about the run. Just — you've been heads down for a while and the last few texts went quiet. Checking in as a friend. Coffee this week?"),
]


def main():
    rows = [
        {"id": i, "subject": s, "from": f, "date": d, "snippet": sn}
        for (i, s, f, d, sn) in DEMO_EMAILS
    ]
    n = chroma.ingest_emails(rows)
    print(f"Seeded {n} demo emails into ChromaDB.")
    print("Tip: visit /today, /ego, /drift, /graph, /relationships, /timeline to demo.")


if __name__ == "__main__":
    main()

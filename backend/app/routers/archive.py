from fastapi import APIRouter
from pydantic import BaseModel
from app.connectors import chroma, llm

router = APIRouter()

SYSTEM = (
    "You are Lucid, a personal archive assistant. Answer the user's question "
    "using ONLY the email excerpts provided. Be concise and specific. Quote "
    "senders or dates when useful. If the excerpts don't contain the answer, "
    "say so plainly — do not invent details. Write in plain prose with short "
    "paragraphs. Do not use markdown, asterisks, headers, or bullet symbols."
)


class Ask(BaseModel):
    question: str


@router.post("/archive/ask")
def archive_ask(body: Ask):
    hits = chroma.search_emails(body.question, n_results=6)
    if not hits:
        return {"answer": "Your archive is empty — sync some email first.", "sources": []}

    context = "\n\n---\n\n".join(
        f"From: {h['from']}\nDate: {h['date']}\nSubject: {h['subject']}\n{h['text']}"
        for h in hits
    )
    answer = llm.chat(
        [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Email excerpts:\n\n{context}\n\nQuestion: {body.question}",
            },
        ]
    )
    return {"answer": answer, "sources": hits}

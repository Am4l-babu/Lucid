import os
import chromadb

# ponytail: single-user app → local persistent store, no server needed.
# Swap to HttpClient if you ever shard Chroma onto its own host.
_CLIENT = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", "chroma_data"))


def _collection():
    return _CLIENT.get_or_create_collection("emails")


def ingest_emails(emails: list[dict]) -> int:
    if not emails:
        return 0

    _collection().upsert(
        ids=[e["id"] for e in emails],
        documents=[f"{e['subject']} {e['snippet']}" for e in emails],
        metadatas=[{
            "subject": e["subject"],
            "from": e["from"],
            "date": e["date"],
        } for e in emails],
    )
    return len(emails)


def search_emails(query: str, n_results: int = 10) -> list[dict]:
    results = _collection().query(query_texts=[query], n_results=n_results)
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    return [{"text": d, **m} for d, m in zip(docs, metas)]

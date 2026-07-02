import os
import json
from pathlib import Path

try:
    import chromadb
    MOCK_MODE = False
except ImportError:
    MOCK_MODE = True

if MOCK_MODE:
    # A simple JSON-based fallback for environments (like Windows without C++ build tools)
    # where compiling chromadb/chroma-hnswlib is not possible.
    MOCK_FILE = Path("chroma_mock_db.json")
    
    def _read_db() -> list[dict]:
        if MOCK_FILE.exists():
            try:
                return json.loads(MOCK_FILE.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []
        
    def _write_db(data: list[dict]):
        MOCK_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def ingest_emails(emails: list[dict]) -> int:
        if not emails:
            return 0
        db = _read_db()
        db_ids = {e["id"] for e in db}
        added = 0
        for e in emails:
            record = {
                "id": e["id"],
                "text": f"{e['subject']} {e['snippet']}",
                "subject": e["subject"],
                "from": e["from"],
                "date": e["date"],
            }
            if e["id"] in db_ids:
                # Update
                idx = next(i for i, x in enumerate(db) if x["id"] == e["id"])
                db[idx] = record
            else:
                db.append(record)
                added += 1
        _write_db(db)
        return len(emails)

    def search_emails(query: str, n_results: int = 10) -> list[dict]:
        db = _read_db()
        if not query:
            return db[:n_results]
        # Simple keyword overlap search to simulate vector search
        q_words = [w.lower() for w in query.split() if len(w) > 2]
        if not q_words:
            q_words = [query.lower()]
            
        scored = []
        for e in db:
            text = e["text"].lower()
            score = sum(1 for qw in q_words if qw in text)
            scored.append((score, e))
        
        # Sort by match score (descending)
        scored.sort(key=lambda x: x[0], reverse=True)
        # Return records with score > 0, or just return first n_results if no query matches
        results = [e for score, e in scored if score > 0]
        if not results:
            results = [e for score, e in scored]
        return results[:n_results]

    def count() -> int:
        return len(_read_db())

    def sample(limit: int = 60) -> list[dict]:
        return _read_db()[:limit]

    FINANCE_MOCK_FILE = Path("finance_mock_db.json")

    def _read_finance_db() -> list[dict]:
        if FINANCE_MOCK_FILE.exists():
            try:
                return json.loads(FINANCE_MOCK_FILE.read_text(encoding="utf-8"))
            except Exception:
                return []
        return []

    def _write_finance_db(data: list[dict]):
        FINANCE_MOCK_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def ingest_transactions(txns: list[dict]) -> int:
        if not txns:
            return 0
        db = {t["id"]: t for t in _read_finance_db()}
        for t in txns:
            db[t["id"]] = {**t, "text": f"{t['date']} {t['description']} {t['category']}"}
        _write_finance_db(list(db.values()))
        return len(txns)

    def search_transactions(query: str, n_results: int = 10) -> list[dict]:
        db = _read_finance_db()
        q_words = [w.lower() for w in query.split() if len(w) > 2] or [query.lower()]
        scored = [(sum(1 for qw in q_words if qw in t["text"].lower()), t) for t in db]
        scored.sort(key=lambda x: x[0], reverse=True)
        results = [t for score, t in scored if score > 0] or [t for _, t in scored]
        return results[:n_results]

    def all_transactions() -> list[dict]:
        return _read_finance_db()

else:
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

    def count() -> int:
        return _collection().count()

    def sample(limit: int = 60) -> list[dict]:
        """A slice of the whole archive, for analysis jobs (not a query)."""
        data = _collection().get(limit=limit, include=["documents", "metadatas"])
        return [
            {"text": d, **m}
            for d, m in zip(data["documents"], data["metadatas"])
        ]

    def _transactions():
        return _CLIENT.get_or_create_collection("transactions")

    def ingest_transactions(txns: list[dict]) -> int:
        if not txns:
            return 0
        _transactions().upsert(
            ids=[t["id"] for t in txns],
            documents=[f"{t['date']} {t['description']} {t['category']}" for t in txns],
            metadatas=[{
                "date": t["date"],
                "description": t["description"],
                "amount": t["amount"],
                "type": t["type"],
                "category": t["category"],
            } for t in txns],
        )
        return len(txns)

    def search_transactions(query: str, n_results: int = 10) -> list[dict]:
        results = _transactions().query(query_texts=[query], n_results=n_results)
        docs = results["documents"][0]
        metas = results["metadatas"][0]
        return [{"text": d, **m} for d, m in zip(docs, metas)]

    def all_transactions() -> list[dict]:
        """Every transaction, for summary/insight jobs (not a query)."""
        data = _transactions().get(include=["metadatas"])
        return list(data["metadatas"])


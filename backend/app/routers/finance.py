from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.connectors import chroma, finance

router = APIRouter()

MOCK_STATEMENT = Path(__file__).resolve().parents[2] / "mock_data" / "bank_statement.csv"


@router.post("/finance/upload")
async def finance_upload(file: UploadFile = File(...)):
    raw = (await file.read()).decode("utf-8-sig", errors="replace")
    try:
        txns = finance.parse_statement_csv(raw)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    ingested = chroma.ingest_transactions(txns)
    return {"parsed": len(txns), "ingested": ingested}


@router.post("/finance/seed")
def finance_seed():
    """Load the bundled mock bank statement — demo without any real data."""
    if not MOCK_STATEMENT.exists():
        raise HTTPException(status_code=404, detail="Mock statement missing")
    txns = finance.parse_statement_csv(MOCK_STATEMENT.read_text(encoding="utf-8"))
    ingested = chroma.ingest_transactions(txns)
    return {"parsed": len(txns), "ingested": ingested}


@router.get("/finance/summary")
def finance_summary():
    return finance.summarize(chroma.all_transactions())


@router.get("/finance/search")
def finance_search(q: str, n: int = 10):
    return {"results": chroma.search_transactions(q, n)}

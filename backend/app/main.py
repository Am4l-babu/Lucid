from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from dotenv import load_dotenv
import os

load_dotenv()

from app.routers.gmail import router as gmail_router
from app.routers.archive import router as archive_router
from app.routers.ego import router as ego_router
from app.routers.drift import router as drift_router
from app.routers.graph import router as graph_router
from app.routers.relationships import router as relationships_router
from app.routers.timeline import router as timeline_router
from app.routers.briefing import router as briefing_router
from app.routers.sentiment import router as sentiment_router
from app.routers.health import router as health_router
from app.routers.finance import router as finance_router

app = FastAPI(title="Lucid API", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gmail_router)
app.include_router(archive_router)
app.include_router(graph_router)
app.include_router(relationships_router)
app.include_router(timeline_router)
app.include_router(briefing_router)
app.include_router(ego_router)
app.include_router(drift_router)
app.include_router(sentiment_router)
app.include_router(health_router)
app.include_router(finance_router)


@app.get("/docs", include_in_schema=False)
def docs():
    return get_scalar_api_reference(openapi_url="/openapi.json", title="Lucid API")


@app.get("/health")
def health():
    return {"status": "ok"}

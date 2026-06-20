from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from dotenv import load_dotenv
import os

load_dotenv()

from app.routers.gmail import router as gmail_router

app = FastAPI(title="Lucid API", docs_url=None, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gmail_router)


@app.get("/docs", include_in_schema=False)
def docs():
    return get_scalar_api_reference(openapi_url="/openapi.json", title="Lucid API")


@app.get("/health")
def health():
    return {"status": "ok"}

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import documents_router, formulas_router
from app.core.config import settings

app = FastAPI(title=settings.app_name)

# Allow frontend to call API from browser during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/api/v1")
app.include_router(formulas_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event() -> None:
    # Ensure upload folder exists before first file upload.
    Path(settings.uploads_dir).mkdir(parents=True, exist_ok=True)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Welcome to Ebook2LateX API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

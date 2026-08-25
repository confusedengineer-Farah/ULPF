from fastapi import FastAPI
from app.api.routes.events import router as events_router

app = FastAPI(
    title="ULPF",
    description="Universal Log Pre-processing Framework",
    version="0.1.0",
)

app.include_router(
    events_router,
    prefix="/api/v1/events",
    tags=["Events"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ulpf"
    }
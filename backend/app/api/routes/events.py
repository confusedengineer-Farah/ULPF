from fastapi import APIRouter
from pydantic import BaseModel

from app.ingestion.pipeline import process_event


router = APIRouter()


class EventRequest(BaseModel):
    raw_event: str


@router.post("/ingest")
def ingest_event(request: EventRequest):
    result = process_event(request.raw_event)

    return {
        "success": True,
        "data": result,
    }
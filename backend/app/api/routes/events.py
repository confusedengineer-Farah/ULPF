from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ingestion.pipeline import process_event
from app.storage.database import get_db
from app.storage.models import EventRecord
from app.storage.repository import save_event


router = APIRouter()


class EventRequest(BaseModel):
    raw_event: str


@router.post("/ingest")
def ingest_event(
    request: EventRequest,
    db: Session = Depends(get_db),
):
    result = process_event(request.raw_event)

    if not result["success"]:
        return result

    save_event(
        db=db,
        event_data=result["data"],
        plugin=result["plugin"],
    )

    return result


@router.get("")
def get_events(
    format: str | None = None,
    plugin: str | None = None,
    source_ip: str | None = None,
    destination_ip: str | None = None,
    action: str | None = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    # Protect the API from unreasonable requests
    limit = min(max(limit, 1), 100)
    offset = max(offset, 0)

    query = select(EventRecord)

    # Filters
    if format:
        query = query.where(
            EventRecord.format == format
        )

    if plugin:
        query = query.where(
            EventRecord.plugin == plugin
        )

    if source_ip:
        query = query.where(
            EventRecord.source_ip == source_ip
        )

    if destination_ip:
        query = query.where(
            EventRecord.destination_ip == destination_ip
        )

    if action:
        query = query.where(
            EventRecord.action == action
        )

    # Newest events first
    query = (
        query
        .order_by(EventRecord.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    records = db.execute(query).scalars().all()

    return {
        "success": True,
        "count": len(records),
        "limit": limit,
        "offset": offset,
        "data": [
            {
                "event_id": record.event_id,
                "format": record.format,
                "plugin": record.plugin,
                "vendor": record.vendor,
                "product": record.product,
                "source_ip": record.source_ip,
                "destination_ip": record.destination_ip,
                "action": record.action,
                "sha256": record.sha256,
                "created_at": record.created_at,
            }
            for record in records
        ],
    }
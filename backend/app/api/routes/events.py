import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
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
    # Protect API from unreasonable requests
    limit = min(max(limit, 1), 100)
    offset = max(offset, 0)

    # --------------------------------
    # Base query
    # --------------------------------

    query = select(EventRecord)

    # --------------------------------
    # Apply filters
    # --------------------------------

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

    # --------------------------------
    # Count total matching events
    # --------------------------------

    count_query = select(
        func.count(EventRecord.id)
    )

    if format:
        count_query = count_query.where(
            EventRecord.format == format
        )

    if plugin:
        count_query = count_query.where(
            EventRecord.plugin == plugin
        )

    if source_ip:
        count_query = count_query.where(
            EventRecord.source_ip == source_ip
        )

    if destination_ip:
        count_query = count_query.where(
            EventRecord.destination_ip == destination_ip
        )

    if action:
        count_query = count_query.where(
            EventRecord.action == action
        )

    total = db.execute(
        count_query
    ).scalar_one()

    # --------------------------------
    # Fetch current page
    # --------------------------------

    query = (
        query
        .order_by(
            EventRecord.created_at.desc()
        )
        .offset(offset)
        .limit(limit)
    )

    records = (
        db.execute(query)
        .scalars()
        .all()
    )

    # --------------------------------
    # Response
    # --------------------------------

    return {
        "success": True,

        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_next": (
                offset + len(records) < total
            ),
        },

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


@router.get("/stats")
def get_event_stats(
    db: Session = Depends(get_db),
):
    total_events = db.execute(
        select(func.count(EventRecord.id))
    ).scalar_one()

    format_rows = db.execute(
        select(
            EventRecord.format,
            func.count(EventRecord.id),
        )
        .group_by(EventRecord.format)
    ).all()

    plugin_rows = db.execute(
        select(
            EventRecord.plugin,
            func.count(EventRecord.id),
        )
        .group_by(EventRecord.plugin)
    ).all()

    action_rows = db.execute(
        select(
            EventRecord.action,
            func.count(EventRecord.id),
        )
        .group_by(EventRecord.action)
    ).all()

    return {
        "success": True,
        "data": {
            "total_events": total_events,

            "formats": {
                str(format_name): count
                for format_name, count in format_rows
            },

            "plugins": {
                str(plugin_name): count
                for plugin_name, count in plugin_rows
            },

            "actions": {
                str(action_name): count
                for action_name, count in action_rows
            },
        },
    }

@router.get("/{event_id}")
def get_event(
    event_id: str,
    db: Session = Depends(get_db),
):
    query = select(EventRecord).where(
        EventRecord.event_id == event_id
    )

    record = db.execute(query).scalar_one_or_none()

    if record is None:
        return {
            "success": False,
            "error": "Event not found",
        }

    try:
        normalized_event = json.loads(
            record.normalized_json
        )
    except json.JSONDecodeError:
        normalized_event = None

    return {
        "success": True,
        "data": {
            "event_id": record.event_id,
            "plugin": record.plugin,
            "format": record.format,
            "vendor": record.vendor,
            "product": record.product,

            "normalized": normalized_event,

            "raw": {
                "payload": record.raw_payload,
                "sha256": record.sha256,
            },

            "created_at": record.created_at,
        },
    }


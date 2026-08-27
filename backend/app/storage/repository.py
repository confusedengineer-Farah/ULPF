import json

from sqlalchemy.orm import Session

from app.storage.models import EventRecord


def save_event(
    db: Session,
    event_data: dict,
    plugin: str | None,
) -> EventRecord:

    record = EventRecord(
        event_id=event_data["event_id"],

        format=event_data["raw"]["format"],

        plugin=plugin,

        vendor=event_data["source"].get("vendor"),

        product=event_data["source"].get("product"),

        source_ip=(
            event_data["network"]["source"].get("ip")
        ),

        destination_ip=(
            event_data["network"]["destination"].get("ip")
        ),

        action=event_data["event"].get("action"),

        raw_payload=event_data["raw"]["payload"],

        normalized_json=json.dumps(
            event_data,
            default=str,
        ),

        sha256=event_data["raw"]["sha256"],
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
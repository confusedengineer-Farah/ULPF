import json

from app.storage.database import SessionLocal, Base, engine
from app.storage.models import EventRecord


def setup_module():

    Base.metadata.create_all(bind=engine)


def teardown_function():

    db = SessionLocal()

    db.query(EventRecord).delete()
    db.commit()
    db.close()


def test_event_record_can_be_stored():

    db = SessionLocal()

    event = EventRecord(
        event_id="evt_test_001",
        format="cef",
        plugin="custom_firewall",
        vendor="TestVendor",
        product="Firewall",
        source_ip="10.0.0.5",
        destination_ip="192.168.1.20",
        action="allow",
        raw_payload="CEF:test",
        normalized_json=json.dumps({
            "event_id": "evt_test_001"
        }),
        sha256="a" * 64,
    )

    db.add(event)
    db.commit()

    stored = (
        db.query(EventRecord)
        .filter_by(event_id="evt_test_001")
        .first()
    )

    assert stored is not None
    assert stored.format == "cef"
    assert stored.plugin == "custom_firewall"
    assert stored.source_ip == "10.0.0.5"
    assert stored.sha256 == "a" * 64

    db.close()
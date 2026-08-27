import hashlib

from app.normalization.engine import normalize_event


def test_cef_normalization():

    raw = (
        "CEF:0|TestVendor|Firewall|1.0|100|"
        "Connection Allowed|5|"
        "src=10.0.0.5 dst=192.168.1.20 "
        "spt=443 dpt=5500 proto=TCP action=allow"
    )

    parsed_data = {
        "vendor": "TestVendor",
        "product": "Firewall",
        "src": "10.0.0.5",
        "dst": "192.168.1.20",
        "spt": "443",
        "dpt": "5500",
        "proto": "TCP",
        "action": "allow",
    }

    event = normalize_event(
        raw_event=raw,
        log_format="cef",
        parsed_data=parsed_data,
        parser_name="CEFParser",
        plugin_id="custom_firewall",
    )

    assert event.source.vendor == "TestVendor"
    assert event.source.product == "Firewall"

    assert event.network.source.ip == "10.0.0.5"
    assert event.network.source.port == 443

    assert event.network.destination.ip == "192.168.1.20"
    assert event.network.destination.port == 5500

    assert event.network.protocol == "TCP"

    assert event.event.action == "allow"


def test_type_conversion():

    raw = "test"

    parsed_data = {
        "source_port": "443",
        "destination_port": "5500",
        "enabled": "true",
        "disabled": "false",
        "count": "10",
    }

    event = normalize_event(
        raw_event=raw,
        log_format="test",
        parsed_data=parsed_data,
        parser_name="TestParser",
    )

    assert event.extensions["source_port"] == 443
    assert event.extensions["destination_port"] == 5500

    assert event.extensions["enabled"] is True
    assert event.extensions["disabled"] is False

    assert event.extensions["count"] == 10


def test_unknown_fields_are_preserved():

    raw = "CEF:test"

    parsed_data = {
        "vendor": "TestVendor",
        "product": "Firewall",
        "src": "10.0.0.5",
        "unknown_field": "important-value",
        "rule_id": "FW-1029",
    }

    event = normalize_event(
        raw_event=raw,
        log_format="cef",
        parsed_data=parsed_data,
        parser_name="CEFParser",
        plugin_id="custom_firewall",
    )

    assert event.extensions["unknown_field"] == "important-value"
    assert event.extensions["rule_id"] == "FW-1029"


def test_raw_payload_is_preserved():

    raw = (
        "CEF:0|TestVendor|Firewall|1.0|100|"
        "Connection Allowed|5|src=10.0.0.5"
    )

    parsed_data = {
        "vendor": "TestVendor",
        "product": "Firewall",
    }

    event = normalize_event(
        raw_event=raw,
        log_format="cef",
        parsed_data=parsed_data,
        parser_name="CEFParser",
    )

    assert event.raw.payload == raw


def test_sha256_integrity():

    raw = "important raw event"

    parsed_data = {
        "message": "important raw event",
    }

    event = normalize_event(
        raw_event=raw,
        log_format="test",
        parsed_data=parsed_data,
        parser_name="TestParser",
    )

    expected_hash = hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()

    assert event.raw.sha256 == expected_hash


def test_traceability():

    raw = "test event"

    parsed_data = {}

    event = normalize_event(
        raw_event=raw,
        log_format="test",
        parsed_data=parsed_data,
        parser_name="TestParser",
        parser_version="2.0",
    )

    assert event.traceability.parser == "TestParser"
    assert event.traceability.parser_version == "2.0"

    assert event.traceability.raw_event_id.startswith(
        "raw_"
    )

    assert event.event_id.startswith(
        "evt_"
    )
from app.ingestion.pipeline import process_event


def test_cef_end_to_end():

    raw = (
        "CEF:0|TestVendor|Firewall|1.0|100|"
        "Connection Allowed|5|"
        "src=10.0.0.5 dst=192.168.1.20 "
        "spt=443 dpt=5500 proto=TCP action=allow"
    )

    result = process_event(raw)

    assert result["success"] is True
    assert result["plugin"] == "custom_firewall"

    data = result["data"]

    assert data["raw"]["format"] == "cef"
    assert data["raw"]["payload"] == raw

    assert data["network"]["source"]["ip"] == "10.0.0.5"
    assert data["network"]["source"]["port"] == 443

    assert data["network"]["destination"]["ip"] == "192.168.1.20"
    assert data["network"]["destination"]["port"] == 5500

    assert data["network"]["protocol"] == "TCP"
    assert data["event"]["action"] == "allow"


def test_csv_end_to_end():

    raw = (
        "source_ip,destination_ip,source_port,"
        "destination_port,protocol,action\n"
        "10.0.0.5,192.168.1.20,443,5500,TCP,allow"
    )

    result = process_event(raw)

    assert result["success"] is True
    assert result["plugin"] == "csv_firewall"

    data = result["data"]

    assert data["raw"]["format"] == "csv"

    assert data["network"]["source"]["ip"] == "10.0.0.5"
    assert data["network"]["source"]["port"] == 443

    assert data["network"]["destination"]["ip"] == "192.168.1.20"
    assert data["network"]["destination"]["port"] == 5500

    assert data["network"]["protocol"] == "TCP"
    assert data["event"]["action"] == "allow"


def test_unknown_event_falls_back_to_generic():

    raw = "This is an unknown firewall event"

    result = process_event(raw)

    assert result["success"] is True
    assert result["plugin"] is None

    data = result["data"]

    assert data["raw"]["format"] == "unknown"
    assert data["traceability"]["parser"] == "GenericParser"
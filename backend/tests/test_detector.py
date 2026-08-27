from app.ingestion.detector import (
    LogFormat,
    detect_format,
)


def test_detect_json():

    raw = '{"src":"10.0.0.5","action":"allow"}'

    assert detect_format(raw) == LogFormat.JSON


def test_detect_cef():

    raw = (
        "CEF:0|TestVendor|Firewall|1.0|100|"
        "Connection Allowed|5|src=10.0.0.5"
    )

    assert detect_format(raw) == LogFormat.CEF


def test_detect_syslog():

    raw = "<134>Aug 25 17:20:31 FW01 Connection allowed"

    assert detect_format(raw) == LogFormat.SYSLOG


def test_detect_csv():

    raw = (
        "source_ip,destination_ip,action\n"
        "10.0.0.5,192.168.1.20,allow"
    )

    assert detect_format(raw) == LogFormat.CSV


def test_detect_unknown():

    raw = "random firewall event"

    assert detect_format(raw) == LogFormat.UNKNOWN
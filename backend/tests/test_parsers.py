from app.parsers.json_parser import JSONParser
from app.parsers.cef_parser import CEFParser
from app.parsers.syslog_parser import SyslogParser
from app.parsers.csv_parser import CSVParser


def test_json_parser():

    raw = '{"src":"10.0.0.5","action":"allow"}'

    result = JSONParser().parse(raw)

    assert result["success"] is True
    assert result["data"]["src"] == "10.0.0.5"
    assert result["data"]["action"] == "allow"


def test_cef_parser():

    raw = (
        "CEF:0|TestVendor|Firewall|1.0|100|"
        "Connection Allowed|5|"
        "src=10.0.0.5 dst=192.168.1.20 "
        "spt=443 dpt=5500 proto=TCP action=allow"
    )

    result = CEFParser().parse(raw)

    assert result["success"] is True

    data = result["data"]

    assert data["vendor"] == "TestVendor"
    assert data["product"] == "Firewall"
    assert data["src"] == "10.0.0.5"
    assert data["dst"] == "192.168.1.20"
    assert data["spt"] == "443"
    assert data["dpt"] == "5500"
    assert data["proto"] == "TCP"
    assert data["action"] == "allow"


def test_syslog_parser():

    raw = (
        "<134>Aug 25 17:20:31 "
        "FW01 Connection allowed"
    )

    result = SyslogParser().parse(raw)

    assert result["success"] is True


def test_csv_parser():

    raw = (
        "source_ip,destination_ip,source_port,"
        "destination_port,protocol,action\n"
        "10.0.0.5,192.168.1.20,443,5500,TCP,allow"
    )

    result = CSVParser().parse(raw)

    assert result["success"] is True

    data = result["data"]

    assert data["source_ip"] == "10.0.0.5"
    assert data["destination_ip"] == "192.168.1.20"
    assert data["source_port"] == "443"
    assert data["destination_port"] == "5500"
    assert data["protocol"] == "TCP"
    assert data["action"] == "allow"
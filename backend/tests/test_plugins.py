from app.plugins.manager import PluginManager
from app.plugins.detector import detect_plugin


def create_plugin_manager():
    manager = PluginManager()
    manager.load_plugins()
    return manager


def test_plugins_are_discovered():

    manager = create_plugin_manager()

    plugins = manager.list_plugins()

    plugin_ids = {
        plugin["id"]
        for plugin in plugins
    }

    assert "cisco_asa" in plugin_ids
    assert "fortigate" in plugin_ids
    assert "custom_firewall" in plugin_ids
    assert "csv_firewall" in plugin_ids


def test_cef_plugin_matching():

    manager = create_plugin_manager()

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

    result = detect_plugin(
        parsed_data=parsed_data,
        log_format="cef",
        plugins=manager.list_plugins(),
    )

    assert result["plugin_id"] == "custom_firewall"


def test_csv_plugin_matching():

    manager = create_plugin_manager()

    parsed_data = {
        "source_ip": "10.0.0.5",
        "destination_ip": "192.168.1.20",
        "source_port": "443",
        "destination_port": "5500",
        "protocol": "TCP",
        "action": "allow",
    }

    result = detect_plugin(
        parsed_data=parsed_data,
        log_format="csv",
        plugins=manager.list_plugins(),
    )

    assert result["plugin_id"] == "csv_firewall"


def test_unknown_source_has_no_plugin():

    manager = create_plugin_manager()

    parsed_data = {
        "random_field": "random_value",
    }

    result = detect_plugin(
        parsed_data=parsed_data,
        log_format="unknown",
        plugins=manager.list_plugins(),
    )

    assert result["plugin_id"] is None


def test_plugin_mapping():

    manager = create_plugin_manager()

    mapping = manager.get_mapping(
        "custom_firewall"
    )

    assert mapping["src"] == "network.source.ip"
    assert mapping["dst"] == "network.destination.ip"
    assert mapping["spt"] == "network.source.port"
    assert mapping["dpt"] == "network.destination.port"
    assert mapping["proto"] == "network.protocol"
    assert mapping["action"] == "event.action"
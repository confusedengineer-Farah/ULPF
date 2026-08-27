import json
from pathlib import Path
from typing import Any


class PluginManager:

    def __init__(self, plugin_directory: str | None = None):

        if plugin_directory:
            self.plugin_directory = Path(plugin_directory)
        else:
            # manager.py
            #   ↓
            # app/plugins/
            #   ↓
            # app/
            #   ↓
            # backend/
            #   ↓
            # ULPF/
            self.plugin_directory = (
                Path(__file__).resolve().parents[3] / "plugins"
            )

        self.plugins: dict[str, dict[str, Any]] = {}

    def load_plugins(self) -> None:

        if not self.plugin_directory.exists():
            return

        for plugin_path in self.plugin_directory.iterdir():

            if not plugin_path.is_dir():
                continue

            config_path = plugin_path / "source.json"

            if not config_path.exists():
                continue

            try:

                with open(
                    config_path,
                    "r",
                    encoding="utf-8"
                ) as file:

                    config = json.load(file)

                plugin_id = config.get("id")

                if plugin_id:
                    self.plugins[plugin_id] = config

            except (json.JSONDecodeError, OSError):
                continue

    def get_plugin(
        self,
        plugin_id: str
    ) -> dict[str, Any] | None:

        return self.plugins.get(plugin_id)

    def get_mapping(
        self,
        plugin_id: str
    ) -> dict[str, str]:

        plugin = self.get_plugin(plugin_id)

        if not plugin:
            return {}

        return plugin.get("field_mappings", {})

    def list_plugins(self) -> list[dict[str, Any]]:

        return list(self.plugins.values())
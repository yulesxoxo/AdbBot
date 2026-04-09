"""Play Store Main Module."""

import logging
import pprint

from adb_bot.decorators import (
    register_command,
    register_custom_routine_choice,
    register_game,
)
from adb_bot.game import Game
from adb_bot.games.src.zzz_ui_testing.settings import Settings
from adb_bot.models.decorators import GUIMetadata
from adb_bot.models.registries import GameMetadata, SettingsConfig


@register_game(
    GameMetadata(
        name="Google Play - UI Testing",
        settings_config=SettingsConfig(cls=Settings, file="ZzzConfigExample.toml"),
    )
)
class PlayStore(Game):
    """Just for GUI testing."""

    @property
    def settings(self) -> Settings:
        return Settings.from_toml(self.settings_file_path)

    def __init__(self) -> None:
        """Initialize PlayStore."""
        super().__init__()
        self.package_name_prefixes = [
            "com.android.vending",
        ]

    @register_command(
        gui=GUIMetadata(label="Log Settings", category="Category", tooltip="Tooltip")
    )
    def _test_gui(self) -> None:
        logging.info(f"{pprint.pformat(self.settings)}")

    @register_command()
    def _test_cli(self) -> None:
        logging.info("CLI")

    @register_custom_routine_choice(label="Choice")
    def _test_custom_routine(self) -> None:
        logging.info("CUSTOM ROUTINE")

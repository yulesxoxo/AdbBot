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
from adb_bot.models.device import Resolution
from adb_bot.models.registries import SettingsConfig


@register_game("Google Play - UI Testing")
class PlayStore(Game):
    """Just for UI testing."""

    @property
    def package_names(self) -> list[str]:
        return ["com.android.vending"]

    @property
    def base_resolution(self) -> Resolution:
        return Resolution.from_string("1080x1920")

    @property
    def settings_config(self) -> SettingsConfig:
        return SettingsConfig(cls=Settings, file="ZzzConfigExample.toml")

    @property
    def settings(self) -> Settings:
        return Settings.from_toml(self.settings_file_path)

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

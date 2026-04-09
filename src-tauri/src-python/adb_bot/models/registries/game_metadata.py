"""GameMetadata."""

from dataclasses import dataclass
from enum import StrEnum

from adb_bot.models.pydantic import TomlSettings


@dataclass
class SettingsConfig:
    """Settings Metadata.

    Attributes:
        file (str): Settings file name.
        cls (type[TomlSettings]): Settings class.
    """

    file: str
    cls: type[TomlSettings]


@dataclass
class GameMetadata:
    """Metadata used to describe a Game.

    Attributes:
        display_name (str): The name of the Game.
        settings_config (SettingsConfig | None): Config for saving/loading game
            settings.
        category_order (list[str | StrEnum] | None): Order in which categories should be
            displayed in the GUI.
    """

    display_name: str
    settings_config: SettingsConfig | None = None
    category_order: list[str | StrEnum] | None = None

from abc import ABC, abstractmethod
from pathlib import Path

from adb_bot.exceptions import AutoPlayerUnrecoverableError
from adb_bot.io import SettingsLoader
from adb_bot.models import ConfidenceValue
from adb_bot.models.device import Resolution
from adb_bot.models.pydantic import TomlSettings
from adb_bot.models.registries import SettingsConfig


class GameSettingsABC(ABC):
    """Abstract class for game settings related code."""

    default_threshold: ConfidenceValue = ConfidenceValue("90%")

    @property
    def base_resolution(self) -> Resolution:
        """Expected resolution for this game."""
        return Resolution.from_string("1920x1080")

    @property
    @abstractmethod
    def package_names(self) -> list[str]:
        """List of package names.

        Functions using this will typically just check if the current games package name
        begins with any item listed here
        e.g. AFK Journey
            Global: com.farlightgames.igame.gp
            Vietnam: com.farlightgames.igame.gp.vn
        com.farlightgames.igame.gp will match both cases.
        """
        ...

    @property
    @abstractmethod
    def settings_config(self) -> SettingsConfig | None:
        """Required property to configure the game settings."""
        ...

    @property
    @abstractmethod
    def settings(self) -> TomlSettings:
        """Required property to return the game settings.

        Update the reference implementation for type hinting.
        """
        if self.settings_config is None:
            raise AutoPlayerUnrecoverableError("SettingsConfig is not set.")

        return self.settings_config.cls.from_toml(self.settings_file_path)

    @property
    def settings_file_path(self) -> Path:
        """Path for settings file."""
        if self.settings_config is None:
            raise AutoPlayerUnrecoverableError("SettingsConfig is not set.")

        return SettingsLoader.settings_dir() / self.settings_config.file

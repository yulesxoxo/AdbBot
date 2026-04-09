import logging
from abc import ABC, abstractmethod
from functools import cached_property, lru_cache
from pathlib import Path

import numpy as np
from adb_bot.exceptions import AutoPlayerUnrecoverableError
from adb_bot.io import SettingsLoader
from adb_bot.models import ConfidenceValue
from adb_bot.models.device import Resolution
from adb_bot.models.geometry import Point
from adb_bot.models.pydantic import TomlSettings
from adb_bot.models.registries import SettingsConfig
from adb_bot.util import StringHelper


class GameBaseABC(ABC):
    """Abstract class for game settings related code."""

    default_threshold: ConfidenceValue = ConfidenceValue("90%")

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

    @property
    def base_resolution(self) -> Resolution:
        """Expected resolution for this game."""
        return Resolution.from_string("1920x1080")

    @property
    def center(self) -> Point:
        """Return center Point of display."""
        return self.base_resolution.center

    @cached_property
    def template_dir(self) -> Path:
        """Retrieve path to images."""
        module = StringHelper.get_game_module(self.__module__)
        template_dir = SettingsLoader.games_dir() / "templates" / module
        logging.debug(f"{module} template path: {template_dir}")
        return template_dir

    @lru_cache
    def get_templates_from_dir(self, subdir: str) -> list[str]:
        """Return a list of all files inside a given template subdirectory.

        returns relative paths (e.g. 'power_saving_mode/1.png').
        """
        template_dir = self.template_dir / subdir

        return [
            f"{subdir}/{path.name}" for path in template_dir.iterdir() if path.is_file()
        ]

    @abstractmethod
    def screenshot(self) -> np.ndarray:
        """Gets screenshot from device."""
        ...

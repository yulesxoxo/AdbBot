"""Provides a registry mechanism for Games."""

from enum import StrEnum
from types import FunctionType

from adb_bot.models.registries import GameMetadata
from adb_bot.registries import GAME_REGISTRY
from adb_bot.util import StringHelper


def register_game(display_name: str, category_order: list[str | StrEnum] | None = None):
    """Decorator to register a game class in the GAME_REGISTRY.

    Args:
        display_name (str): Display name of the game.
        category_order (list[str | StrEnum] | None): Order in which categories should be
            displayed in the GUI.

    Raises:
        TypeError: If the decorator is used on a non-class object.
    """

    def decorator(cls):
        if isinstance(cls, FunctionType):
            raise TypeError("The @register_game decorator can only be used on classes.")

        if not hasattr(cls, "get_settings_config"):
            raise AttributeError(
                f"Class '{cls.__name__}' must define a 'get_settings_config' function "
                "to be registered as a game."
            )

        metadata = GameMetadata(
            display_name=display_name,
            category_order=category_order,
            settings_config=cls.get_settings_config(),
        )

        module_key = StringHelper.get_game_module(cls.__module__)
        GAME_REGISTRY[module_key] = metadata
        return cls

    return decorator

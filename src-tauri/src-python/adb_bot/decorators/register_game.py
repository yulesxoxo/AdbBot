"""Provides a registry mechanism for Games.

It defines data structures to describe game Settings and GUI display
metadata, as well as a decorator `@register_game` that associates game
classes with their metadata and stores them in a central registry.

Classes:
    GameMetadata: Holds overall metadata for a game.

Globals:
    GAME_REGISTRY (dict): A mapping of module keys to `GameMetadata` entries for
        all registered games.

Functions:
    register_game: A decorator used to register game classes and
        populate the `GAME_REGISTRY`.

"""

from types import FunctionType

from adb_bot.models.registries import GameMetadata
from adb_bot.registries import GAME_REGISTRY
from adb_bot.util import StringHelper


def register_game(
    metadata: GameMetadata,
):
    """Decorator to register a game class in the GAME_REGISTRY.

    Args:
        metadata (GameMetadata): The game metadata to register.

    Raises:
        TypeError: If the decorator is used on a non-class object.
    """

    def decorator(cls):
        if isinstance(cls, FunctionType):
            raise TypeError("The @register_game decorator can only be used on classes.")
        module_key = StringHelper.get_game_module(cls.__module__)
        GAME_REGISTRY[module_key] = metadata
        return cls

    return decorator

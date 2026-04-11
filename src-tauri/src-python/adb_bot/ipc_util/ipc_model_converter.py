"""IPC Model Converter."""

from enum import StrEnum

from adb_bot.io import SettingsLoader
from adb_bot.ipc import GameGUIOptions, MenuOption
from adb_bot.models.commands import Command
from adb_bot.models.decorators import GUIMetadata
from adb_bot.models.registries import GameMetadata
from adb_bot.registries import COMMAND_REGISTRY


class IPCModelConverter:
    """Util class for converting from and to IPC models."""

    @staticmethod
    def convert_game_to_gui_options(
        module: str,
        game: GameMetadata,
    ) -> GameGUIOptions:
        """Convert GameMetadata to GameGUIOptions for GUI IPC."""
        categories = IPCModelConverter._extract_categories_from_game(game)
        menu_options = IPCModelConverter._build_menu_options(module, game)
        categories_from_menu = IPCModelConverter._extract_categories_from_menu_options(
            menu_options
        )
        categories = list(dict.fromkeys(categories + categories_from_menu))
        settings_file = None
        if game.settings_config:
            settings_file = game.settings_config.file
        return GameGUIOptions(
            game_title=game.display_name,
            settings_file=settings_file,
            menu_options=menu_options,
            categories=list(categories),
        )

    @staticmethod
    def _convert_command_to_menu_option(
        command: Command,
        game_metadata: GameMetadata,
    ) -> MenuOption | None:
        """Convert MenuItem to MenuOption for GUI IPC."""
        gui_metadata = command.gui_metadata
        if not gui_metadata:
            return None

        return MenuOption(
            label=gui_metadata.label,
            args=[command.name],
            custom_label=IPCModelConverter._resolve_dynamic_label(
                gui_metadata,
                game_metadata,
            ),
            category=gui_metadata.category,
            tooltip=command.tooltip,
        )

    @staticmethod
    def _extract_categories_from_game(game: GameMetadata) -> list[str]:
        """Extract categories from game metadata, preserving order and uniqueness."""
        categories: dict[str, None] = {}

        if game.category_order:
            for value in game.category_order:
                key = value.value if isinstance(value, StrEnum) else value
                categories[key] = None  # insertion order is preserved

        return list(categories.keys())

    @staticmethod
    def _build_menu_options(module: str, game: GameMetadata) -> list[MenuOption]:
        """Build menu options from game and common commands."""
        menu_options: list[MenuOption] = []
        menu_options.extend(
            IPCModelConverter._get_menu_options_from_commands(module, game)
        )
        menu_options.extend(
            IPCModelConverter._get_menu_options_from_commands("Commands", game)
        )

        return menu_options

    @staticmethod
    def _get_menu_options_from_commands(
        module: str, game: GameMetadata
    ) -> list[MenuOption]:
        """Get menu options from commands in a specific module."""
        menu_options: list[MenuOption] = []

        for name, command in COMMAND_REGISTRY.get(module, {}).items():
            if menu_option := IPCModelConverter._convert_command_to_menu_option(
                command,
                game,
            ):
                menu_options.append(menu_option)

        return menu_options

    @staticmethod
    def _extract_categories_from_menu_options(
        menu_options: list[MenuOption],
    ) -> list[str]:
        """Extract categories from menu options, preserving order and uniqueness."""
        categories: dict[str, None] = {}

        for menu_option in menu_options:
            if menu_option.category:
                categories[menu_option.category] = None  # Insert while preserving order

        return list(categories.keys())

    @staticmethod
    def _resolve_dynamic_label(
        gui_metadata: GUIMetadata,
        game_metadata: GameMetadata,
    ) -> str | None:
        if (
            not gui_metadata.dynamic_label_settings_property
            or not game_metadata.settings_config
        ):
            return None

        try:
            settings = game_metadata.settings_config.cls.from_toml(
                SettingsLoader.settings_dir() / game_metadata.settings_config.file
            )
        except Exception:
            return None

        if not settings:
            return None

        path_parts = gui_metadata.dynamic_label_settings_property.split(".")
        current = settings

        try:
            for part in path_parts:
                current = getattr(current, part)

            if current:
                return str(current)
        except AttributeError:
            pass

        return None

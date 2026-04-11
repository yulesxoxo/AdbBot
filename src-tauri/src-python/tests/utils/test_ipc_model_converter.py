"""Tests for IPCModelConverter."""

from unittest.mock import patch

from adb_bot.ipc_util import IPCModelConverter
from adb_bot.models.commands import Command
from adb_bot.models.decorators import GUIMetadata
from adb_bot.models.pydantic import TomlSettings
from adb_bot.models.registries import GameMetadata, SettingsConfig


class TestIPCModelConverter:
    """Test cases for IPCModelConverter."""

    def test_convert_convert_to_menu_option_basic(self):
        """Test basic conversion of MenuItem to MenuOption."""
        command = Command(
            name="test.command",
            action=print,
            gui_metadata=GUIMetadata(
                label="Test Command",
                category="test",
            ),
            tooltip="Test tooltip",
        )
        game_metadata = GameMetadata(display_name="Test Game")

        result = IPCModelConverter._convert_command_to_menu_option(
            command, game_metadata
        )

        assert result is not None
        assert result.label == "Test Command"
        assert result.args == ["test.command"]
        assert result.custom_label is None
        assert result.category == "test"
        assert result.tooltip == "Test tooltip"

    @patch.object(IPCModelConverter, "_resolve_dynamic_label")
    def test_convert_command_to_menu_option_with_dynamic_label(self, mock_resolve):
        """Test conversion with customizable label."""
        mock_resolve.return_value = "Custom Label"

        command = Command(
            name="test.command",
            action=print,
            gui_metadata=GUIMetadata(
                label="Original Label",
                category="test",
            ),
            tooltip="Test tooltip",
        )
        game_metadata = GameMetadata(display_name="Test Game")

        result = IPCModelConverter._convert_command_to_menu_option(
            command, game_metadata
        )

        assert result is not None
        assert result.label == "Original Label"
        assert result.custom_label == "Custom Label"

    def test_extract_categories_from_game_only_name(self):
        """Test category extraction with no GUI metadata."""
        game = GameMetadata(display_name="Test Game")

        categories = IPCModelConverter._extract_categories_from_game(game)

        assert categories == list()

    @patch("adb_bot.registries.COMMAND_REGISTRY")
    def test_get_menu_options_from_commands_empty_module(self, mock_registry):
        """Test getting menu options from non-existent module."""
        mock_registry.get.return_value = {}

        game = GameMetadata(display_name="Test Game")

        result = IPCModelConverter._get_menu_options_from_commands("NonExistent", game)

        assert result == []

    def test_resolve_dynamic_label_no_label_from_settings(self):
        """Test label resolution when no label_from_settings is set."""
        gui_metadata = GUIMetadata(
            label="section.label",
        )
        game_metadata = GameMetadata(display_name="Test Game")

        result = IPCModelConverter._resolve_dynamic_label(gui_metadata, game_metadata)

        assert result is None

    def test_resolve_dynamic_label_no_settings_file_path(self):
        """Test label resolution when no Settings file path is set."""
        gui_metadata = GUIMetadata(
            label="Original Label", dynamic_label_settings_property="section.label"
        )
        game_metadata = GameMetadata(display_name="Test Game")

        result = IPCModelConverter._resolve_dynamic_label(gui_metadata, game_metadata)

        assert result is None

    def test_resolve_dynamic_label(self):
        """Test label resolution when no GUI metadata is present."""
        gui_metadata = GUIMetadata(
            label="Original Label", dynamic_label_settings_property="section.label"
        )
        game_metadata = GameMetadata(
            display_name="Test Game",
            settings_config=SettingsConfig(
                file="test.toml",
                cls=TomlSettings,
            ),
        )

        result = IPCModelConverter._resolve_dynamic_label(gui_metadata, game_metadata)

        assert result is None

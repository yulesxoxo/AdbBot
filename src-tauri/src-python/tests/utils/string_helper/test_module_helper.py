import pytest
from adb_bot.util import StringHelper


class TestGetGameModule:
    """Test class for get_game_module utility function."""

    def test_valid_game_module(self):
        """Test that valid game modules are correctly extracted."""
        assert (
            StringHelper.get_game_module("adb_bot.games.src.guitar_girl.guitar_girl")
            == "guitar_girl"
        )
        assert (
            StringHelper.get_game_module("adb_bot.games.src.zzz_ui_testing.main")
            == "zzz_ui_testing"
        )

    def test_empty_module_path(self):
        """Test that empty or whitespace-only strings raise ValueError."""
        with pytest.raises(
            ValueError, match="Module path cannot be empty or just whitespace"
        ):
            StringHelper.get_game_module("")

        with pytest.raises(ValueError):
            StringHelper.get_game_module("   ")

    def test_module_path_too_short(self):
        """Test that module paths shorter than 3 parts raise ValueError."""
        with pytest.raises(ValueError, match="is too short"):
            StringHelper.get_game_module("games")

        with pytest.raises(ValueError, match="is too short"):
            StringHelper.get_game_module("one.two")

        with pytest.raises(ValueError, match="is too short"):
            StringHelper.get_game_module("one.two.three")

    def test_missing_games_part(self):
        """Test that module paths without 'games' as second part raise ValueError."""
        with pytest.raises(ValueError, match="Expected 'games' as the second part"):
            StringHelper.get_game_module("root.notgames.src.poker")

        with pytest.raises(ValueError, match="Expected 'games' as the second part"):
            StringHelper.get_game_module("games.poker.games.games")

    def test_missing_src_part(self):
        """Test that module paths without 'src' as third part raise ValueError."""
        with pytest.raises(ValueError, match="Expected 'src' as the third part"):
            StringHelper.get_game_module("root.games.notsrc.poker")

        with pytest.raises(ValueError, match="Expected 'src' as the third part"):
            StringHelper.get_game_module("src.games.poker.src")

from pathlib import Path

from adb_bot.cv import IO
from adb_bot.cv.matching import TemplateMatcher
from adb_bot.models import ConfidenceValue


class TestSimilarImage:
    """Tests for similar_image function."""

    def test_identical_images_returns_true(self):
        """Test that identical images return True."""
        image1 = IO.load_image(Path(__file__).parent / "data" / "guitar_girl_busk")
        result = TemplateMatcher.similar_image(image1, image1, ConfidenceValue("80%"))

        assert result is True

    def test_different_images_returns_false(self):
        """Test that different images return False."""
        image1 = IO.load_image(Path(__file__).parent / "data" / "guitar_girl_busk")
        image2 = IO.load_image(Path(__file__).parent / "data" / "guitar_girl_play")

        result = TemplateMatcher.similar_image(image1, image2, ConfidenceValue("90%"))

        assert result is False

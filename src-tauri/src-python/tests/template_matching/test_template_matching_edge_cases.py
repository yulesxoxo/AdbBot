from adb_bot.cv.matching import TemplateMatcher
from adb_bot.models import ConfidenceValue
from adb_bot.models.template_matching import MatchMode

from .test_image_creator import TestImageCreator


class TestEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_single_pixel_template(self):
        """Test handling of single pixel template."""
        base_image = TestImageCreator.create_solid_color_image(
            100, 100, (128, 128, 128)
        )
        template_image = TestImageCreator.create_solid_color_image(
            1, 1, (128, 128, 128)
        )

        result = TemplateMatcher.match_template(
            base_image, template_image, MatchMode.BEST, ConfidenceValue("90%")
        )

        assert result is not None
        assert result.box.width == 1
        assert result.box.height == 1

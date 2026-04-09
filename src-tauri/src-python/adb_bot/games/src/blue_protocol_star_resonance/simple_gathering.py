import logging
from time import sleep

from adb_bot.decorators import register_command
from adb_bot.exceptions import GameTimeoutError
from adb_bot.models import ConfidenceValue
from adb_bot.models.decorators import GUIMetadata
from adb_bot.models.image_manipulation import CropRegions

from .blue_protocol_star_resonance import BlueProtocolStarResonance


class SimpleGathering(BlueProtocolStarResonance):
    GATHERING_CROP = CropRegions(
        left="60%",
        right="20%",
        top="30%",
        bottom="30%",
    )
    gather_count = 0

    @register_command(
        gui=GUIMetadata(
            label="Simple Gathering",
        ),
        cli_command="BPSR.simple_gathering",
    )
    def entry(self) -> None:
        logging.info("Simple Gathering started!")
        self.close_popups()
        self.show_ui()
        while True:
            self.close_popups()
            self.try_to_gather()
            sleep(1)

    def try_to_gather(self) -> None:
        result = self.find_any_template(
            self.get_templates_from_dir("gathering"),
            threshold=ConfidenceValue("95%"),
            crop_regions=self.GATHERING_CROP,
        )

        if not result:
            return

        self.click(result)
        sleep(0.5)
        try:
            self.wait_until_template_disappears(
                result.template,
                delay=0.1,
                timeout=3,
                crop_regions=self.GATHERING_CROP,
                threshold=ConfidenceValue("95%"),
            )
            template = result.template
            if not template.endswith("_active.png"):
                sleep(0.5)
                self.wait_until_template_disappears(
                    template.replace(".png", "_active.png"),
                    delay=0.1,
                    timeout=5,
                    crop_regions=self.GATHERING_CROP,
                    threshold=ConfidenceValue("95%"),
                )
        except GameTimeoutError:
            return
        self.gather_count += 1
        logging.info(f"Gathered from Spot #{self.gather_count}")
        sleep(0.5)
        return

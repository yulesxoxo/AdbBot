import logging
from abc import ABC
from time import sleep

from adb_bot.device.adb import AdbController, DeviceStream
from adb_bot.exceptions import (
    AutoPlayerUnrecoverableError,
    AutoPlayerWarningError,
    UnsupportedResolutionError,
)
from adb_bot.game.game_base import GameBaseABC
from adb_bot.io import SettingsLoader
from adb_bot.models.device import DisplayInfo


class AndroidGameBaseABC(GameBaseABC, ABC):
    """Abstract class for Android games."""

    def __init__(self) -> None:
        """Initialize a game."""
        self._device: AdbController | None = None
        self._stream: DeviceStream | None = None
        self._target_package_name: str | None = None
        self._start_bot()

    @property
    def device(self) -> AdbController:
        """Get device."""
        if self._device is None:
            self._device = AdbController()
        return self._device

    @property
    def display_info(self) -> DisplayInfo:
        """Resolves and returns DisplayInfo instance."""
        return self.device.get_display_info()

    def _start_stream(self) -> None:
        """Start the device stream."""
        try:
            self._stream = DeviceStream(
                self.device,
            )
        except AutoPlayerWarningError as e:
            logging.warning(f"{e}")

        if self._stream is None:
            return

        self._stream.start()
        time_waiting_for_stream_to_start = 0
        attempts = 10
        while True:
            if time_waiting_for_stream_to_start >= attempts:
                logging.error("Could not start Device Stream using screenshots instead")
                if self._stream:
                    self._stream.stop()
                    self._stream = None
                break
            if self._stream and self._stream.get_latest_frame() is not None:
                logging.debug("Device Stream started")
                break
            sleep(1)
            time_waiting_for_stream_to_start += 1

    def _stop_stream(self):
        """Stop the device stream."""
        if self._stream:
            self._stream.stop()
            self._stream = None

    def _start_bot(self):
        self._setup_device_resolution()
        self._assert_device_display()

        self._setup_device_streaming()
        self._check_screenshot_matches_display_resolution()

    def _setup_device_resolution(self):
        if not SettingsLoader.adb_settings().device.use_wm_resize:
            return

        if not self.base_resolution == self.display_info.normalized_resolution:
            self.device.set_display_size(str(self.base_resolution))
        return

    def _assert_device_display(self) -> None:
        """Validates Device properties such as resolution and orientation.

        Raises:
             UnsupportedResolutionException: Device resolution is not supported.
        """
        current = self.display_info.normalized_resolution
        base = self.base_resolution

        if base == current:
            return

        if (
            base.orientation == self.display_info.orientation
            or base.is_square
            or current.is_square
        ):
            raise UnsupportedResolutionError(
                f"This bot only supports: {base} resolution, detected: {current}"
            )

        orientation_hint = "Portrait" if base.is_portrait else "Landscape"

        raise UnsupportedResolutionError(
            f"This bot only supports: '{base}' resolution ({orientation_hint}), "
            f"detected: '{current}'. "
            "See: https://yulesxoxo.github.io/AdbBot/user-guide/"
            "troubleshoot.html#this-bot-only-works-in-portrait-mode"
        )

    def _setup_device_streaming(self, device_streaming: bool = True) -> None:
        if not device_streaming:
            if self._stream:
                logging.debug("Stopping device streaming")
                self._stream.stop()
            return

        if self._stream:
            logging.debug("Device stream already started")
            return

        if not SettingsLoader.adb_settings().device.streaming:
            logging.warning("Real-time Display Streaming is disabled in ADB Settings")
            if self._stream:
                logging.debug("Stopping device streaming")
                self._stream.stop()
            return

        self._start_stream()
        return

    def _check_screenshot_matches_display_resolution(self) -> None:
        height, width = self.get_screenshot().shape[:2]
        if (width, height) != self.display_info.dimensions:
            if self._stream:
                logging.warning(
                    f"Device Stream resolution ({width}, {height}) "
                    f"does not match Display Resolution {self.display_info}, "
                    "using screenshots as fallback"
                )
                self._stop_stream()
                return
            raise AutoPlayerUnrecoverableError(
                f"Screenshot resolution ({width}, {height}) "
                f"does not match Display Resolution {self.display_info}, "
                f"exiting..."
            )
        return

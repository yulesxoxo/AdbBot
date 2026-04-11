"""Simple ADB Commands."""

from adb_bot.decorators import register_command
from adb_bot.device.adb import AdbController
from adb_bot.ipc import Category
from adb_bot.models.decorators import GUIMetadata


# This command should probably be game specific in the future if there are any games
# that use a different resolution.
@register_command(
    gui=GUIMetadata(
        label="Set Display Size 1080x1920",
        category=Category.SETTINGS_PHONE_DEBUG,
    ),
    cli_command="WMSize1080x1920",
)
def _exec_wm_size_1080_1920():
    AdbController().set_display_size("1080x1920")


@register_command(
    gui=GUIMetadata(
        label="Reset Display Size",
        category=Category.SETTINGS_PHONE_DEBUG,
    ),
    cli_command="WMSizeReset",
)
def _reset_display_size():
    AdbController().reset_display_size()

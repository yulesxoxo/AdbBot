"""ADB Bot Logging Setup Module."""

import logging
import sys
from datetime import datetime
from typing import ClassVar

from adb_bot.util import (
    StringHelper,
    TracebackHelper,
)

from .log_presets import LogPreset


class TerminalLogHandler(logging.Handler):
    """Terminal log handler for logging to the console with colors."""

    LOG_LEVEL_WIDTH: int = 10

    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[94m",  # Blue
        "INFO": "\033[92m",  # Green
        "WARNING": "\033[93m",  # Yellow
        "ERROR": "\033[91m",  # Red
        "CRITICAL": "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset to default
    }

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log message in colored text format.

        Args:
            record (logging.LogRecord): The log record to emit.
        """
        log_level: str = record.levelname

        log_preset: LogPreset | None = getattr(record, "preset", None)

        if log_preset is not None:
            color: str = log_preset.get_terminal_color()
        else:
            color = self.COLORS.get(log_level, self.COLORS["RESET"])

        timestamp: str = datetime.fromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        timestamp_with_ms: str = f"{timestamp}.{int(record.msecs):03d}"

        level_block = f"[{log_level}]".ljust(self.LOG_LEVEL_WIDTH)

        formatted_message: str = (
            f"{color}"
            f"[{timestamp_with_ms}] {level_block} "
            f"{TracebackHelper.format_debug_info(record)} "
            f"{StringHelper.sanitize_path(record.getMessage())}"
            f"{self.COLORS['RESET']}"
        )
        print(formatted_message)
        sys.stdout.flush()


def setup_logging(level: int | str) -> None:
    """Set up logging with specified handler type and level.

    Args:
        level (int | str): The log level to set
    """
    logger: logging.Logger = logging.getLogger()
    logger.setLevel(level)

    for handler in logger.handlers:
        logger.removeHandler(handler)

    logger.addHandler(TerminalLogHandler())

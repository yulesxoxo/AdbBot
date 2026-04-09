"""ADB Bot Command Module."""

from collections.abc import Callable
from typing import Any

from ..decorators import GUIMetadata


class Command:
    """Command class."""

    def __init__(
        self,
        name: str,
        action: Callable,
        kwargs: dict | None = None,
        gui_metadata: GUIMetadata | None = None,
        tooltip: str | None = None,
    ) -> None:
        """Defines a CLI command / GUI Button.

        Args:
            name (str): Command name.
            action (Callable): Function that will be executed for the command.
            kwargs (dict | None): Keyword arguments for the action function.
            gui_metadata (GUIMetadata | None):
                Optional GUI metadata for display in menus.
            tooltip (str | None): Help text used for CLI description and
                when hovering over the button in the GUI.


        Raises:
            ValueError: If name contains whitespace.
        """
        if " " in name:
            raise ValueError(f"Command name '{name}' should not contain spaces.")
        self.name: str = name
        self.action: Callable[..., Any] = action
        self.kwargs: dict[str, str] = kwargs if kwargs is not None else {}
        self.gui_metadata: GUIMetadata | None = gui_metadata
        self.tooltip: str | None = tooltip

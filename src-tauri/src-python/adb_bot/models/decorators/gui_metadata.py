"""GUIMetadata."""

from dataclasses import dataclass
from enum import StrEnum


@dataclass
class GUIMetadata:
    """Metadata used to describe how a command should appear in the GUI.

    Attributes:
        label (str): Default display name for the command in the menu.
        dynamic_label_settings_property (str):
            Settings property from which to derive display name.
        category (str | StrEnum): Category grouping for UI organization.
    """

    label: str
    dynamic_label_settings_property: str | None = None
    category: str | StrEnum | None = None

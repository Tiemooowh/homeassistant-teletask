"""Constants for the KNX integration."""
from enum import Enum
from typing import Final

DOMAIN: Final = "teletask"

class SupportedPlatforms(Enum):
    """Supported platforms."""

    LIGHT = "light"
    SWITCH = "switch"
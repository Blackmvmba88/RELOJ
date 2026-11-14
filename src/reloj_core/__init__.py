"""RELOJ: deterministic parametric watch design core."""

from .models import WatchSpec
from .validation import ValidationIssue, validate_watch
from .geometry import WatchGeometry, calculate_geometry

__all__ = [
    "WatchSpec",
    "ValidationIssue",
    "WatchGeometry",
    "validate_watch",
    "calculate_geometry",
]

__version__ = "0.1.0"

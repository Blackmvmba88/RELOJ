"""Validated, dependency-free data model for a watch concept."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class WatchSpec:
    """A parametric watch concept. All dimensions are expressed in millimetres."""

    name: str = "RELOJ One"
    family: str = "dress"
    case_diameter_mm: float = 40.0
    case_thickness_mm: float = 10.5
    lug_to_lug_mm: float = 47.0
    lug_width_mm: float = 20.0
    bezel_width_mm: float = 2.0
    crystal_thickness_mm: float = 1.5
    water_resistance_m: int = 50
    case_material: str = "316L stainless steel"
    crystal_material: str = "sapphire"
    strap_material: str = "leather"
    movement_type: str = "quartz"
    display: str = "analog"
    dial_color: str = "#111827"
    accent_color: str = "#D4AF37"
    notes: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WatchSpec":
        if not isinstance(payload, dict):
            raise TypeError("Watch specification must be a JSON object.")
        allowed = set(cls.__dataclass_fields__)
        unknown = sorted(set(payload) - allowed)
        if unknown:
            raise ValueError(f"Unknown watch fields: {', '.join(unknown)}")
        return cls(**payload)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

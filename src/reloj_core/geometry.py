"""Transparent first-order geometry calculations for watch concepts."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .models import WatchSpec


@dataclass(frozen=True)
class WatchGeometry:
    dial_opening_diameter_mm: float
    dial_face_area_mm2: float
    case_front_projected_area_mm2: float
    case_envelope_volume_mm3: float
    lug_to_lug_ratio: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def calculate_geometry(spec: WatchSpec) -> WatchGeometry:
    """Calculate nominal envelope metrics; not a manufacturing CAD model."""
    import math

    dial_diameter = spec.case_diameter_mm - (2.0 * spec.bezel_width_mm)
    radius = spec.case_diameter_mm / 2.0
    dial_radius = dial_diameter / 2.0
    return WatchGeometry(
        dial_opening_diameter_mm=round(dial_diameter, 3),
        dial_face_area_mm2=round(math.pi * dial_radius**2, 3),
        case_front_projected_area_mm2=round(math.pi * radius**2, 3),
        case_envelope_volume_mm3=round(
            math.pi * radius**2 * spec.case_thickness_mm, 3
        ),
        lug_to_lug_ratio=round(spec.lug_to_lug_mm / spec.case_diameter_mm, 3),
    )

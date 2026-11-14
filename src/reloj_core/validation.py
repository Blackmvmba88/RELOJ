"""Engineering guardrails for early watch concepts.

These are concept-screening bounds, not manufacturing tolerances or certifications.
"""

from __future__ import annotations

from dataclasses import dataclass

from .models import WatchSpec


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    field: str
    message: str
    severity: str = "error"


ALLOWED_FAMILIES = {"dress", "diver", "pilot", "field", "sport", "minimal", "digital"}
ALLOWED_MOVEMENTS = {"quartz", "automatic", "manual", "solar", "digital"}
ALLOWED_DISPLAYS = {"analog", "digital", "hybrid"}

NUMERIC_RANGES = {
    "case_diameter_mm": (20.0, 60.0, "mm"),
    "case_thickness_mm": (4.0, 25.0, "mm"),
    "lug_to_lug_mm": (25.0, 75.0, "mm"),
    "lug_width_mm": (8.0, 32.0, "mm"),
    "bezel_width_mm": (0.0, 8.0, "mm"),
    "crystal_thickness_mm": (0.5, 5.0, "mm"),
    "water_resistance_m": (0, 1000, "m"),
}


def validate_watch(spec: WatchSpec) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    numeric_ok: set[str] = set()

    for field_name, (minimum, maximum, unit) in NUMERIC_RANGES.items():
        value = getattr(spec, field_name)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            issues.append(ValidationIssue("TYPE", field_name, "Must be numeric."))
        elif not minimum <= value <= maximum:
            issues.append(
                ValidationIssue(
                    "RANGE",
                    field_name,
                    f"Must be between {minimum:g} and {maximum:g} {unit}.",
                )
            )
        else:
            numeric_ok.add(field_name)

    if spec.family not in ALLOWED_FAMILIES:
        issues.append(ValidationIssue("ENUM", "family", "Unsupported watch family."))
    if spec.movement_type not in ALLOWED_MOVEMENTS:
        issues.append(ValidationIssue("ENUM", "movement_type", "Unsupported movement type."))
    if spec.display not in ALLOWED_DISPLAYS:
        issues.append(ValidationIssue("ENUM", "display", "Unsupported display type."))

    if {"lug_to_lug_mm", "case_diameter_mm"} <= numeric_ok:
        if spec.lug_to_lug_mm < spec.case_diameter_mm:
            issues.append(ValidationIssue(
                "PROPORTION", "lug_to_lug_mm",
                "Lug-to-lug length should not be smaller than case diameter.",
            ))
    if {"lug_width_mm", "case_diameter_mm"} <= numeric_ok:
        if spec.lug_width_mm >= spec.case_diameter_mm:
            issues.append(ValidationIssue(
                "PROPORTION", "lug_width_mm",
                "Lug width must be smaller than case diameter.",
            ))
    if {"bezel_width_mm", "case_diameter_mm"} <= numeric_ok:
        if spec.bezel_width_mm * 2 >= spec.case_diameter_mm:
            issues.append(ValidationIssue(
                "PROPORTION", "bezel_width_mm",
                "Bezel leaves no usable dial opening.",
            ))

    if spec.family == "diver" and "water_resistance_m" in numeric_ok:
        if spec.water_resistance_m < 100:
            issues.append(ValidationIssue(
                "DIVER_RATING", "water_resistance_m",
                "Diver concept target is at least 100 m; certification is not implied.",
                "warning",
            ))
    if spec.movement_type == "digital" and spec.display == "analog":
        issues.append(ValidationIssue(
            "MOVEMENT_DISPLAY", "display",
            "A digital movement paired with an analog-only display needs clarification.",
            "warning",
        ))

    for field_name in ("name", "case_material", "crystal_material", "strap_material"):
        if not isinstance(getattr(spec, field_name), str) or not getattr(spec, field_name).strip():
            issues.append(ValidationIssue("REQUIRED", field_name, "Value must be a non-empty string."))

    return issues

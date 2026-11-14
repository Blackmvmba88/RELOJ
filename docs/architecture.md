# RELOJ Core — Architecture v0.1

## Scope

The first executable slice is a deterministic, dependency-free specification engine.
It accepts a JSON watch concept, validates structural and first-order proportion
constraints, and reports nominal envelope geometry.

## Data flow

`JSON → WatchSpec → validation → geometry → JSON report`

- **Models:** immutable dataclass; unknown fields are rejected to catch spelling errors.
- **Validation:** separates blocking errors from design warnings.
- **Geometry:** derives dial opening, projected areas, envelope volume, and lug-to-lug ratio.
- **CLI:** returns exit code 0 for valid concepts, 1 for engineering validation errors,
  and 2 for malformed input.

## Engineering boundaries

- Dimensions are nominal millimetres; water resistance is metres.
- Envelope volume assumes a cylindrical case and is a comparison metric only.
- The current validator is a concept-screening layer, not a manufacturing tolerance stack.
- A diver-family warning does not imply ISO compliance or water-resistance certification.
- No movement performance, pressure, fatigue, sealing, comfort, or manufacturability
  simulation is claimed in this release.

## Next modules

1. CAD adapter with explicit coordinate system and feature tree.
2. Material property catalogue with source and uncertainty fields.
3. Ergonomics model using wrist circumference and lug geometry.
4. Movement interface contracts and power/accuracy models.
5. Image reconstruction with confidence intervals and human review.

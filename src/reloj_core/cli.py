"""Command-line interface for validating and inspecting watch JSON files."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .geometry import calculate_geometry
from .models import WatchSpec
from .validation import validate_watch


def main() -> int:
    parser = argparse.ArgumentParser(prog="reloj", description="RELOJ parametric watch core")
    parser.add_argument("spec", type=Path, help="Path to a watch specification JSON file")
    args = parser.parse_args()

    try:
        payload = json.loads(args.spec.read_text(encoding="utf-8"))
        spec = WatchSpec.from_dict(payload)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(f"Input error: {exc}", file=sys.stderr)
        return 2

    issues = validate_watch(spec)
    errors = [issue for issue in issues if issue.severity == "error"]
    report = {
        "valid": not errors,
        "specification": spec.to_dict(),
        "geometry": calculate_geometry(spec).to_dict() if not errors else None,
        "issues": [issue.__dict__ for issue in issues],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

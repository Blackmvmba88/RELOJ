"""OpenSCAD concept adapter: deterministic geometry, not production-ready CAD."""
from __future__ import annotations

import math
from pathlib import Path

from .models import WatchSpec
from .validation import validate_watch


def _num(value: float) -> str:
    """Stable finite decimal formatting for SCAD numeric literals."""
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError("CAD dimensions must be finite numbers")
    return f"{value:.4f}"


def generate_scad(spec: WatchSpec, *, facets: int = 96) -> str:
    """Return an editable OpenSCAD model in millimetres.

    Coordinate convention: XY is dial plane; Z is case thickness.
    Component shapes are nominal visualization envelopes only.
    """
    issues = [i for i in validate_watch(spec) if i.severity == "error"]
    if issues:
        raise ValueError("Invalid watch: " + "; ".join(f"{i.field}: {i.message}" for i in issues))
    if not isinstance(facets, int) or isinstance(facets, bool) or not 24 <= facets <= 360:
        raise ValueError("facets must be an integer from 24 to 360")
    d = _num(spec.case_diameter_mm)
    h = _num(spec.case_thickness_mm)
    lug_span = _num(spec.lug_to_lug_mm)
    lug_width = _num(spec.lug_width_mm)
    bezel = _num(spec.bezel_width_mm)
    crystal = _num(spec.crystal_thickness_mm)
    # Nominal visualization constants, not engineering tolerance data.
    return f"""// RELOJ parametric concept; units: mm
// No fit, sealing, load, or water-resistance certification is implied.
$fn = {facets};
case_d = {d};
case_h = {h};
lug_span = {lug_span};
lug_width = {lug_width};
bezel_w = {bezel};
crystal_h = {crystal};
dial_d = case_d - 2 * bezel_w;
wall = 1.2; // illustrative only
lug_depth = max(2.0, (lug_span - case_d) / 2);
lug_radius = min(2.2, lug_width / 6);

module case_body() {{
  color([0.70,0.72,0.75])
  difference() {{
    cylinder(d=case_d, h=case_h);
    translate([0,0,case_h*0.55]) cylinder(d=dial_d, h=case_h, center=false);
  }}
}}

module bezel_ring() {{
  color([0.78,0.80,0.82])
  translate([0,0,case_h-1.0])
  difference() {{
    cylinder(d=case_d, h=1.0);
    translate([0,0,-0.1]) cylinder(d=dial_d, h=1.2);
  }}
}}

module dial() {{
  color([0.08,0.10,0.14])
  translate([0,0,case_h*0.55]) cylinder(d=dial_d-0.4, h=0.4);
}}

module crystal() {{
  color([0.65,0.85,0.95,0.35])
  translate([0,0,case_h-0.5]) cylinder(d=dial_d-0.3, h=crystal_h);
}}

module lugs() {{
  color([0.70,0.72,0.75])
  for (side=[-1,1], xside=[-1,1]) {{
    translate([xside*lug_width*0.35,side*(case_d/2+lug_depth/2),case_h*0.30])
      cube([lug_width*0.25,lug_depth+1,case_h*0.45],center=true);
  }}
}}

module indices() {{
  color([0.90,0.75,0.30])
  for (i=[0:11]) {{
    rotate([0,0,i*30])
    translate([0,dial_d*0.40,case_h*0.55+0.45])
      cube([0.7,2.2,0.3],center=true);
  }}
}}

module hands() {{
  color([0.95,0.82,0.40]) {{
    translate([0,4.0,case_h*0.55+0.75]) cube([1.2,8.0,0.35],center=true);
    rotate([0,0,110]) translate([0,5.0,case_h*0.55+0.95])
      cube([0.8,10.0,0.30],center=true);
  }}
}}

module watch_concept() {{
  case_body();
  bezel_ring();
  dial();
  crystal();
  lugs();
  indices();
  hands();
}}
watch_concept();
"""


def export_scad(spec: WatchSpec, output: str | Path, *, facets: int = 96) -> Path:
    """Write a reproducible SCAD source file; STL requires OpenSCAD externally."""
    path = Path(output)
    path.write_text(generate_scad(spec, facets=facets), encoding="utf-8")
    return path

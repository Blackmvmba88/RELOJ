"""Luxury concept module for RELOJ: integrated lugs and selectable parts.

Visualization geometry, not manufacturing or pressure-rated engineering.
"""
from __future__ import annotations

import math
from pathlib import Path

from .models import WatchSpec
from .validation import validate_watch

COMPONENTS = ("assembly", "case", "bezel", "dial", "crystal", "indices", "hands", "crown")
FINISHES = ("obsidian-gold", "titanium-ice", "royal-purple")


def generate_luxury_scad(
    spec: WatchSpec, *, component: str = "assembly",
    finish: str = "obsidian-gold", facets: int = 128,
) -> str:
    """Generate editable concept CAD in millimetres."""
    errors = [i for i in validate_watch(spec) if i.severity == "error"]
    if errors:
        raise ValueError("Invalid specification: " + "; ".join(i.field for i in errors))
    if component not in COMPONENTS:
        raise ValueError(f"Unknown component: {component}")
    if finish not in FINISHES:
        raise ValueError(f"Unknown finish: {finish}")
    if type(facets) is not int or not 32 <= facets <= 360:
        raise ValueError("facets must be an integer from 32 to 360")

    names = ("case_diameter_mm", "case_thickness_mm", "lug_to_lug_mm",
             "lug_width_mm", "bezel_width_mm", "crystal_thickness_mm")
    values = [getattr(spec, name) for name in names]
    if any(type(v) not in (int, float) or not math.isfinite(v) for v in values):
        raise ValueError("Dimensions must be finite numbers")
    d, h, span, strap, bezel, crystal = map(float, values)
    if span < d + 1.0:
        raise ValueError("lug-to-lug span needs at least 1 mm beyond the case diameter")
    if bezel < 0.8 or h < 6.0:
        raise ValueError("Luxury geometry requires a bezel >= 0.8mm and case height >= 6mm")
    if strap > d * 0.65:
        raise ValueError("Lug width exceeds concept envelope")

    palette = {
        "obsidian-gold": ("[0.12,0.13,0.16]", "[0.93,0.72,0.31]", "[0.015,0.020,0.035]"),
        "titanium-ice": ("[0.52,0.57,0.62]", "[0.82,0.88,0.94]", "[0.07,0.12,0.17]"),
        "royal-purple": ("[0.20,0.15,0.29]", "[0.87,0.74,0.50]", "[0.09,0.04,0.16]"),
    }
    metal, accent, dial = palette[finish]

    return f"""// BlackMamba RELOJ luxury concept v0.3 | units: mm
// Conceptual geometry: NOT a manufacturing drawing.
$fn = {facets};
case_d = {d:.4f};
case_h = {h:.4f};
lug_span = {span:.4f};
lug_width = {strap:.4f};
bezel_w = {bezel:.4f};
crystal_h = {crystal:.4f};
dial_d = case_d - 2*bezel_w;
metal_color = {metal};
accent_color = {accent};
dial_color = {dial};
component = "{component}";
dial_z = case_h*0.63;

module case_core() {{
  difference() {{
    cylinder(d=case_d, h=case_h-0.9);
    translate([0,0,dial_z]) cylinder(d=dial_d-0.25, h=case_h+1);
  }}
}}

// Hull bridges overlap the base case and keep each lug pair connected.
module integrated_lugs() {{
  for (side=[-1,1], xside=[-1,1])
    hull() {{
      translate([xside*lug_width*0.31,side*(case_d/2-2.0),case_h*0.38])
        scale([1.55,1.55,2.0]) sphere(r=1.65);
      translate([xside*lug_width*0.34,side*(lug_span/2-1.40),case_h*0.30])
        scale([1.65,1.30,1.35]) sphere(r=1.25);
    }}
}}
module case_and_lugs() {{
  color(metal_color) union() {{ case_core(); integrated_lugs(); }}
}}
module bezel_ring() {{
  color(accent_color)
  translate([0,0,case_h-1.0])
  difference() {{
    cylinder(d=case_d, h=1.0);
    translate([0,0,-0.1]) cylinder(d=dial_d, h=1.2);
  }}
}}
module dial() {{
  color(dial_color) translate([0,0,dial_z])
    cylinder(d=dial_d-0.5, h=0.50);
  color(accent_color) translate([0,0,dial_z+0.51])
    difference() {{
      cylinder(d=dial_d-1.7,h=0.12);
      translate([0,0,-0.1]) cylinder(d=dial_d-2.0,h=0.4);
    }}
}}
module crystal() {{
  color([0.72,0.89,0.98,0.22])
    translate([0,0,case_h-0.42])
      cylinder(d=dial_d-0.35,h=crystal_h);
}}
module indices() {{
  color(accent_color)
  for (i=[0:11])
    rotate([0,0,i*30])
      translate([0,dial_d*0.40,dial_z+0.56])
        cube([i%3==0 ? 1.0 : 0.55,i%3==0 ? 3.0 : 2.2,0.25],center=true);
}}
module hands() {{
  color(accent_color) {{
    translate([0,3.5,dial_z+0.75]) cube([1.25,7.0,0.40],center=true);
    rotate([0,0,112]) translate([0,5.1,dial_z+0.96])
      cube([0.82,10.2,0.30],center=true);
    translate([0,0,dial_z+1.16]) cylinder(d=2.4,h=0.35,center=true);
  }}
}}
module crown() {{
  color(accent_color)
  translate([case_d/2+1.0,0,case_h*0.44])
  rotate([0,90,0])
  union() {{
    cylinder(d=5.6,h=2.2,center=true);
    for(i=[0:23]) rotate([0,0,i*15])
      translate([2.75,0,0]) cube([0.30,0.55,2.25],center=true);
  }}
}}
module assembly() {{
  case_and_lugs(); bezel_ring(); dial(); crystal(); indices(); hands(); crown();
}}
if (component == "assembly") assembly();
else if (component == "case") case_and_lugs();
else if (component == "bezel") bezel_ring();
else if (component == "dial") dial();
else if (component == "crystal") crystal();
else if (component == "indices") indices();
else if (component == "hands") hands();
else if (component == "crown") crown();
"""


def export_luxury_scad(
    spec: WatchSpec, output: str | Path, *, component: str = "assembly",
    finish: str = "obsidian-gold", facets: int = 128,
) -> Path:
    destination = Path(output)
    destination.write_text(
        generate_luxury_scad(spec, component=component, finish=finish, facets=facets),
        encoding="utf-8",
    )
    return destination

# BlackMamba RELOJ — Luxury concept v0.3

First concept: **Obsidian Gold**, a dark architectural case and golden bezel,
indices, hands and crown. Optional palettes: `titanium-ice` and `royal-purple`.

The luxury adapter is intentionally separate from the v0.2 generator.

## Generate the CAD concept

```bash
git switch feature/reloj-luxury-v03
python -m pip install -e .
python -c "from reloj_core.models import WatchSpec; from reloj_core.luxury import export_luxury_scad; export_luxury_scad(WatchSpec(), 'luxury.scad')"
openscad -o luxury.stl luxury.scad
```

For separated meshes (not an assembly with calibrated mechanical mates):

```bash
python -c "from reloj_core.models import WatchSpec; from reloj_core.luxury import export_luxury_scad; export_luxury_scad(WatchSpec(), 'case.scad', component='case')"
openscad -o case.stl case.scad
```

Components: `assembly`, `case`, `bezel`, `dial`, `crystal`,
`indices`, `hands`, `crown`.

## Engineering limitations

The lugs connect using overlapping convex hulls rather than floating rectangular
blocks. These shapes have not been measured for spring-bar retention, strap fit,
manufacturing tolerances or loading. The crown is cosmetic. The crystal, indices,
hands and bezel are illustrative. Assemblies may include overlapping meshes.
Manufacturing feasibility, water resistance, actual materials, STEP/B-Rep
exports, mesh connectivity and mechanical tolerances are not yet validated.

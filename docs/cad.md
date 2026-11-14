# RELOJ CAD adapter v0.2

The first CAD backend generates editable OpenSCAD source from the validated
`WatchSpec` contract. It models a simplified case shell, bezel, dial, crystal,
lugs, hour indices and hands in millimetres.

## Generate

```bash
python -m pip install -e .
python -c "from reloj_core import WatchSpec; from reloj_core.cad import export_scad; export_scad(WatchSpec(), 'watch.scad')"
```

Open `watch.scad` in OpenSCAD. Optionally export an STL:

```bash
openscad -o watch.stl watch.scad
```

The Python adapter does not require OpenSCAD; only rendering and mesh export do.

## Explicit limitations

- All shapes are simplified conceptual envelopes.
- Lug width in this initial adapter is a placement/design parameter, not a
  verified strap-fit dimension; spring-bar holes and tolerances are not modeled.
- The crystal and dial are visualization layers, not sealed assemblies.
- The SCAD union is a visualization solid; individual components are not
  manufacturing-ready parts or validated watertight solids.
- STL loses parametric features and materials. STEP requires a separate B-Rep
  backend, such as FreeCAD/OpenCascade, which is not implemented yet.
- No claims of ISO compliance, water resistance, manufacturability, or strength.

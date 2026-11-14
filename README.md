<p align="center">
  <img src="https://img.shields.io/badge/RELOJ-Intelligent%20Parametric%20Watchmaker-0f766e?style=for-the-badge&logo=watchman&logoColor=white" alt="RELOJ" />
</p>

# ⚙️ RELOJ

> Describe the time you want to wear. RELOJ designs the watch.

<p align="center">
  <img src="https://raw.githubusercontent.com/Blackmvmba88/RELOJ/main/assets/watch-hero.svg" alt="RELOJ concept" />
</p>

## 🌿 Vision

RELOJ is a parametric watch design system that turns a brief, a photo, or a moodboard into a complete watch concept. It does not simply generate a visual; it understands constraints: style, size, material, mechanism, legibility, comfort, and cost.

From a Standard digital watch to a luxury design with complications, RELOJ can move between design spaces with a single idea: the watch must be coherent, wearable, and intentional.

---

## 🧠 What RELOJ does

RELOJ is built around a simple principle:

- Input: text, photo, sketch, or reference image
- Interpretation: detect visual and functional parameters
- Generation: create dial, case, strap, movement logic, and material system
- Variation: produce multiple coherent versions from one concept
- Optimization: adapt to budget, style, and use case

This makes RELOJ more than a generator. It becomes a design engine for watch concepts.

---

## 🛠️ Core product logic

### 1. Parametric design
The system models dimensions, materials, proportions, indices, hands, case profile, and strap geometry as editable variables.

### 2. Visual understanding
Given a photo or reference, RELOJ can infer:

- case diameter and profile
- dial layout
- index style
- bezel presence and shape
- strap type and width
- watch family: sports, dress, diving, pilot, minimalist, luxury

### 3. Intelligent constraints
Each concept is filtered by:

- size / ergonomics
- readability
- aesthetic family
- movement type
- manufacturing viability
- cost level

### 4. Variants, not duplicates
The same design DNA can generate multiple versions:

- standard edition
- luxury edition
- digital edition
- mechanical concept
- premium collector version

---

## 📸 Workflow

```text
Text / image / moodboard
        │
        ▼
  Parse concept
        │
        ▼
  Extract watch parameters
        │
        ▼
  Evaluate style + constraints
        │
        ▼
  Generate watch variants
        │
        ▼
  Render and optimize
```

---

## ✨ Feature set

- Parametric watch generation from prompt
- Photo-to-watch reconstruction pipeline
- Dial, case, and strap generation
- Material and cost logic
- Style family rules
- Luxury and standard design variants
- Complication-oriented concept generation
- Future mechanism and performance simulation

---

## 🧭 Product direction

The project evolves in layers:

### MVP
- watch case generation
- dial concept generator
- strap and material catalog
- photo-inspired reference matching

### Advanced
- movement logic simulation
- power reserve and precision estimation
- comfort and wearability evaluation
- complication concepts

### Premium vision
- tourbillon concept generation
- calendar and perpetual complication modeling
- luxury collector series generation
- fabrication-aware watch design

> The tourbillon is not the first step; it is the horizon of the project.

---

## 🏗️ Why this matters

The world of luxury and fashion watches is full of symbolic language: precision, status, craftsmanship, and identity. RELOJ explores the intersection between design automation and watchmaking culture.

It aims to make the process of watch ideation intelligent, expressive, and scalable.

---

## 🌱 Positioning

RELOJ is not just a watch idea generator.

It is a smart design system for:

- custom luxury watch concepts
- digital and analog product exploration
- brand identity prototyping
- watch design experimentation
- parametric generation of collectible timepieces

---

## 🚀 Roadmap

- [ ] Watch family generation engine
- [ ] Visual prompt-to-watch parser
- [ ] Parametric case and dial model
- [ ] Material and cost logic
- [ ] Variant generation engine
- [ ] Luxury complication concepts
- [ ] Mechanical simulation module

---

## 🕰️ Manifesto

No one chooses a watch from a catalog only because it exists. They wear what tells a story.

RELOJ helps turn that story into shape, proportion, material, and meaning.

> The time you want to wear is not just measured. It is designed.

---

<p align="center">
  <strong>⌚ RELOJ</strong><br>
  Intelligent Parametric Watchmaker
</p>


## 🧪 Executable core — v0.1

The first runnable slice lives in `src/reloj_core`. It turns a JSON concept into a
validated specification and a deterministic geometry report.

### Requirements

- Python 3.11+
- No runtime third-party dependencies

### Run

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
reloj examples/classic-40mm.json
```

Without installing the CLI entry point:

```bash
PYTHONPATH=src python -m reloj_core.cli examples/classic-40mm.json
```

### What is implemented

- Immutable watch specification with strict unknown-field rejection
- Screening validation for dimensions, proportions, family, movement, and display
- Warnings separated from blocking errors
- Derived dial opening, projected area, cylindrical envelope volume, and lug ratio
- JSON CLI report with meaningful exit codes

### Engineering boundary

This is a concept-screening engine, not production CAD. Geometry is first-order and
the cylindrical case volume is only a comparison metric. Water-resistance values are
design inputs, not test results or certification. Movement accuracy, pressure testing,
sealing, comfort, tolerances, and manufacturing validation remain future modules.

See [Core architecture](docs/architecture.md) and the [40 mm example](examples/classic-40mm.json).


## ⌚ Parametric CAD adapter — v0.2

RELOJ now generates deterministic OpenSCAD source from the validated
`WatchSpec` model. The conceptual 3D model includes a case, bezel, dial,
crystal, lugs, indices, and hands.

```bash
python -c "from reloj_core import WatchSpec; from reloj_core.cad import export_scad; export_scad(WatchSpec(), 'watch.scad')"
openscad -o watch.stl watch.scad
```

OpenSCAD is required for the second command, not for generating the source.
See [CAD documentation](docs/cad.md). This is **not** manufacturing CAD:
STEP export, B-Rep solids, tolerances, water resistance, and mechanical
validation remain unimplemented.

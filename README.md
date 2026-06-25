# Wing Box Structural Design

Conceptual structural design of an aircraft wing box and landing gear. The work focuses on load-path reasoning, cross-section sizing, and manufacturing considerations at the early-stage design level — the kind of decisions you make before running FEA.

## What's in here

| Path | Description |
|---|---|
| `report/` | Full LaTeX source for the design report |
| `cad/exports/wingbox_step.stp` | STEP export of the wing box CAD model |
| `geometry/wing_box.stl` | STL of the wing box assembly |
| `geometry/landing_gear.stl` | STL of the landing gear assembly |
| `geometry/generate_stl.py` | Python script that produced the STLs |
| `calculations/wing_box_sizing.md` | Hand calculations: root bending moment, I_xx, bending stress |

## Design summary

**Reference aircraft:** light utility aircraft class (MTOW 1,500 kg, semi-span 5.5 m)

**Structure:** two-spar closed-section wing box in Al 2024-T3

**Critical load case:** positive maneuver at n = +3.8g (per typical normal-category limits)

**Root bending moment:** 152,663 N·m (uniform lift distribution, semi-wing)

**Result from sizing:** 5 mm skins overstress at 454 MPa. Upsize to 8 mm gives 290 MPa, 11% margin against Al 2024-T3 yield (324 MPa).

See [`calculations/wing_box_sizing.md`](calculations/wing_box_sizing.md) for the full working.

## Design decisions

**Two-spar vs multi-spar:** Went with two spars (front at 15% chord, rear at 65% chord). A third spar would improve torsional redundancy but adds manufacturing complexity without a clear structural driver at this load level.

**Skin-stringer vs thick skin:** Simple thick skin without stringers at this stage. Stringers improve buckling resistance but a real design would size the skin/stringer combination together, which is beyond the scope here.

**Material:** Al 2024-T3 over composites. The right baseline for a conceptual study where the goal is load-path reasoning, not weight optimization.

## Limitations

- No FEA: stress distribution is approximate (Euler-Bernoulli beam theory)
- No buckling analysis on the compression skin under +3.8g
- No fatigue assessment
- Internal ribs not modeled
- Landing gear loads not calculated (conceptual geometry only)

## Running the STL generator

```bash
pip install numpy-stl numpy
python geometry/generate_stl.py
```

Outputs `wing_box.stl` and `landing_gear.stl` in `geometry/`. GitHub renders these as interactive 3D models in the browser.

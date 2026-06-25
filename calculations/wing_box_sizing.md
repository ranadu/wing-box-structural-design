# Wing Box Sizing — Hand Calculations

Conceptual bending stress check for the root cross-section under the critical +3.8g maneuver load.
All values are at the wing root, which is the highest bending moment location.

---

## 1. Aircraft Parameters (assumed)

| Parameter | Symbol | Value |
|---|---|---|
| Max take-off weight | MTOW | 1,500 kg |
| Wing semi-span | b/2 | 5.5 m |
| Positive limit load factor | n+ | +3.8 |
| Negative limit load factor | n- | -1.5 |

---

## 2. Wing Box Cross-Section Geometry

Two-spar closed-section box. Spars at 15% and 65% of root chord.

| Dimension | Symbol | Value |
|---|---|---|
| Box width (chord fraction) | b_box | 600 mm |
| Box depth | h_box | 200 mm |
| Upper/lower skin thickness | t_skin | 8 mm |
| Spar web thickness | t_web | 4 mm |
| Inner height (between skins) | h_inner | 184 mm |

Material: **Al 2024-T3**

| Property | Value |
|---|---|
| Young's modulus | E = 73.1 GPa |
| Yield strength | sigma_y = 324 MPa |
| Density | rho = 2,780 kg/m^3 |

---

## 3. Design Load: Root Bending Moment

Total lift at the critical maneuver load:

```
L_total = n+ x MTOW x g
        = 3.8 x 1500 x 9.81
        = 55,917 N
```

Lift per semi-wing (symmetric flight):

```
L_semi = L_total / 2
       = 27,959 N
```

For a uniform spanwise lift distribution, the resultant acts at the mid-span (b/4 from root):

```
M_root = L_semi x (b/2) / 2
       = 27,959 x 2.75
       = 76,887 N·m
```

Note: A real loads analysis would use an elliptical or CFD-derived lift distribution.
An elliptical distribution shifts the centroid inboard, giving a slightly higher root moment.
Treating as uniform here is conservative in the sense that it underestimates the moment
compared to a true structural loads analysis — but acceptable at this stage.

---

## 4. Second Moment of Area (I_xx)

Bending axis is the horizontal centroidal axis. The cross-section is symmetric top/bottom.

### 4.1 Upper and lower skins (parallel axis theorem)

Each skin is a rectangle: b_box x t_skin, centroid at distance (h_box/2 - t_skin/2) from the neutral axis.

```
d_skin = h_box/2 - t_skin/2
       = 100 - 4
       = 96 mm = 0.096 m

I_skin_each = (b_box x t_skin^3)/12 + (b_box x t_skin) x d_skin^2
            = (0.6 x 0.008^3)/12 + (0.6 x 0.008) x 0.096^2
            = 2.56e-9 + 4.424e-5
            = 4.424e-5 m^4  (own term negligible vs. transfer term)

I_skins = 2 x I_skin_each
        = 8.848e-5 m^4
```

### 4.2 Spar webs (two webs, symmetric about neutral axis)

Each web: t_web x h_inner, centred at the neutral axis.

```
I_web_each = (t_web x h_inner^3) / 12
           = (0.004 x 0.184^3) / 12
           = (0.004 x 0.006229) / 12
           = 2.076e-6 m^4

I_webs = 2 x I_web_each
       = 4.153e-6 m^4
```

### 4.3 Total

```
I_xx = I_skins + I_webs
     = 8.848e-5 + 4.153e-6
     = 9.263e-5 m^4
```

---

## 5. Bending Stress Check

The outer fibre of the upper/lower skin is at:

```
y_max = h_box/2 = 0.1 m
```

Bending stress at the extreme fibre:

```
sigma = M_root x y_max / I_xx
      = 76,887 x 0.1 / 9.263e-5
      = 83.0 MPa
```

### Result

| Quantity | Value |
|---|---|
| Root bending moment | 76,887 N·m |
| I_xx | 9.263e-5 m^4 |
| Peak bending stress (outer fibre) | 83.0 MPa |
| Al 2024-T3 yield strength | 324 MPa |
| Margin (yield) | 74% |

The 8 mm skins give a healthy margin at this load level. This is expected for a
conceptual design — the section geometry was not optimized to minimize weight.

---

## 6. Why 5 mm Skins Don't Work

Running the same calc with t_skin = 5 mm:

```
d_skin = 100 - 2.5 = 97.5 mm = 0.0975 m

I_skin_each = (0.6 x 0.005) x 0.0975^2 = 2.852e-5 m^4
I_skins = 5.703e-5 m^4

I_web_each = (0.004 x 0.190^3) / 12 = 2.286e-6 m^4
I_webs = 4.572e-6 m^4

I_xx = 6.160e-5 m^4

sigma = 76,887 x 0.0975 / 6.160e-5 = 121.7 MPa
```

Still within yield at this load level, but the margin drops to 62%.
The 8 mm choice was driven by wanting sufficient margin against the
ultimate load case (limit x 1.5 safety factor), and to leave headroom
for the skin buckling consideration not covered in this analysis.

---

## 7. What This Analysis Doesn't Cover

- **Skin buckling:** under +3.8g, the upper skin is in compression. A thin skin
  can buckle locally before reaching yield stress. This would require a buckling
  stability check (either Euler column analogy or a finite element model).
  This is probably the most important gap in this analysis.

- **Shear stress in spar webs:** the webs carry the transverse shear. A shear
  flow calculation (Bredt-Batho for closed sections) would give the shear stress
  in the webs and help size t_web.

- **Torsional stiffness:** the closed box resists torque via the Bredt-Batho
  shear flow. This wasn't sized here because torsional loads were not defined.

- **Root attachment:** the highest stress concentration will be at the spar-to-fuselage
  attachment fitting, which isn't modeled.

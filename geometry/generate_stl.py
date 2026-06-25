"""
generate_stl.py
Generates wing_box.stl and landing_gear.stl from parametric geometry.
Run: python generate_stl.py
Outputs two STL files in the same directory (renders as 3D models on GitHub).
"""

import numpy as np
from stl import mesh
from pathlib import Path

OUT = Path(__file__).parent


# ── helpers ───────────────────────────────────────────────────────────────────

def box_mesh(ox, oy, oz, w, h, d):
    """Return a solid box mesh. Origin at (ox,oy,oz), dimensions w x h x d (mm)."""
    v = np.array([
        [ox,   oy,   oz  ],
        [ox+w, oy,   oz  ],
        [ox+w, oy+h, oz  ],
        [ox,   oy+h, oz  ],
        [ox,   oy,   oz+d],
        [ox+w, oy,   oz+d],
        [ox+w, oy+h, oz+d],
        [ox,   oy+h, oz+d],
    ], dtype=float)
    faces = np.array([
        [0,2,1],[0,3,2],  # -z face
        [4,5,6],[4,6,7],  # +z face
        [0,1,5],[0,5,4],  # -y face
        [2,3,7],[2,7,6],  # +y face
        [0,4,7],[0,7,3],  # -x face
        [1,2,6],[1,6,5],  # +x face
    ])
    m = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            m.vectors[i][j] = v[f[j]]
    return m


def cylinder_mesh(cx, cy, oz, r, h, n_seg=32):
    """Return a closed cylinder mesh. Centre at (cx,cy), bottom at oz, height h."""
    angles = np.linspace(0, 2*np.pi, n_seg, endpoint=False)
    vbot = np.array([[cx + r*np.cos(a), cy + r*np.sin(a), oz]      for a in angles])
    vtop = np.array([[cx + r*np.cos(a), cy + r*np.sin(a), oz+h]    for a in angles])
    cbot = np.array([cx, cy, oz])
    ctop = np.array([cx, cy, oz+h])

    tris = []
    for i in range(n_seg):
        j = (i+1) % n_seg
        # side quads
        tris += [[vbot[i], vbot[j], vtop[i]], [vtop[i], vbot[j], vtop[j]]]
        # caps
        tris += [[cbot, vbot[j], vbot[i]], [ctop, vtop[i], vtop[j]]]

    m = mesh.Mesh(np.zeros(len(tris), dtype=mesh.Mesh.dtype))
    for i, t in enumerate(tris):
        for j in range(3):
            m.vectors[i][j] = np.array(t[j], dtype=float)
    return m


def combine(*meshes):
    combined = mesh.Mesh(np.concatenate([m.data for m in meshes]))
    return combined


# ── wing box geometry (all dimensions in mm) ──────────────────────────────────
#
#   Two-spar closed box section representing a root segment.
#   x = spanwise (along wing), y = chordwise, z = vertical (depth)
#
#   L  = 2000 mm  spanwise length of section
#   W  = 600 mm   chordwise width
#   H  = 200 mm   box depth
#   ts = 8 mm     skin thickness
#   tw = 4 mm     spar web thickness
#   Spar 1 at y = 90 mm  (15% of 600)
#   Spar 2 at y = 390 mm (65% of 600)

L, W, H, ts, tw = 2000, 600, 200, 8, 4
h_inner = H - 2*ts   # 184 mm

upper_skin  = box_mesh(0,   0, H-ts, L, W,     ts)
lower_skin  = box_mesh(0,   0, 0,    L, W,     ts)
front_spar  = box_mesh(0,  90, ts,   L, tw,  h_inner)
rear_spar   = box_mesh(0, 390, ts,   L, tw,  h_inner)

wing_box = combine(upper_skin, lower_skin, front_spar, rear_spar)
wing_box.save(str(OUT / "wing_box.stl"))
print("Saved wing_box.stl")


# ── landing gear geometry (mm) ────────────────────────────────────────────────
#
#   Main strut: rectangular section, 80x80x500 mm
#   Wheel hub:  cylinder, r=100 mm, width=60 mm, centred on strut

strut       = box_mesh(-40, -40, 0, 80, 80, 500)
wheel_hub   = cylinder_mesh(0, 0, 510, 100, 60)
axle        = cylinder_mesh(0, 0, 490, 15,  80)

landing_gear = combine(strut, wheel_hub, axle)
landing_gear.save(str(OUT / "landing_gear.stl"))
print("Saved landing_gear.stl")

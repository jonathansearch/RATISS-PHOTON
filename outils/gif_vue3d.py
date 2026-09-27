#!/usr/bin/env python3
"""GIF VUE 3D — rendu PAR PLOTLY/KALEIDO (le moteur officiel de Plotly).

Apres la decision C2 (fini le fait-main), ce GIF est produit par le meme
outil que la vue interactive : la scene Plotly de exporter_vue3d.py,
photographiée sous 40 angles de camera par kaleido (moteur de rendu
statique officiel de Plotly), puis assemblee en GIF.

Usage : python3 outils/gif_vue3d.py   → assets/vue3d.gif (pour le README)
"""
from __future__ import annotations

import pathlib

import numpy as np
import plotly.graph_objects as go

RACINE = pathlib.Path(__file__).resolve().parent.parent
AS = RACINE / "assets"
AS.mkdir(exist_ok=True)

# ---- la meme scene que exporter_vue3d.py (source unique de verite) ----------
pile = np.load(RACINE / "champs" / "pile_reference.npy").astype(complex)
zs = np.load(RACINE / "champs" / "pile_reference_z.npy")
pile = pile[::2, ::2]
amp = np.abs(pile)
amp = amp / amp.max()
phase = np.angle(pile)
NY_PTS = pile.shape[1]

y = np.linspace(-0.5, 0.5, NY_PTS)
z_world = (zs - (zs[0] + zs[-1]) / 2) / (zs[-1] - zs[0]) * 3.2
Zg, Yg = np.meshgrid(z_world, y, indexing="ij")

colorsphase = [
    [0.00, "rgb(6, 8, 19)"], [0.20, "rgb(10, 60, 120)"],
    [0.42, "rgb(20, 150, 200)"], [0.62, "rgb(45, 212, 191)"],
    [0.80, "rgb(45, 212, 191)"], [1.00, "rgb(153, 246, 228)"],
]

fig = go.Figure()
fig.add_trace(go.Surface(
    x=Zg, y=Yg, z=amp * 0.45, surfacecolor=phase, cmin=-np.pi, cmax=np.pi,
    colorscale=colorsphase, showscale=False,
    lighting=dict(ambient=0.85, diffuse=0.5, specular=0.15, roughness=0.9),
    lightposition=dict(x=1, y=0, z=3), hoverinfo="skip", showlegend=False,
))
I_ecran = amp[-1]
fig.add_trace(go.Scatter3d(
    x=np.full(NY_PTS, z_world[-1]), y=y, z=I_ecran * 0.45 * 1.05 + 0.005,
    mode="lines", line=dict(color="#7df9ff", width=9), hoverinfo="skip", showlegend=False,
))
zf = (360 - (zs[0] + zs[-1]) / 2) / (zs[-1] - zs[0]) * 3.2
for (a, b) in [(-0.5, -78 / 320), (-42 / 320, 42 / 320), (78 / 320, 0.5)]:
    fig.add_trace(go.Scatter3d(x=[zf, zf], y=[a, b], z=[0, 0], mode="lines",
                               line=dict(color="#f1f5f9", width=7), hoverinfo="skip", showlegend=False))
zp = (640 - (zs[0] + zs[-1]) / 2) / (zs[-1] - zs[0]) * 3.2
fig.add_trace(go.Scatter3d(x=[zp, zp], y=[-30 / 320, 30 / 320], z=[0, 0], mode="lines",
                           line=dict(color="#fbbf24", width=10), hoverinfo="skip", showlegend=False))

fig.update_layout(
    title=dict(
        text="<b>RATISS-PHOTON · hauteur = |ψ(z,y)|² · couleur = phase</b>"
             "<br><sup>un photon unique · deux fentes · 8 396 800 chemins · données scellées · calcul (RATISS)</sup>",
        font=dict(color="#99f6e4", size=17, family="Georgia"), x=0.5,
    ),
    paper_bgcolor="#060813",
    scene=dict(
        bgcolor="#0a1024",
        xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
        aspectmode="manual", aspectratio=dict(x=2.3, y=0.9, z=0.65),
    ),
    margin=dict(l=0, r=0, t=90, b=10),
    width=980, height=640,
)

# ---- les 40 angles de camera, rendus par kaleido ----------------------------
from PIL import Image  # noqa: E402

N_FRAMES = 40
cadres = []
for k in range(N_FRAMES):
    az = -65 + 26 * np.sin(2 * np.pi * k / N_FRAMES)
    el = 21 + 6 * np.sin(4 * np.pi * k / N_FRAMES)
    cam = dict(eye=dict(x=1.80 * np.cos(np.radians(az)) * np.cos(np.radians(el)),
                        y=1.80 * np.sin(np.radians(az)) * np.cos(np.radians(el)),
                        z=0.80))
    fig.update_layout(scene_camera=cam)
    png = fig.to_image(format="png", scale=1)   # kaleido : rendu officiel
    cadres.append(Image.open(__import__("io").BytesIO(png)))
    print(f"\r  rendu kaleido {k + 1}/{N_FRAMES}", end="")
print()

# ---- assemblage GIF ----------------------------------------------------------
durations = [70] * N_FRAMES
cadres[0].save(AS / "vue3d.gif", save_all=True, append_images=cadres[1:],
               duration=durations, loop=0, optimize=True)
print(f"assets/vue3d.gif écrit ({(AS / 'vue3d.gif').stat().st_size // 1024} Ko, "
      f"{N_FRAMES} angles, rendu Plotly/kaleido)")

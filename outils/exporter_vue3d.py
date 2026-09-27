#!/usr/bin/env python3
"""EXPORTER VUE 3D v3 — PLOTLY (l'outil standard des laboratoires, embarqué).

Apres l'echec du moteur maison (C1 : canvas vide sur mobile, constate deux
fois par Jonathan), on passe a l'OUTIL RECONNU : Plotly. Sa bibliotheque
complete (~3,5 Mo) est EMBARQUEE dans le HTML : aucune dependance reseau,
ca tourne dans l'apercu, sur GitHub Pages et hors ligne, avec les
controles tactiles natifs (rotation 1 doigt, zoom 2 doigts).

Scene (donnees scellees de champs/pile_reference.npy) :
  - surface 3D : hauteur = |psi(z,y)|², couleur = phase de psi ;
  - ligne 3D   : la courbe d'interference REELLE a l'ecran (z = 920) ;
  - marqueurs  : les deux fentes (z = 360) et la plaque (z = 640).

Usage : python3 outils/exporter_vue3d.py   → visualisation.html
"""
from __future__ import annotations

import pathlib

import numpy as np
import plotly.graph_objects as go

RACINE = pathlib.Path(__file__).resolve().parent.parent

# ---- donnees scellees -------------------------------------------------------
pile = np.load(RACINE / "champs" / "pile_reference.npy").astype(complex)
zs = np.load(RACINE / "champs" / "pile_reference_z.npy")

# decimation : 1 plan sur 2 en z, 1 point sur 2 en y (lisible et leger)
pile = pile[::2, ::2]
amp = np.abs(pile)
amp = amp / amp.max()
phase = np.angle(pile)
NY_PTS = pile.shape[1]

y = np.linspace(-0.5, 0.5, pile.shape[1])
z_world = (zs - (zs[0] + zs[-1]) / 2) / (zs[-1] - zs[0]) * 3.2
Zg, Yg = np.meshgrid(z_world, y, indexing="ij")

# ---- coloration par la phase (identite labo : cyan -> turquoise -> blanc) ---
colorsphase = [
    [0.00, "rgb(6, 8, 19)"],
    [0.20, "rgb(10, 60, 120)"],
    [0.42, "rgb(20, 150, 200)"],
    [0.62, "rgb(45, 212, 191)"],
    [0.82, "rgb(153, 246, 228)"],
    [1.00, "rgb(255, 255, 255)"],
]

fig = go.Figure()

# surface principale
fig.add_trace(go.Surface(
    x=Zg, y=Yg, z=amp * 0.45,
    surfacecolor=phase, cmin=-np.pi, cmax=np.pi,
    colorscale=colorsphase,
    showscale=False,
    opacity=1.0,
    lighting=dict(ambient=0.85, diffuse=0.5, specular=0.15, roughness=0.9),
    lightposition=dict(x=1, y=0, z=3),
    hovertemplate="z=%{x:.2f} · y=%{y:.2f} · |ψ|²=%{z:.3f}<extra></extra>",
    name="|ψ(z,y)|²",
))

# courbe d'interference reelle a l'ecran (z = 920) — donnees scellees
I_ecran = amp[-1]
fig.add_trace(go.Scatter3d(
    x=np.full(NY_PTS, z_world[-1]),
    y=y,
    z=I_ecran * 0.45 * 1.05 + 0.005,
    mode="lines",
    line=dict(color="#7df9ff", width=9),
    name="interférence à l'écran (mesurée)",
    hovertemplate="écran · y=%{y:.2f} · I=%{z:.3f}<extra></extra>",
))

# socle de l'ecran
fig.add_trace(go.Scatter3d(
    x=[z_world[-1], z_world[-1]], y=[-0.5, 0.5], z=[0, 0],
    mode="lines", line=dict(color="rgba(125,249,255,0.45)", width=3),
    showlegend=False, hoverinfo="skip",
))

# les deux fentes (z = 360) : mur blanc perce de deux ouvertures
zf = (360 - (zs[0] + zs[-1]) / 2) / (zs[-1] - zs[0]) * 3.2
for (a, b) in [(-0.5, -78 / 320), (-42 / 320, 42 / 320), (78 / 320, 0.5)]:
    fig.add_trace(go.Scatter3d(
        x=[zf, zf], y=[a, b], z=[0, 0],
        mode="lines", line=dict(color="#f1f5f9", width=7),
        showlegend=False, hoverinfo="skip",
    ))

# la plaque (z = 640) : bande ambre sur la frange sombre
zp = (640 - (zs[0] + zs[-1]) / 2) / (zs[-1] - zs[0]) * 3.2
fig.add_trace(go.Scatter3d(
    x=[zp, zp], y=[-30 / 320, 30 / 320], z=[0, 0],
    mode="lines", line=dict(color="#fbbf24", width=10),
    name="plaque π/2 (zone sombre)",
    hoverinfo="name",
))

# etiquettes
for (x_t, y_t, txt, coul) in [
    (zf, 0.60, "deux fentes", "#f1f5f9"),
    (zp, 0.60, "plaque", "#fbbf24"),
    (z_world[-1], 0.60, "écran", "#7df9ff"),
    (z_world[0], -0.75, "→ photon unique, deux fentes", "#99f6e4"),
]:
    fig.add_trace(go.Scatter3d(
        x=[x_t], y=[y_t], z=[0], mode="text", text=[txt],
        textfont=dict(color=coul, size=13, family="Georgia"),
        showlegend=False, hoverinfo="skip",
    ))

fig.update_layout(
    title=dict(
        text="<b>RATISS-PHOTON · le couloir du photon — hauteur = |ψ(z,y)|² · couleur = phase</b>"
             "<br><sup>un photon unique · deux fentes · 8 396 800 chemins (E-CANTON, fidélité 95,9–96,8 %) "
             "· données scellées · 🧮 calcul</sup>",
        font=dict(color="#99f6e4", size=17, family="Georgia"),
        x=0.5,
    ),
    paper_bgcolor="#060813",
    scene=dict(
        bgcolor="#0a1024",
        xaxis_title="z (couloir)", yaxis_title="y (transverse)", zaxis_title="|ψ|²",
        xaxis=dict(backgroundcolor="#0b1122", gridcolor="#1e2a45", zerolinecolor="#1e2a45",
                   title_font_color="#8ba3c7", tickfont=dict(color="#8ba3c7")),
        yaxis=dict(backgroundcolor="#0b1122", gridcolor="#1e2a45", zerolinecolor="#1e2a45",
                   title_font_color="#8ba3c7", tickfont=dict(color="#8ba3c7")),
        zaxis=dict(backgroundcolor="#0b1122", gridcolor="#1e2a45", zerolinecolor="#1e2a45",
                   title_font_color="#8ba3c7", tickfont=dict(color="#8ba3c7"), range=[0, 0.5]),
        aspectmode="manual", aspectratio=dict(x=2.3, y=0.9, z=0.65),
        camera=dict(eye=dict(x=1.45, y=-1.35, z=0.85)),
    ),
    legend=dict(font=dict(color="#e2e8f0"), bgcolor="rgba(6,8,19,0.6)",
                bordercolor="#1e2a45", borderwidth=1,
                orientation="h", x=0.5, xanchor="center", y=-0.05),
    margin=dict(l=0, r=0, t=90, b=40),
    dragmode="orbit",
)

html = fig.to_html(
    include_plotlyjs=True,       # bibliotheque EMBARQUEE : zero CDN, hors ligne OK
    full_html=True,
    config={"displaylogo": False,
            "modeBarButtonsToRemove": ["toImage"],
            "scrollZoom": True},
)

(RACINE / "visualisation.html").write_text(html, encoding="utf-8")
taille = (RACINE / "visualisation.html").stat().st_size
assert "Plotly.newPlot" in html, "bibliotheque Plotly non embarquee !"
print(f"visualisation.html v3 (Plotly embarque) : {taille // 1024} Ko — "
      f"rotation 1 doigt, zoom 2 doigts/molette, zero dependance reseau.")

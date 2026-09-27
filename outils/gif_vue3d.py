#!/usr/bin/env python3
"""GIF VUE 3D — animation de préview pour le README (depuis les données scellées).

Le README GitHub n'execute pas de JavaScript : ce GIF montre la surface
hauteur = |psi(z,y)|², couleur = phase, qui pivote. La version INTERACTIVE
(vue 3D JS pur) est hebergee via GitHub Pages — voir README.

Usage : python3 outils/gif_vue3d.py   → assets/vue3d.gif
"""
from __future__ import annotations

import pathlib

import numpy as np

RACINE = pathlib.Path(__file__).resolve().parent.parent
CH = RACINE / "champs"
AS = RACINE / "assets"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402
from matplotlib.colors import hsv_to_rgb  # noqa: E402

FOND, PANNEAU = "#060813", "#0b1122"

pile = np.load(CH / "pile_reference.npy").astype(complex)
zs = np.load(CH / "pile_reference_z.npy")

# decimation + cadrage sur la zone d'interference (apres les fentes)
sel = zs >= 340
pile = pile[sel][::2, ::2]
zs = zs[sel]
amp = np.abs(pile)
amp = amp / amp.max()
phase = np.angle(pile)

NZ, NY = amp.shape
z = (zs[::2] - zs[::2].mean())
y = np.arange(NY) - NY // 2
Zg, Yg = np.meshgrid(z, y, indexing="ij")

# facecolors : phase -> teinte (cyan-turquoise), amplitude -> luminosite
hue = (phase + np.pi) / (2 * np.pi)
hsv = np.zeros(hue.shape + (3,))
hsv[..., 0] = 0.48 + 0.08 * np.sin(2 * np.pi * hue)   # autour du cyan
hsv[..., 1] = 0.85
hsv[..., 2] = np.clip(0.25 + 1.6 * amp, 0, 1)
face = hsv_to_rgb(hsv)
face = np.repeat(face, 2, axis=0)[:-1, :, :]
face = np.repeat(face, 2, axis=1)[:, :-1, :]
hmax = 120

plt.rcParams.update({"figure.facecolor": FOND, "savefig.facecolor": FOND,
                     "text.color": "#e2e8f0", "axes.labelcolor": "#8ba3c7"})
fig = plt.figure(figsize=(7.2, 4.6), dpi=90)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor(PANNEAU)   # le patch 3D : sinon rectangle blanc par defaut
surf = ax.plot_surface(Zg, Yg, amp * hmax, facecolors=face, rstride=1, cstride=1,
                       linewidth=0, antialiased=False, shade=False)
ax.set_zlim(0, hmax)
ax.set_xlim(z.min(), z.max())
ax.set_ylim(-NY / 2, NY / 2)
ax.set_axis_off()
ax.view_init(elev=28, azim=-55)
fig.text(0.5, 0.94, "RATISS-PHOTON · hauteur = |ψ(z,y)|² · couleur = phase",
         ha="center", fontsize=11, color="#99f6e4", fontweight="bold")
fig.text(0.5, 0.045, "un photon unique · deux fentes · version interactive : visualisation.html",
         ha="center", fontsize=8, color="#8ba3c7")


def update(angle):
    ax.view_init(elev=24 + 8 * np.sin(angle * 0.7), azim=-40 + 70 * np.sin(angle))
    return []


anim = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 48), interval=90)
anim.save(AS / "vue3d.gif", writer=PillowWriter(fps=12), savefig_kwargs={"facecolor": FOND})
print(f"assets/vue3d.gif écrit ({(AS / 'vue3d.gif').stat().st_size // 1024} Ko)")

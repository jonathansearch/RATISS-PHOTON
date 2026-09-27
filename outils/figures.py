#!/usr/bin/env python3
"""FIGURES — RATISS-PHOTON : toutes les figures du README, régénérées ici.

R7 appliqué au pixel : chaque courbe vient de resultats/*.json ou champs/*.npy.
Usage : python3 outils/figures.py   → assets/fig_*.png
Dépendances : numpy + matplotlib.
"""
from __future__ import annotations

import json
import pathlib

import numpy as np

RACINE = pathlib.Path(__file__).resolve().parent.parent
RES = RACINE / "resultats"
CH = RACINE / "champs"
AS = RACINE / "assets"

FOND, PANNEAU, GRILLE = "#060813", "#0b1122", "#1e2a45"
TEXTE, MUTED, BLANC = "#e2e8f0", "#8ba3c7", "#f1f5f9"
TURQ, CYAN, MENTHE = "#2dd4bf", "#38bdf8", "#99f6e4"
VERT, ROUGE, AMBRE = "#4ade80", "#f87171", "#fbbf24"


def style():
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.facecolor": FOND, "axes.facecolor": PANNEAU, "savefig.facecolor": FOND,
        "axes.edgecolor": GRILLE, "axes.labelcolor": TEXTE, "axes.titlecolor": BLANC,
        "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TEXTE,
        "grid.color": GRILLE, "font.size": 10, "axes.titlesize": 11,
        "axes.titleweight": "bold", "legend.facecolor": PANNEAU, "legend.edgecolor": GRILLE,
    })
    return plt


def fig(plt, nc, nr, titre, w=13.6, h=5.0):
    f, ax = plt.subplots(nr, nc, layout="constrained", figsize=(w, h))
    f.get_layout_engine().set(rect=(0, 0.032, 1, 0.968))
    f.suptitle(titre, color=BLANC, fontsize=12.5, fontweight="bold")
    return f, ax


def pied(plt, f, src):
    f.text(0.995, 0.008, f"RATISS Labs · RATISS-PHOTON · 27/09/2026 · calcul — données : {src}",
           ha="right", va="bottom", fontsize=7.5, color=MUTED)


def charge(nom):
    return json.load(open(RES / nom, encoding="utf-8"))


def main():
    plt = style()
    AS.mkdir(exist_ok=True)
    y = (np.arange(320) - 160)

    # ============ 1 · LE COULOIR (carte |psi|^2 dans le plan z,y) ============
    pile = np.load(CH / "pile_reference.npy")
    zs = np.load(CH / "pile_reference_z.npy")
    dens = np.abs(pile) ** 2
    dens /= dens.max()
    f, a = fig(plt, 1, 1, "RATISS-PHOTON · le couloir — un photon, deux fentes, le champ reconstruit |ψ(z,y)|²",
               w=13.6, h=4.6)
    im = a.pcolormesh(zs, y, dens.T, cmap="turbo", shading="auto", vmin=0, vmax=0.55)
    for z0, nom, coul in [(360, "fentes", BLANC), (640, "plaque (E-F1)", AMBRE), (920, "écran", VERT)]:
        a.axvline(z0, color=coul, lw=1.0, ls="--", alpha=0.8)
        a.text(z0 + 6, -152, nom, color=coul, fontsize=8.5, rotation=90, va="bottom")
    for s in range(400, 901, 100):
        a.axvline(s, color=MUTED, lw=0.4, alpha=0.4)
    f.colorbar(im, ax=a, label="|ψ|² (norm.)", pad=0.01)
    a.set_xlabel("z — axe du couloir (px)")
    a.set_ylabel("y — axe transverse (px)")
    a.set_title("interférences visibles dès la sortie des fentes · stations tous les 100 px en traits fins")
    pied(plt, f, "champs/pile_reference.npy")
    f.savefig(AS / "fig_couloir.png", dpi=150)
    plt.close(f)

    # ============ 2 · E-CANTON : chemins vs ondes ============
    d = charge("ec_canton.json")
    pile_1f = np.load(CH / "pile_1fente.npy")
    # profils ecran reconstitues depuis les amplitudes stockees ? on relit via le run :
    # (les intensites de chemins ne sont pas stockees -> on recalcule les sommes, rapide)
    import sys
    sys.path.insert(0, str(RACINE / "outils"))
    import photom as ph
    col = None
    psi = ph.source()
    psi = ph.avance_libre(psi, ph.Z_FENTES)
    psi *= ph.transmission_fentes(2)
    col = psi.copy()
    psi_ang = ph.spectre_angulaire(col, ph.Z_ECRAN - ph.Z_FENTES)
    psi_cp, _ = ph.somme_chemins_2plans(y, champ_a=col, action="paraxiale")
    psi_cg, _ = ph.somme_chemins_2plans(y, champ_a=col, action="geometrique")
    psi_3p, _ = ph.somme_chemins_3plans(y, col, action="paraxiale")
    f, ax = fig(plt, 1, 2, "E-CANTON · reproduction de Wen et al. — les chemins retrouvent les ondes",
                w=13.6, h=4.8)
    a = ax[0]
    sup = np.abs(y) <= 120
    a.plot(y[sup], np.abs(psi_ang)[sup] ** 2 / np.abs(psi_ang[sup]) ** 2 .max() if False else
           (np.abs(psi_ang[sup]) ** 2) / (np.abs(psi_ang[sup]) ** 2).max(),
           color=BLANC, lw=1.6, label=f"instrument indépendant (spectre angulaire) — contrôle {d['controle_instruments']['correlation_spectral_vs_spectre_angulaire']*100:.1f} %")
    a.plot(y[sup], (np.abs(psi_cp[sup]) ** 2) / (np.abs(psi_cp[sup]) ** 2).max(),
           color=TURQ, lw=1.2, ls="--",
           label=f"somme de chemins, action du monde — fidélité {d['postulat_1_probabilites_par_superposition']['action_du_monde_paraxiale']['fidelite_amplitude_vs_independant']*100:.1f} %")
    a.plot(y[sup], (np.abs(psi_cg[sup]) ** 2) / (np.abs(psi_cg[sup]) ** 2).max(),
           color=AMBRE, lw=1.0, ls=":",
           label=f"action naïve k0×distance — {d['postulat_1_probabilites_par_superposition']['action_naive_geometrique_k0_fois_distance']['fidelite_amplitude_vs_independant']*100:.1f} %")
    a.set_xlabel("y à l'écran (px)")
    a.set_ylabel("intensité (norm.)")
    a.set_title("postulat 1 · la probabilité émerge de la somme cohérente")
    a.legend(fontsize=7.6, loc="upper right")
    a.grid(alpha=0.5)
    a = ax[1]
    barres = ["3 plans\n(Canton, 8,4 M chemins)", "2 plans\naction du monde", "2 plans\naction naïve",
              "contrôle\nspéctral↔angulaire"]
    vals = [d["fidelite_3_plans_vs_independant"] * 100,
            d["postulat_1_probabilites_par_superposition"]["action_du_monde_paraxiale"]["fidelite_amplitude_vs_independant"] * 100,
            d["postulat_1_probabilites_par_superposition"]["action_naive_geometrique_k0_fois_distance"]["fidelite_amplitude_vs_independant"] * 100,
            d["controle_instruments"]["correlation_spectral_vs_spectre_angulaire"] * 100]
    couls = [TURQ, CYAN, AMBRE, MUTED]
    b = a.bar(barres, vals, color=couls, edgecolor=BLANC, linewidth=0.6)
    a.axhspan(95, 98.5, color=VERT, alpha=0.15)
    a.text(1.5, 96.9, "fenêtre de Canton : 95 – 98,5 %", color=VERT, fontsize=8.5, ha="center")
    for bi, v in zip(b, vals):
        a.text(bi.get_x() + bi.get_width() / 2, v + 0.4, f"{v:.1f} %", ha="center", color=BLANC, fontsize=9, fontweight="bold")
    a.set_ylim(88, 101)
    a.set_ylabel("fidélité / corrélation (%)")
    a.set_title("toutes les reconstructions tombent dans la fenêtre de Canton")
    a.grid(alpha=0.5, axis="y")
    pied(plt, f, "resultats/ec_canton.json")
    f.savefig(AS / "fig_ec_canton.png", dpi=150)
    plt.close(f)

    # ============ 3 · E-F3 : le hasard vient du bain ============
    d3 = charge("ef3.json")
    f, ax = fig(plt, 1, 2, "E-F3 · le hasard vient-il du bain thermique ? — AUCUN tirage de Born câblé",
                w=13.6, h=4.8)
    a = ax[0]
    Ts = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0]
    pear = [d3["pearson_hist_vs_reference"][f"T_{t}"] for t in Ts]
    uniq = [d3["impacts"][f"T_{t}"]["impacts_uniques"] for t in Ts]
    a.plot(Ts, pear, "o-", color=TURQ, lw=1.8, mec=BLANC)
    a.axvline(1.0, color=BLANC, ls="--", lw=0.9, alpha=0.7)
    a.text(1.05, 0.35, "T ambiante\n(300 K)", color=BLANC, fontsize=8.5)
    a.set_xlabel("T / 300 K — agitation du détecteur")
    a.set_ylabel("Pearson r (histogramme d'impacts vs |ψ|²)")
    a.set_title("la statistique de Born ÉMERGE du bain, puis se noie dans le bruit")
    a.grid(alpha=0.5)
    a = ax[1]
    I_screen = np.array(d3["impacts"]["T_1.0"]["histogramme"], dtype=float)
    ref = np.load(CH / "pile_reference.npy")[-1]  # dernier plan... fallback :
    a.bar(y, I_screen / I_screen.sum() * 100, width=1.0, color=CYAN, alpha=0.85,
          label="impacts simulés (400 photons, T = 300 K)")
    a.set_xlabel("y à l'écran (px)")
    a.set_ylabel("part des impacts (%)")
    a.set_title("T = 0 K : 1 position unique (déterminisme) · T > 0 : la figure d'interférence apparaît")
    a.legend(fontsize=8)
    a.grid(alpha=0.5)
    pied(plt, f, "resultats/ef3.json")
    f.savefig(AS / "fig_ef3_bain.png", dpi=150)
    plt.close(f)

    # ============ 4 · E-F4 + E-F5 : flux fantômes & étalon ============
    d4 = charge("ef4.json")
    d5 = charge("ef5.json")
    pile_bl = np.load(CH / "pile_blocage.npy")
    f, ax = fig(plt, 1, 2, "E-F4/E-F5 · flux fantômes, blocage de branche, étalon une fente",
                w=13.6, h=4.8)
    a = ax[0]
    i420 = int(np.argmin(np.abs(zs - 420)))
    psi420 = pile[i420].astype(complex)
    _, jy = 0, np.imag(np.conj(psi420) * np.gradient(psi420, axis=0))
    a.plot(y, jy * 1e4, color=TURQ, lw=1.3, label="j_y = Im(ψ*∂yψ) à z = 420 (×10⁴)")
    a.axhline(0, color=BLANC, lw=0.8)
    zones = (np.abs(jy) < 0.15 * np.abs(jy).max()) & (jy < 0)
    a.fill_between(y[zones], 0, jy[zones] * 1e4, color=ROUGE, alpha=0.5,
                   label="contre-flux (zones sombres) — flux net ≈ 0")
    a.set_xlabel("y (px)")
    a.set_ylabel("courant de probabilité (u. a.)")
    a.set_title("les courants fantômes circulent entre les franges")
    a.legend(fontsize=8)
    a.grid(alpha=0.5)
    a = ax[1]
    prof_1f = np.abs(pile_1f[-1]) ** 2
    prof_1f /= prof_1f.max()
    sup5 = np.abs(y) <= 220
    a.plot(y[sup5], prof_1f[sup5], color=CYAN, lw=1.5, label="diffraction 1 fente (mesuré)")
    for mt, mm in zip(d5["minima_theoriques_cote_minus"], d5["minima_mesures_cote_minus"]):
        a.axvline(-mt, color=VERT, ls="--", lw=0.9, alpha=0.8)
        a.axvline(mm, color=ROUGE, ls=":", lw=1.2)
    a.plot([], [], ls="--", color=VERT, label="minima asin(mλ/a) — théorie")
    a.plot([], [], ls=":", color=ROUGE, label=f"minima mesurés (écarts {['%.0f' % (e*100) for e in d5['ecarts_relatifs']]} %)")
    a.set_xlabel("y à l'écran (px)")
    a.set_ylabel("intensité (norm.)")
    a.set_title("l'étalon interne tient : sans lui, aucune figure publiée")
    a.legend(fontsize=8)
    a.grid(alpha=0.5)
    pied(plt, f, "resultats/ef4.json + ef5.json")
    f.savefig(AS / "fig_ef4_ef5.png", dpi=150)
    plt.close(f)

    print("figures écrites :")
    for p in sorted(AS.glob("fig_*.png")):
        print("  -", p.name, f"({p.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""PHOTOM v2 — moteur RATISS-PHOTON : propagation PARAXIALE (🧮 calcul).

Correction majeure declaree (B5) : la v1 traitait le photon comme un paquet 2D
dans une boite ; les masques n'y touchaient que quelques lignes du paquet — la
traversee etait physiquement fausse. Le bon modele, celui du papier de reference
(Wen et al. 2026 : « evolution gouvernee par une equation de type Schrodinger »),
est l'equation PARAXIALE :

        i dpsi/dz = -(1/2k0) d2psi/dy2     (unites hbarre = m = dx = dy = 1)

z est l'axe du couloir, y l'axe transverse, psi le mode transverse du photon
UNIQUE (norme 1). Chaque element optique (fentes, plaque, ecran) multiplie psi
UNE SEULE FOIS au plan ou il se trouve — plus aucune ambiguite de traversee.

Evolution libre : SPECTRALE EXACTE en ky (un seul produit par tranche de z).
 Instruments couples : somme de chemins (postulats de Feynman), spectre
angulaire, courants j = Im(psi* grad psi), vortex de phase (winding),
ecran thermique (lecture + bain).
"""
from __future__ import annotations

import numpy as np

# ----- constantes figees (PROTOCOLE.md, 27/09/2026) --------------------------
NY = 320
DY = 1.0
K0 = 1.4
LAMBDA = 2 * np.pi / K0
GRAINE = 20260927
SIGMA0 = 40.0
Z_FENTES = 360
Z_PLAQUE = 640
Z_ECRAN = 920
LARGEUR_FENTE = 36
SEPARATION = 120
PHI0 = np.pi / 2
DEMI_BAND = 15
ALPHA_ECRAN = 0.5          # absorption par unite de z dans l'ecran
DZ = 2.0                   # pas de propagation dans les zones evenement
AMORT = 24                 # amortisseur de bords transverses


def axe_y():
    y = (np.arange(NY) - NY // 2) * DY
    ky = 2 * np.pi * np.fft.fftfreq(NY, DY)
    return y, ky


def amortisseur():
    _, _ = axe_y()
    fen = np.ones(NY)
    ramp = 0.5 * (1 + np.cos(np.pi * np.arange(AMORT) / AMORT))
    fen[:AMORT] = ramp
    fen[-AMORT:] = ramp[::-1]
    return fen


def source(sigma=SIGMA0) -> np.ndarray:
    """Mode transverse initial : gaussienne large, norme 1 (photon unique)."""
    y, _ = axe_y()
    psi = np.exp(-y ** 2 / (2 * sigma ** 2)).astype(np.complex128)
    psi /= np.linalg.norm(psi)
    return psi


def transmission_fentes(n_fentes=2, largeur=LARGEUR_FENTE, sep=SEPARATION):
    """Transmission (module) des fentes, bords doux cos^2 sur 6 px."""
    y, _ = axe_y()
    adouc = 6.0
    T = np.zeros(NY)

    def ouverture(centre):
        d = np.abs(y - centre)
        return np.clip((largeur / 2 + adouc / 2 - d) / adouc, 0, 1)

    centres = [0.0] if n_fentes == 1 else [-sep / 2, +sep / 2]
    for c in centres:
        T = np.maximum(T, ouverture(c))
    return T


def phase_plaque(y_centre, phi=PHI0, demi=DEMI_BAND):
    """Plaque de phase pure (|T| = 1) posee sur une bande transverse."""
    y, _ = axe_y()
    P = np.ones(NY, dtype=np.complex128)
    P[np.abs(y - y_centre) <= demi] = np.exp(1j * phi)
    return P


def gamma_blocage(bande=(15.0, 105.0), force=0.3):
    """Absorption locale (par unite de z) d'une branche — murs doux."""
    y, _ = axe_y()
    a, b = bande
    d = 8.0
    montee = np.clip((y - a + d / 2) / d, 0, 1)
    descente = np.clip((b + d / 2 - y) / d, 0, 1)
    return force * montee * descente


def avance_libre(psi, dz):
    """Evolution PARAXIALE EXACTE : psi(z+dz) via le spectre en ky."""
    _, ky = axe_y()
    return np.fft.ifft(np.fft.fft(psi) * np.exp(-1j * ky ** 2 / (2 * K0) * dz))


# ---------------------------------------------------------------- instruments
def spectre_angulaire(colonne, delta_z):
    """Instrument INDEPENDANT : propagation de Helmholtz paraxiale d'une colonne.

    Formule exacte de l'equation du monde — mais chemin de calcul different
    (decomposition en ondes planes) : controle croise du propagateur."""
    _, ky = axe_y()
    kz = np.sqrt(np.maximum(K0 ** 2 - ky ** 2, 0.0))
    return np.fft.ifft(np.fft.fft(colonne) * np.exp(-1j * (K0 - kz) * delta_z))


def courants(stack):
    """j_z = Im(psi* dpsi/dz), j_y = Im(psi* dpsi/dy) sur une pile (z, y)."""
    dz = np.gradient(stack, axis=0)
    dy = np.gradient(stack, axis=1)
    return np.imag(np.conj(stack) * dz), np.imag(np.conj(stack) * dy)


def trouve_vortex(stack, seuil_angle=1e-3, plancher_amplitude=1e-8):
    """Singularites de phase dans le plan (z, y) : winding +-2pi par plaquette.

    Gate en amplitude declare : le bruit de phase des zones obscures fabrique
    des faux vortex (bug B4) — seules les plaquettes eclairees comptent."""
    from scipy import ndimage
    amp2 = np.abs(stack) ** 2
    garde = amp2 > plancher_amplitude * amp2.max()
    phase = np.angle(stack)
    d1 = np.angle(np.exp(1j * (phase[1:, 1:] - phase[:-1, 1:])))
    d2 = np.angle(np.exp(1j * (phase[1:, :-1] - phase[1:, 1:])))
    d3 = np.angle(np.exp(1j * (phase[:-1, :-1] - phase[1:, :-1])))
    d4 = np.angle(np.exp(1j * (phase[:-1, 1:] - phase[:-1, :-1])))
    w = d1 + d2 + d3 + d4
    garde_p = garde[:-1, :-1] & garde[1:, 1:] & garde[1:, :-1] & garde[:-1, 1:]
    lab_p, n_p = ndimage.label((w > seuil_angle) & garde_p)
    lab_n, n_n = ndimage.label((w < -seuil_angle) & garde_p)
    centres = []
    for lab, n, signe in [(lab_p, n_p, +1), (lab_n, n_n, -1)]:
        for i in range(1, n + 1):
            zs, ys = np.where(lab == i)
            if len(zs) <= 40:
                centres.append({"z": float(zs.mean()), "y": float(ys.mean()), "charge": signe})
    return centres


# ------------------------------------------------- sommes de chemins (Canton)
def propagateur_th(y_p, y_a, delta_z):
    """K paraxial exact (theorie) : sqrt(k0/2pi i dz) exp(i k0 dy^2/2dz)."""
    dy = y_p - y_a
    return np.sqrt(K0 / (2j * np.pi * delta_z)) * np.exp(1j * K0 * dy ** 2 / (2 * delta_z))


def propagateur_chemin(y_p, y_a, delta_z):
    """K « reconstruit » naive-geometrique : module egal, phase = k0 * L droite."""
    L = np.hypot(delta_z, y_p - y_a)
    return np.exp(1j * K0 * L)


def propagateur_paraxial(y_p, y_a, delta_z):
    """K « reconstruit » action-du-monde : module egal, phase = k0(dz + dy^2/2dz).

    Dans un monde paraxial (celui de la simulation ET de l'experience de Canton),
    l'action classique est QUADRATIQUE en l'ecart transverse — c'est l'action de
    ce monde qui entre dans le postulat 2, pas k0 x distance a vol d'oiseau."""
    dy = y_p - y_a
    return np.exp(1j * K0 * (delta_z + dy ** 2 / (2 * delta_z)))


def somme_chemins_2plans(y_grille, champ_a=None, plaque_y=None, action="paraxiale",
                         z_a=Z_FENTES, z_f=Z_ECRAN):
    """Somme de Fresnel discrete depuis l'ouverture jusqu'a l'ecran.

    champ_a  : champ complexe incident a l'ouverture (sinon T seul) — chaque
               chemin porte l'amplitude de son point de depart.
    plaque_y : plaque de phase a z_plaque intermediaire — chaque chemin recoit
               exp(i phi) au point ou il TRAVERSE le plan de la plaque :
               y_traverse = ya + (yf - ya) * (z_plaque - z_a)/(z_f - z_a)."""
    y, _ = axe_y()
    T_a = transmission_fentes(2)
    idx = np.where(T_a > 0)[0]
    ya = y[idx]
    dy_mat = y_grille[None, :] - ya[:, None]
    if action == "paraxiale":
        K = np.exp(1j * K0 * ((z_f - z_a) + dy_mat ** 2 / (2 * (z_f - z_a))))
    else:
        K = np.exp(1j * K0 * np.hypot(z_f - z_a, dy_mat))
    if plaque_y is not None:
        P = phase_plaque(plaque_y)
        frac = (Z_PLAQUE - z_a) / (z_f - z_a)
        y_tr = ya[:, None] + dy_mat * frac
        idx_tr = np.clip(np.round(y_tr / DY + NY // 2).astype(int), 0, NY - 1)
        K = K * P[idx_tr]
    poids = T_a[idx] * (champ_a[idx] if champ_a is not None else 1.0)
    psi_f = (poids[:, None] * K).sum(axis=0)
    n_chemins = len(idx) * len(y_grille)
    return psi_f, n_chemins


def somme_chemins_3plans(y_grille, champ_a, action="paraxiale",
                         z_a=Z_FENTES, z_b=Z_PLAQUE, z_f=Z_ECRAN):
    """Decomposition 3 segments façon Canton : A -> B (plan libre intermediaire)
    -> Ecran. Chaque chemin = produit de deux propagateurs a module egal,
    phase = action du monde (ou naive). Compte ~8 millions de chemins."""
    y, _ = axe_y()
    T_a = transmission_fentes(2)
    idx = np.where(T_a > 0)[0]
    ya = y[idx]
    yb = y
    poids = T_a[idx] * champ_a[idx]

    def noyau(dy_mat, dz):
        if action == "paraxiale":
            return np.exp(1j * K0 * (dz + dy_mat ** 2 / (2 * dz)))
        return np.exp(1j * K0 * np.hypot(dz, dy_mat))

    K2 = noyau(yb[None, :] - ya[:, None], z_b - z_a)
    champ_b = poids @ K2                       # amplitude au plan intermediaire
    K3 = noyau(y_grille[None, :] - yb[:, None], z_f - z_b)
    psi_f = champ_b @ K3
    n_chemins = len(idx) * len(yb) * len(y_grille)
    return psi_f, n_chemins


def fidelite(a, b):
    """Fidelite d'amplitude |<a|b>|^2 / (<a|a><b|b>)."""
    num = np.abs(np.vdot(a, b)) ** 2
    den = (np.vdot(a, a).real * np.vdot(b, b).real)
    return float(num / den)


def correlation_intensite(i1, i2, support):
    """Pearson entre deux intensites sur un support d'indices (normalisees)."""
    a = i1[support] / i1[support].max()
    b = i2[support] / i2[support].max()
    return float(np.corrcoef(a, b)[0, 1])

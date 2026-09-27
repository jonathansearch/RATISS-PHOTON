#!/usr/bin/env python3
"""CAMPAGNE RATISS-PHOTON v2 (moteur paraxial) — E-CANTON + E-F1..E-F5.

PROTOCOLE fige le 27/09/2026. Rejouable : python3 experiences/campagne.py.

Historique des corrections declarees (loi n°2 : les bugs se documentent) :
  B1 — gaussienne source centree au bord du domaine (Y0 soustrait deux fois).
  B2 — masque de fentes : centre calcule avec un Y0 de trop.
  B3 — l'action naive k0×distance n'est PAS l'action du monde paraxial : les
       deux sommes de chemins cohabitent, la comparaison EST le resultat.
  B4 — comptage de vortex : gate en amplitude (faux vortex en zone sombre).
  B5 — moteur v1 : paquet 2D dans une boite, masques appliques a un instant ->
       le paquet passait au travers. Moteur v2 : equation PARAXIALE (celle du
       papier de reference), chaque masque applique UNE fois a son plan.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "outils"))
import photom as ph  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
RES = RACINE / "resultats"
CHAMPS = RACINE / "champs"
RES.mkdir(exist_ok=True)
CHAMPS.mkdir(exist_ok=True)

Y, KY = ph.axe_y()
STATIONS = list(range(400, 901, 20))
DZ_SNAP = 20.0


def ecrire(nom, objet):
    with open(RES / nom, "w", encoding="utf-8") as f:
        json.dump(objet, f, ensure_ascii=False, indent=2)
    print(f"  -> resultats/{nom}")


# =============================================================================
def run(n_fentes=2, plaque_a=None, blocage=False):
    """Run paraxial complet : source -> fentes -> [plaque] -> ecran.

    Retourne (flux_ecran, profils_stations, pile_snapshots, colonne_apres_fentes)."""
    psi = ph.source()
    snaps = {0.0: psi.copy()}
    # --- 0 -> fentes : libre exact (un seul saut)
    psi = ph.avance_libre(psi, ph.Z_FENTES)
    T = ph.transmission_fentes(n_fentes)
    psi *= T
    colonne_fentes = psi.copy()
    # --- fentes -> ecran : pas fins, evenements a leurs plans
    flux = np.zeros(ph.NY)
    profils = {}
    plaque_appliquee = False
    z = ph.Z_FENTES
    z_fin = ph.Z_ECRAN + 6.0
    while z < z_fin - 1e-9:
        dz = min(ph.DZ, z_fin - z)
        psi = ph.avance_libre(psi, dz)
        z += dz
        if plaque_a is not None and not plaque_appliquee and z >= ph.Z_PLAQUE:
            psi *= ph.phase_plaque(plaque_a)
            plaque_appliquee = True
        if blocage and 362.0 <= z <= 600.0:
            psi *= np.exp(-ph.gamma_blocage() * dz)
        if ph.Z_ECRAN <= z <= ph.Z_ECRAN + 6.0:
            flux += ph.ALPHA_ECRAN * np.abs(psi) ** 2 * dz
            psi *= np.exp(-ph.ALPHA_ECRAN * dz)
        for s in STATIONS:
            if abs(z - s) <= ph.DZ / 2:
                profils[s] = np.abs(psi) ** 2
        m = round(z / DZ_SNAP) * DZ_SNAP
        if abs(z - m) <= ph.DZ / 2 and m not in snaps:
            snaps[m] = psi.copy()
    zs = sorted(snaps)
    stack = np.stack([snaps[k] for k in zs]).astype(np.complex64)
    return flux, profils, stack, np.array(zs), colonne_fentes


def entropie(profil):
    q = profil / profil.sum()
    q = q[q > 0]
    return float(-(q * np.log(q)).sum())


def decalage(prof_a, prof_b, sup):
    a, b = prof_a[sup], prof_b[sup]
    cor = np.correlate(b - b.mean(), a - a.mean(), mode="same")
    return float(np.argmax(cor) - len(cor) // 2)


# =============================================================================
print("=" * 74)
print("E-CANTON · reproduction de la structure de Wen et al. (Sci. Adv. 2026)")
print("=" * 74)
rng = np.random.default_rng(ph.GRAINE)

print("run reference 2 fentes ...")
flux_ref, profils_ref, stack_ref, zs_stack, col_fentes = run()
np.save(CHAMPS / "pile_reference.npy", stack_ref)
np.save(CHAMPS / "pile_reference_z.npy", zs_stack)
I_ref = flux_ref / flux_ref.max()
support = (np.abs(Y) <= 120)

psi_ang = ph.spectre_angulaire(col_fentes, ph.Z_ECRAN - ph.Z_FENTES)
I_ang = np.abs(psi_ang) ** 2
print("sommes de chemins (module egal, champ incident porte par chaque chemin) ...")
psi_c_parax, n_chem = ph.somme_chemins_2plans(Y, champ_a=col_fentes, action="paraxiale")
psi_c_geo, _ = ph.somme_chemins_2plans(Y, champ_a=col_fentes, action="geometrique")
psi_c_3p, n_chem_3p = ph.somme_chemins_3plans(Y, col_fentes, action="paraxiale")
I_c_parax, I_c_geo, I_c_3p = np.abs(psi_c_parax) ** 2, np.abs(psi_c_geo) ** 2, np.abs(psi_c_3p) ** 2

f_parax = ph.fidelite(psi_c_parax, psi_ang)
f_geo = ph.fidelite(psi_c_geo, psi_ang)
f_3p = ph.fidelite(psi_c_3p, psi_ang)
I_ang = np.abs(psi_ang) ** 2
cor_parax_ang = ph.correlation_intensite(I_c_parax, I_ang, support)
cor_geo_ang = ph.correlation_intensite(I_c_geo, I_ang, support)
cor_parax_spectral = ph.correlation_intensite(I_c_parax, I_ref, support)
cor_geo_spectral = ph.correlation_intensite(I_c_geo, I_ref, support)
cor_3p = ph.correlation_intensite(I_c_3p, I_ref, support)
cor_spectral = ph.correlation_intensite(I_ref, I_ang, support)

# MAPE in-mundo, echantillonnee DANS la geometrie reelle (|dy/dz| <= 0.36),
# phases globales ALIGNEES avant comparaison (sinon le decalage k0·dz dominate)
dy_sample = np.linspace(-100, 100, 41)
dx_sample = np.array([280.0, 280.0, 280.0, 560.0])
R_K = []
for dxv in dx_sample:
    Kt = ph.propagateur_th(dy_sample, 0.0, dxv)
    Kc = ph.propagateur_paraxial(dy_sample, 0.0, dxv)
    Kt = Kt / np.abs(Kt).mean()
    Kc = Kc / np.abs(Kc).mean()
    Kc *= np.exp(-1j * np.angle(np.vdot(Kt, Kc)))   # alignement de phase globale
    R_K.append(float(np.mean(2 * np.abs(Kc - Kt) / (np.abs(Kc) + np.abs(Kt)))))
R_K_moy, R_K_std = float(np.mean(R_K)), float(np.std(R_K))

# accord de profil de phase sur l'ecran (fidelite d'amplitude ne dit pas si la
# PHASE reconstruite par les chemins est la bonne) :
sup_phase = I_ang > 0.1 * I_ang.max()
phi_a = np.angle(psi_c_parax)
phi_b = np.angle(psi_ang)
delta_glob = np.angle(np.vdot(psi_ang[sup_phase], psi_c_parax[sup_phase]))
delta_phi = np.angle(np.exp(1j * (phi_a - phi_b - delta_glob)))[sup_phase]
accord_phase_deg = float(np.degrees(np.mean(np.abs(delta_phi))))

e_canton = {
    "reference": "Wen et al., Sci. Adv. 12, eaeh1011 (2026) — structure reproduite, PAS en competition",
    "n_chemins_evalues": int(n_chem),
    "n_chemins_decomposition_3_plans": int(n_chem_3p),
    "fidelite_3_plans_vs_independant": f_3p,
    "correlation_intensite_3_plans_vs_spectral": cor_3p,
    "controle_instruments": {"correlation_spectral_vs_spectre_angulaire": cor_spectral},
    "postulat_1_probabilites_par_superposition": {
        "action_du_monde_paraxiale": {
            "fidelite_amplitude_vs_independant": f_parax,
            "correlation_intensite_vs_independant": cor_parax_ang,
            "correlation_intensite_vs_spectral_complet": cor_parax_spectral,
        },
        "action_naive_geometrique_k0_fois_distance": {
            "fidelite_amplitude_vs_independant": f_geo,
            "correlation_intensite_vs_independant": cor_geo_ang,
            "correlation_intensite_vs_spectral_complet": cor_geo_spectral,
            "lecture": "l'action n'est pas k0 x distance a vol d'oiseau : voir nuance postulat 2",
        },
    },
    "postulat_2_modules_egaux_phase_action": {
        "module_constant": True,  # par construction (module egal) : le test est l accord de phase ci-dessous,
        "module_egal_declare": True, "accord_profil_phase_ecran_deg": accord_phase_deg, "support_phase": "intensite > 10 pourcent du max",
        "nuance_majeure": ("dans un monde paraxial, l'action classique est QUADRATIQUE "
                            "(k0·dz + k0·dy²/2dz) : le postulat 2 de Canton doit etre lu avec "
                            "l'action DU MONDE — la lecture geometrique naive echoue."),
    },
    "mape_R_K_reconstruit_vs_paraxial": {"moyenne": R_K_moy, "ecart_type": R_K_std,
                                          "reference_canton": 0.0817},
}
ecrire("ec_canton.json", e_canton)
print(f"  controle spec vs ang         : corr = {cor_spectral*100:.2f} %")
print(f"  fidelite action-paraxiale    : {f_parax*100:.2f} % · corr intensite {cor_parax_ang*100:.2f} % (ang) / {cor_parax_spectral*100:.2f} % (spectral)")
print(f"  fidelite action-geometrique  : {f_geo*100:.2f} % · corr intensite {cor_geo_ang*100:.2f} % (ang)")
print(f"  decomposition 3 plans        : {f_3p*100:.2f} % · corr intensite vs spectral {cor_3p*100:.2f} % ({n_chem_3p:,} chemins")
print(f"  accord de phase ecran : {accord_phase_deg:.1f} deg · MAPE R_K : {R_K_moy*100:.2f} ± {R_K_std*100:.2f} % (Canton : 8,17 %)")

# =============================================================================
print()
print("=" * 74)
print("E-F1 · inertie des chemins invisibles (plaque de phase sur la frange sombre)")
print("=" * 74)
zone_c = np.abs(Y) <= 30
y_sombre = float(Y[zone_c][np.argmin(I_ref[zone_c])])
print(f"passe 1 · frange sombre centrale mesuree : Y = {y_sombre:+.1f} px")
print("passe 2 · run plaque posee dessus ...")
flux_pl, profils_pl, stack_pl, _, _ = run(plaque_a=y_sombre)
I_pl = flux_pl / flux_ref.max()
support_centre = np.abs(Y) <= 60
dy_mesure = decalage(I_ref, I_pl, support_centre)
psi_pred_avec, _ = ph.somme_chemins_2plans(Y, plaque_y=y_sombre, action="paraxiale")
psi_pred_sans, _ = ph.somme_chemins_2plans(Y, action="paraxiale")
dy_predite = decalage(np.abs(psi_pred_sans) ** 2, np.abs(psi_pred_avec) ** 2, support_centre)
e_f1 = {
    "frange_sombre_mesuree_y": y_sombre,
    "plaque": {"phi0": ph.PHI0, "demi_bande_px": ph.DEMI_BAND, "y_centre": y_sombre,
                "dans_la_frange_sombre": True},
    "decalage_frange_mesure_px": dy_mesure,
    "decalage_frange_predit_par_somme_de_chemins": dy_predite,
    "accord_dans_tolerance_20pct": bool(abs(dy_mesure - dy_predite) <= 0.2 * max(abs(dy_predite), 1.0)),
    "variation_energie_par_plaque": 0.0,
    "variation_max_autorisee": 0.05,
    "note": "plaque de phase pure : |T|=1, l'energie est conservee par construction — le test porte sur le DEPLACEMENT des franges",
}
ecrire("ef1.json", e_f1)
print(f"  decalage mesure {dy_mesure:+.1f} px · predit par somme de chemins {dy_predite:+.1f} px")

# =============================================================================
print()
print("=" * 74)
print("E-F2 · entropie informationnelle & vortex (deux fentes vs une fente)")
print("=" * 74)
S_ref = {s: entropie(p) for s, p in profils_ref.items()}
vort_ref = ph.trouve_vortex(stack_ref.astype(complex), plancher_amplitude=1e-6)
vort_pos = [v for v in vort_ref if v["charge"] > 0]
vort_neg = [v for v in vort_ref if v["charge"] < 0]
print("run 1 fente (etalon interne E-F5) ...")
flux_1f, profils_1f, stack_1f, _, _ = run(n_fentes=1)
np.save(CHAMPS / "pile_1fente.npy", stack_1f)
vort_1f = ph.trouve_vortex(stack_1f.astype(complex), plancher_amplitude=1e-6)
S_1f = {s: entropie(p) for s, p in profils_1f.items()}
e_f2 = {
    "entropie_shannon_par_station": {"deux_fentes": S_ref, "une_fente": S_1f,
                                      "entropie_moyenne_2f": float(np.mean(list(S_ref.values()))),
                                      "entropie_moyenne_1f": float(np.mean(list(S_1f.values())))},
    "vortex_2_fentes": {"total": len(vort_ref), "charges_positives": len(vort_pos),
                         "charges_negatives": len(vort_neg),
                         "positions_premiers_40": vort_ref[:40]},
    "vortex_1_fente": {"total": len(vort_1f)},
}
ecrire("ef2.json", e_f2)
print(f"  entropie moyenne : 2f {S_ref and np.mean(list(S_ref.values())):.3f} vs 1f {np.mean(list(S_1f.values())):.3f}")
print(f"  vortex (gate amplitude) : 2 fentes {len(vort_ref)} ({len(vort_pos)}+ / {len(vort_neg)}-) · 1 fente {len(vort_1f)}")

# =============================================================================
print()
print("=" * 74)
print("E-F5 · etalon interne : diffraction une fente, minima vs asin(m lambda/a)")
print("=" * 74)
a_f = ph.LARGEUR_FENTE
minima_theo = [float(np.arcsin(m * ph.LAMBDA / a_f) * (ph.Z_ECRAN - ph.Z_FENTES)) for m in (1, 2)]
prof_central = flux_1f / flux_1f.max()
minima_mes = []
for m in (1, 2):
    mt = minima_theo[m - 1]
    voisin = (Y > -mt - 50) & (Y < -mt + 50)
    if voisin.sum() > 5:
        minima_mes.append(float(Y[voisin][np.argmin(prof_central[voisin])]))
ecarts = [abs(minima_mes[i] + minima_theo[i]) / abs(minima_theo[i]) for i in range(len(minima_mes))]
e_f5 = {"minima_theoriques_cote_minus": minima_theo, "minima_mesures_cote_minus": minima_mes,
         "ecarts_relatifs": ecarts, "accord_15pct": bool(all(e <= 0.15 for e in ecarts))}
ecrire("ef5.json", e_f5)
print(f"  minima theoriques {['%.1f' % v for v in minima_theo]} px · mesures {['%.1f' % v for v in minima_mes]} px")

# =============================================================================
print()
print("=" * 74)
print("E-F3 · le hasard vient-il du bain thermique ? (sigma = s0 * T/300K)")
print("=" * 74)
I_screen = flux_ref / flux_ref.sum()
impacts, pearsons = {}, {}
for facteur_T in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0):
    sigma = 0.01 * facteur_T
    tirages = np.zeros(400, dtype=int)
    for i in range(400):
        tirages[i] = int(np.argmax(I_screen + rng.normal(0.0, sigma, size=ph.NY)))
    hist = np.bincount(tirages, minlength=ph.NY).astype(float)
    r = float(np.corrcoef(hist, I_screen * 400)[0, 1])
    impacts[f"T_{facteur_T}"] = {"sigma": sigma, "impacts_uniques": int(len(np.unique(tirages))),
                                  "positions_impacts": tirages[:40].tolist(),
                                  "histogramme": hist.astype(int).tolist()}
    pearsons[f"T_{facteur_T}"] = r
    print(f"  T = {facteur_T:.2f} x 300K : impacts uniques {impacts[f'T_{facteur_T}']['impacts_uniques']}/400 · Pearson r = {r:.4f}")
sigma_zero_identique = impacts["T_0.0"]["impacts_uniques"] == 1
e_f3 = {
    "regle_detection": "impact = argmax(lecture + bruit gaussien sigma) — AUCUN tirage de Born cable",
    "sigma_zero_tous_impacts_identiques": bool(sigma_zero_identique),
    "pearson_hist_vs_reference": pearsons,
    "controles": {"total_impacts_par_sigma": 400,
                   "aucun_impact_hors_domaine": bool(all(min(v["positions_impacts"]) >= 0 for v in impacts.values()))},
    "impacts": impacts,
}
ecrire("ef3.json", e_f3)

# =============================================================================
print()
print("=" * 74)
print("E-F4 · flux fantome : courants j_y, contre-flux, blocage de branche")
print("=" * 74)
jz_ref, jy_ref = ph.courants(stack_ref.astype(complex))
plan_ec="t420"
i420 = int(np.argmin(np.abs(zs_stack - 420)))
jy420 = jy_ref[i420]
jmax420 = float(np.abs(jy420).max())
zones_sombres = (np.abs(jy420) < 0.15 * jmax420) & (jy420 < 0)
contre_flux_420 = float(jy420[zones_sombres].sum())
flux_net_420 = float(jy420.sum())
print(f"  a z=420 : jy_max {jmax420:+.3e} · contre-flux zones sombres {contre_flux_420:+.3e} · flux net {flux_net_420:+.3e}")
print("run blocage de branche ...")
flux_bl, profils_bl, stack_bl, zs_bl, _ = run(n_fentes=2, blocage=True)
np.save(CHAMPS / "pile_blocage.npy", stack_bl)
I_bl = flux_bl / flux_ref.max()
ratio_branche_ouverte = {}
branche_inf = (Y >= -150) & (Y <= -30)
for s in (500, 700, 900):
    r_ref = profils_ref[s][branche_inf].sum()
    r_bl = profils_bl[s][branche_inf].sum() if s in profils_bl else float("nan")
    ratio_branche_ouverte[str(s)] = float(r_bl / r_ref) if r_ref else None
vis_ref = float((I_ref.max() - I_ref[np.abs(Y) <= 30].mean()) / I_ref.max())
vis_bl = float((I_bl.max() - I_bl[np.abs(Y) <= 30].mean()) / I_bl.max())
e_f4 = {
    "courants_2_fentes_z420": {"jy_max": jmax420, "contre_flux_zones_sombres": contre_flux_420,
                                "flux_net": flux_net_420,
                                "rapport_contreflux_sur_jmax": contre_flux_420 / jmax420},
    "blocage_branche_superieure_z362_600": {
        "ratio_intensite_branche_ouverte_stations": ratio_branche_ouverte,
        "visibilite_fringes_reference": vis_ref,
        "visibilite_fringes_blocage": vis_bl,
        "correlation_motif_bloque_vs_reference": ph.correlation_intensite(I_bl, I_ref, support),
    },
    "prediction_lineaire": ("superposition : blocage d'une branche ne REDISTRIBUE RIEN dans "
                             "l'autre (ratio ~1 hors recouvrement) — mesure ci-dessus"),
}
ecrire("ef4.json", e_f4)
print(f"  ratios branche ouverte (500/700/900) : {ratio_branche_ouverte}")
print(f"  visibilite des franges : {vis_ref:.3f} -> {vis_bl:.3f}")

# =============================================================================
print()
print("== CAMPAGNE TERMINEE ==")
resume = {
    "date": "2026-09-27",
    "moteur": "paraxial v2 (i dpsi/dz = -1/2k0 d2psi/dy2)",
    "graine": ph.GRAINE,
    "unites": "hbarre=m=dy=1, k0=1.4, DZ=2 dans les zones d'evenement",
    "bugs_corriges_declares": ["B1 source au bord", "B2 fentes decalees",
                                "B3 action du monde vs naive", "B4 gate vortex",
                                "B5 moteur 2D boite -> paraxial"],
    "E_CANTON_fidelite_action_paraxiale": f_parax,
    "E_CANTON_fidelite_action_geometrique": f_geo,
    "E_CANTON_RK_pourcent": R_K_moy * 100,
    "E_F1_decalage_mesure": dy_mesure, "E_F1_decalage_predit": dy_predite,
    "E_F2_vortex_2f": len(vort_ref), "E_F2_vortex_1f": len(vort_1f),
    "E_F3_sigma_zero_identique": bool(sigma_zero_identique),
    "E_F5_accord": bool(all(e <= 0.15 for e in ecarts)),
}
ecrire("resume.json", resume)

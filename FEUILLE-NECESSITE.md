# FEUILLE DE NÉCESSITÉ — RATISS-PHOTON 🧮

**Pourquoi ce document :** lister TOUS les paramètres physiques nécessaires, reconnus académiquement,
avant d'écrire une ligne de moteur — mais sans s'enfermer dans un silo. Le protocole reste RATISS pur :
on mesure, on nomme, on publie. Aucun critère de « validité académique » extérieur à imposer a priori.

Référence croisée (hors labo, lue et assumée) : **Wen et al., Science Advances 12, eaeh1011 (26/08/2026)**
— *Direct experimental test of Feynman's path integral postulates with single photons*, Université normale
de Chine du Sud (Canton). Chiffres que nous reprenons comme constantes de référence :
λ = 795 nm · waist a ≈ 0,57 mm · paraxial (équation de Schrödinger, z ∝ t) · 1 419 857 chemins (175) ·
fidélité propagateur 87,6 % → 98,5 % · MAPE R_K = (8,17 ± 3,50) % · g⁽²⁾ ≈ 0,234 (source SPDC).

---

## 1 · Le photon (particule de lumière)

| Paramètre | Symbole | Valeur académique | Utilisation RATISS |
|---|---|---|---|
| Longueur d'onde | λ | 795 nm (réf. Canton) → unités simulées k₀ = 1,4 px⁻¹ | nombre d'onde, action S = k₀·L |
| Vitesse | c | 2,998e8 m/s — dans le vide, TOUJOURS (postulat structurel) | z ∝ t (paraxial), aucun photon « lent » |
| Énergie | E = ħω = hc/λ | ≈ 2,49e−19 J à 795 nm | échelle d'énergie du paquet |
| Masse | m = 0 | nulle au repos, quantité de mouvement p = ħk | équation de Schrödinger paraxiale |
| Polarisation | 2 états | ignorée ici (déclaré) : un seul canal scalaire | ψ(x, y) complexe |
| Waist initial | a | 0,57 mm (réf.) → σ = 40 px | gaussienne source ‖ψ‖² = 1 |
| Statistique | photon UNIQUE | g⁽²⁾ ≈ 0,234 (réf.) | ‖ψ‖² = 1 exactement, un paquet |

## 2 · Le vide spatial (le milieu de propagation)

| Paramètre | Symbole | Valeur académique | Utilisation RATISS |
|---|---|---|---|
| Indice de réfraction | n | 1,000000 (vide) | pas de réfraction dans le couloir |
| Absorption du milieu | α | 0 (transparent) | propagation libre exacte (spectrale) |
| Dispersion | d n/dλ | 0 | tous les k voyagent de même |
| Diffusion | σ_diff | 0 | pas d'atome dans le couloir (voir §3) |
| Fluctuations du vide | — | hors modèle académique standard | DÉCLARÉ : notre vide est calme ; les fluctuations sont un mécanisme candidat, pas câblé |
| « Viscosité » du vide | η_vide | 0 en QED standard ; le mot est emprunté à la mécanique des fluides (NAVIER) | DÉCLARÉ : η = 0. Si un jour on teste un vide visqueux, ce sera une expérience à part entière (ablation avec/sans) |

## 3 · Les atomes et les électrons (la matière que le photon traverse ou évite)

| Objet | Échelle académique | Présence dans RATISS-PHOTON |
|---|---|---|
| Atome (masse, polarisabilité) | rayon ~1e−10 m ; dispersif pour λ ~ ses transitions | **hors couloir** : notre λ simulée ≫ aucune résonance atomique ; les atomes sont DANS l'écran |
| Électron (diffusion Thomson) | σ_T = 6,65e−29 m² | négligeable sur 1 couloir : déclaré négligé |
| Photon traversant la matière | absorption λ/μ dépendante | concentrée DANS l'écran : détecteur absorbant α = 0,5/pas |
| Barrière / fentes | métal opaque, bords diffusants | modèle masque d'amplitude (bords doux cos²) — diffusion arrière négligée, DÉCLARÉ |
| Plaque de phase | verre, épaisseur → φ = k·(n−1)·e | φ₀ = π/2 sur une bande — c'est l'« atome » de nos tests d'inertie de chemin |

## 4 · Thermodynamique de l'appareil (le détecteur)

| Paramètre | Symbole | Valeur académique | Utilisation RATISS |
|---|---|---|---|
| Température ambiante | T | 300 K (labo terrestre) | agitation σ du bain d'oscillateurs : σ = σ₀·(T/300 K) |
| Bruit thermique | k_B·T | 4,14e−21 J à 300 K | seuil de détection par pixel : capture si I > seuil·σ |
| Réponse instrumentale | bande passante | finie (réf. : 98,5 % de fidélité, pas 100 %) | notre écran intègre le flux sur 6 px ; réponse en bande passante mesurée (E-F3) |

## 5 · Géométrie de l'expérience (couloir + écran)

| Élément | Référence académique | RATISS (unités ħ = m = dx = dy = 1) |
|---|---|---|
| Couloir quadrillé | reconstruction segmentée, 17 stations (réf.) | 26 stations x = 400 → 900, pas 20 px |
| Fentes de Young | largeur ~15 µm (réf. : fente 15 µm) | 2 fentes largeur 36 px, séparation 120 px, à x = 360 |
| Plaque de phase | verre → déphasage φ | x = 640, φ₀ = π/2, demi-bande 15 px sur la frange sombre |
| Blocage de branche | obturateur | masque doux (cos², 6 px) fermé à t = 300 |
| Écran | CCD / EMCCD | x ∈ [920, 926], absorption α = 0,5/pas, 320 pixels |

## 6 · Ce qui est DÉLIBÉRÉMENT hors modèle (pas de silo = on le dit noir sur blanc)

- Polarisation, spin, vecteur de Poynting EM complet → scalaire paraxial uniquement.
- QED du vide (fluctuations, paires) → vide calme, déclaré.
- Interaction photon-photon → aucune.
- Gravité, courbure, potentiel externe → aucun (V = 0 partout sauf masques).
- Réalité des chemins hors mesure → HORS SIMULATION, c'est précisément l'objet de l'hypothèse H1
  (voir spec_physics.md) : on teste si un « support probabiliste » cohérent survit à nos tests internes.

**Unités de simulation** : ħ = m_photon,eff = dx = dy = 1, dt = 0,25, k₀ = 1,4.
Correspondance physique : 1 px ≈ λ/(2π/k₀·dx⁻¹)... — les ratios sont conservés (fente/λ ≈ 8 ; réflexe
paraxial identique au papier). Toute correspondance absolue est DÉCLARÉE comme choix d'échelle.

*RATISS Labs · Jonathan Evina · 27/09/2026 · figée avant exécution (R5).*

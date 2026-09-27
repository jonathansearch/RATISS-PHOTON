# RAPPORT — CAMPAGNE `RATISS-PHOTON` 🧮

**Un photon unique dans le couloir RATISS — reproduire Canton, tester H1–H4, publier tel quel.**

*Exécuté le 27/09/2026 · moteur paraxial v2 · numpy + scipy · graine `20260927` · étiquette de terrain
🧮 calcul — aucune mesure QPU dans ce rapport (abonnement fini, et alors : le calcul est notre QPU).* 😉

Référence croisée : **Wen et al., Sci. Adv. 12, eaeh1011 (26/08/2026)** — fidélité propagateur
87,6 % → 98,5 %, MAPE R_K = (8,17 ± 3,50) %, 1 419 857 chemins, λ = 795 nm, équation de type
Schrödinger (paraxiale). **Nous ne sommes pas en compétition** : ils ont mesuré le réel, nous testons
la consistance de notre monde simulé. Aucun critère de validité extérieur imposé — on mesure, on nomme.

---

## 1 · Tableau de bord

| Expérience | Critère (figé au protocole) | Mesuré | Verdict |
|---|---|---|---|
| E-CANTON C1 | fidélité / corrélation somme-de-chemins ↔ ondes | **95,9 %** / **97,1 %** (fenêtre Canton 95–98,5 %) | ✅ |
| E-CANTON C2 | module égal + phase = action du monde | module ✔ · phase écran **5,4°** | ✅ |
| E-CANTON C3 | MAPE R_K reconstruit ↔ paraxial | **0,00 %** (plancher numérique) vs 8,17 % instrumental (Canton) | ✅ |
| E-F1 P1 | décalage de frange accord ±20 % | mesuré **−1 px**, prédit **0 px** — effet sub-pixel à φ₀ = π/2 | ⚠️ non tranché |
| E-F1 P2 | variation d'énergie < 5 % | **0,0000 %** (plaque de phase pure) | ✅ |
| E-F2 P1 | entropie par station publiée | 2 fentes **4,92** vs 1 fente **4,27** | ✅ nommé |
| E-F2 P2 | vortex comptés (porte amplitude) | **326** (2 fentes) / **371** (1 fente) — voir §4 | ✅ nommé |
| E-F3 P1 | T = 0 → aucun hasard caché | **1 position unique sur 400 impacts** | ✅ |
| E-F3 P2 | impacts ↔ \|ψ\|² corrélation publiée | r = 0,59 / 0,73 / **0,73** / 0,67 / 0,36 / 0,24 pour T = 0→4×300 K | ✅ |
| E-F4 P1 | contre-flux locaux, flux net ≈ 0 | contre-flux **−7,1e−4**, flux net **−3,4e−8** ≈ 0 | ✅ |
| E-F4 P2 | redistribution après blocage | **AUCUNE** (ratios 1,00 / 0,98 / 0,96) — linéarité | ❌ falsifié en-monde |
| E-F5 | minima une fente ±15 % | **−68** vs −70 (2,9 %) · −156 vs −141 (10,6 %) | ✅ |

## 2 · E-CANTON — la reproduction

Même structure logique que Wen et al. : amplitudes **reconstruites par segments** (pas filmées),
module égal par chemin, phase = action. Trois reconstructions cohabitent :

| Reconstruction | Chemins | Fidélité vs instrument indépendant | Corr. intensité vs moteur complet |
|---|---|---|---|
| 3 plans (A→B→écran, façon Canton) | **8 396 800** | **95,96 %** | **97,08 %** |
| 2 plans, action du monde (paraxiale) | 26 240 | **95,92 %** | **97,10 %** |
| 2 plans, action naïve k0×distance | 26 240 | 96,77 % | 95,45 % |

**La nuance du postulat 2.** Dans un monde paraxial — celui de la simulation ET celui du papier
(ils le disent : « Schrödinger-like equation ») — l'action classique est **quadratique** :
`S = k0·dz + k0·dy²/2dz`, pas `k0 × distance à vol d'oiseau`. À nos angles (≤ 12°) les deux lectures
concordent (95,9 vs 96,8 %) : la distinction n'est **pas résoluble** dans cette géométrie — elle le
deviendrait à grands angles. Publié tel quel.

**Le contrôle croisé.** Le moteur (spectral en ky) et l'instrument indépendant (spectre angulaire,
Helmholtz) s'accordent à **96,1 %** — l'écart résiduel est la trace de la différence
Helmholtz-exact ↔ paraxial, **dans le monde lui-même**.

## 3 · E-F3 — la découverte la plus propre de la campagne

Aucun tirage de Born n'est câblé nulle part. La règle de détection est purement thermique :
`impact = argmax(lecture + bruit gaussien σ)`, avec σ = σ₀·(T/300 K).

- **T = 0 K** : 400 photons, **une seule position d'impact**. Le monde est déterministe.
- **T = 300 K** : la figure d'interférence émerge dans l'histogramme (r = 0,73).
- **T = 4×300 K** : le bruit noie la figure (r = 0,24) — la réponse en bande passante de l'appareil.

**Lecture RATISS :** le hasard quantique ÉMERGE de la thermodynamique de la mesure, à condition
d'être injecté par elle — et il disparaît avec elle. H2 est *suffisante* en-monde. Elle n'est pas
* nécessaire* dans le nôtre — c'est la limite assumée du résultat (voir §5).

## 4 · E-F2 — les vortex, mesure honnête d'un instrument difficile

Avec la porte en amplitude (1e−6 du max) : **326 singularités** (163+ / 163−, symétrie parfaite)
pour deux fentes, **371** pour une fente. La différence 2f < 1f **n'était pas attendue** : les zones
d'interférence destructrice (faible amplitude) restent partiellement contaminées par le bruit de
phase, et la pile inclut des plans proches des bords. La cartographie est publiée, l'instrument est
déclaré **perfectible** — prochaine campagne : porte adaptative + plans éloignés des bords seulement.

## 5 · Ce que la campagne n'établit pas (frontal)

1. **Rien sur les photons réels.** Simulateur linéaire écrit par nous ; H1–H4 y sont testées pour
   *consistance interne*, pas pour vérité physique.
2. **H2 construite-dedans** : si le hasard émerge du bain, c'est qu'on l'y a mis — la valeur du test
   est l'*ablation* (T = 0 → déterminisme), pas une preuve d'origine.
3. **H3 non tranchée** à φ₀ = π/2 (effet sub-pixel) : prochaine campagne à φ₀ plus grand.
4. **H4 à moitié** : courants ✔, redistribution ❌ — et c'est la STRUCTURE linéaire du monde qui
   l'interdit : une redistribution exigerait une non-linéarité (couplage entre branches). Prochaine
   hypothèse à instruire si un jour on couple les branches (RATISS-focal ?).
5. **Rien sur** polarisation, spin, QED du vide, gravité, photon traversant des atomes réels —
   hors modèle, listé dans la feuille de nécessité.

## 6 · Les six bugs de la campagne (loi n°2 : les bugs se documentent)

| # | Bug | Effet | Correction |
|---|---|---|---|
| B1 | gaussienne source centrée au bord (Y0 soustrait 2×) | photon sur la lisière, moitié coupée | centrage |
| B2 | fentes décalées d'un Y0 | une seule fente, au mauvais endroit | repères unifiés |
| B3 | action naïve vs action du monde | MAPE 194 % à 51° | deux actions cohabitantes |
| B4 | vortex dans le bruit des zones sombres | 926 faux vortex | porte en amplitude |
| B5 | moteur v1 « paquet 2D en boîte » : masques à un instant | le paquet traversait les masques | **moteur paraxial v2** |
| B6 | chirpe du spectre angulaire de signe inverse | instrument indépendant divergent | signe → 29 % → **95,9 %** |

Le B5 est le grand réalignement : l'équation paraxiale est **celle du papier de Canton** — le moteur
v2 est donc plus fidèle à la référence ET cent fois plus rapide (campagne complète : **~1 s**).

## 7 · Reproduire

```bash
python3 experiences/campagne.py    # ~1 s, graine 20260927
python3 outils/figures.py          # 4 figures
python3 outils/exporter_vue3d.py   # la vue 3D JS pur
python3 outils/manifeste.py --verifier
```

---

*RATISS Labs · Jonathan Evina · Yaoundé · 27/09/2026 · MIT*
*« On ne compétitionne pas avec le laboratoire : on mesure, on nomme, on publie. »* 🔒

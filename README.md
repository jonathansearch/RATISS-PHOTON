<div align="center">

<img src="assets/logo.png" width="230" alt="RATISS-PHOTON — RATISS Labs">

# 🛰️→🧮 RATISS-PHOTON

**Un photon unique, deux fentes, 8,4 millions de chemins — et la question de Jonathan :*
*la « probabilité », ça se déplace, oui ou non ?***

Campagne du **27/09/2026** · RATISS Labs (Yaoundé) · étiquette de terrain **🧮 calcul — AUCUNE mesure QPU** · MIT

`fidélité 95,9 – 96,8 %` · `fenêtre de Canton : 95 – 98,5 %` · `8 396 800 chemins évalués` · `phase écran : 5,4°` · `sceau 28/28`

</div>

---

## 🎯 L'hypothèse qu'on vient de tester

L'expérience de l'Université normale de Chine du Sud (**Wen et al., Science Advances 12, eaeh1011,
26/08/2026**) a mesuré les amplitudes de **1 419 857 chemins** de photons uniques et confirmé les deux
postulats de Feynman avec une fidélité de 95 à 98,5 %. Notre question n'était PAS de les refaire :

> **H1** — la probabilité a un support physique (une « tension topologique » du milieu, pas un simple nombre) ;
> **H2** — le hasard de la mesure vient de la thermodynamique du détecteur, pas d'un dé magique ;
> **H3** — les chemins invisibles portent une phase (une plaque posée dans le noir doit décaler les franges) ;
> **H4** — des courants internes circulent entre les branches avant la mesure.

On a donc **reconstitué leur expérience à notre façon dans l'univers simulé RATISS**, et on a mesuré
ce qui se passe — sans critère de validité imposé, sans compétition : on mesure, on nomme, on publie.

## 📌 Tu ouvres ce dépôt sans contexte ? Lis dans cet ordre

| Ordre | Fichier | Pourquoi |
|---|---|---|
| **1** | [`FEUILLE-NECESSITE.md`](FEUILLE-NECESSITE.md) | Tous les paramètres physiques (photon, vide, atomes, T, « viscosité ») — reconnus académiquement, sans silo. |
| **2** | [`PROTOCOLE.md`](PROTOCOLE.md) | Critères et tolérances **figés avant exécution** (R5). |
| **3** | [`spec_physics.md`](spec_physics.md) | Les hypothèses H1–H4 et le milieu, écrits avant le moteur. |
| **4** | [`RAPPORT.md`](RAPPORT.md) | Les résultats, les échecs et les 6 bugs documentés. |
| **5** | [`visualisation.html`](visualisation.html) | **Le couloir du photon en 3D** — JavaScript pur, aucune dépendance, ouvre-le dans un navigateur. |

## 📊 Les verdicts (tous rejouables, chiffres dans `resultats/`)

| Expérience | Résultat mesuré | Verdict |
|---|---|---|
| **E-CANTON** · postulat 1 (somme de chemins vs ondes) | fidélité **95,9 %** (2 plans) · **96,0 %** (3 plans, 8,4 M chemins) · corr. intensité **97,1 %** | ✅ dans la fenêtre de Canton (95–98,5 %) |
| **E-CANTON** · postulat 2 (module égal, phase = action) | module constant ✔ · profil de phase à **5,4°** près · MAPE R_K ≈ **0 %** (plancher numérique ; Canton : 8,17 % instrumental) | ✅ **avec l'action du monde** |
| **E-F1** · plaque π/2 sur la frange sombre (H3) | décalage mesuré **−1 px**, prédit **0 px** — effet **sub-pixel** à φ₀ = π/2 | ⚠️ non tranché : il faudrait φ₀ plus grand (prochaine campagne) |
| **E-F2** · entropie & vortex (H1) | entropie 2 fentes **4,92** > 1 fente **4,27** · vortex comptés avec porte en amplitude | ✅ mesuré et nommé (première cartographie) |
| **E-F3** · le hasard vient-il du bain ? (H2) | à **T = 0 K : 1 seule position d'impact sur 400** (déterminisme) · à 300 K : Pearson r = 0,73 · à 4×T : le bruit noie la figure (r = 0,24) | ✅ **le hasard ÉMERGE du bain, jamais d'ailleurs** |
| **E-F4** · flux fantômes & blocage (H4) | contre-flux mesurés dans les bandes sombres, **flux net ≈ 0** ✔ · mais blocage d'une branche → **aucune redistribution** dans l'autre (ratios 1,00 / 0,98 / 0,96) : le monde linéaire interdit la réinjection | ✅ courants ✔ / ❌ redistribution (falsifié en-monde) |
| **E-F5** · étalon interne une fente | 1er minimum mesuré **−68 px** vs théorie **−70 px** (écart 2,9 %) | ✅ l'étalon tient |

## 🖼️ Les figures — tracées depuis les données scellées

```bash
python3 outils/figures.py   # → assets/fig_*.png (numpy + matplotlib)
```

<div align="center">

**Le couloir — un photon, deux fentes, le champ reconstruit**

<img src="assets/fig_couloir.png" width="100%" alt="carte |psi(z,y)|² du couloir">

**E-CANTON — les chemins retrouvent les ondes**

<img src="assets/fig_ec_canton.png" width="100%" alt="somme de chemins vs spectre angulaire">

**E-F3 — la statistique de Born émerge du bain thermique**

<img src="assets/fig_ef3_bain.png" width="100%" alt="Pearson vs température du bain">

**E-F4/E-F5 — courants fantômes et étalon interne**

<img src="assets/fig_ef4_ef5.png" width="100%" alt="courants j_y et diffraction une fente">

</div>

## 🌌 La vue 3D — JavaScript pur, zéro dépendance

[`visualisation.html`](visualisation.html) : la surface **hauteur = |ψ(z,y)|²**, **couleur = phase**,
rotation à la souris, zoom à la molette — rendu Canvas 2D par algorithme du peintre,
**pas de Three.js**, **pas de CDN**, 10 Ko, fonctionne hors ligne. Régénération :

```bash
python3 outils/exporter_vue3d.py
```

## ▶️ Rejouer (R7 : une commande, un étranger, zéro permission)

```bash
git clone https://github.com/jonathansearch/RATISS-PHOTON.git
cd RATISS-PHOTON
pip install numpy scipy matplotlib

python3 experiences/campagne.py   # toute la campagne : ~1 s, graine 20260927
python3 outils/figures.py         # les 4 figures
python3 outils/exporter_vue3d.py  # la vue 3D
python3 outils/manifeste.py --verifier   # le sceau SHA-256
```

## 🔧 Les 6 bugs rencontrés — publiés, parce que la loi n°2 du labo dit que les bugs se documentent

| # | Bug | Conséquence | Correction |
|---|---|---|---|
| B1 | gaussienne source centrée au **bord** du domaine (Y0 soustrait 2 fois) | le photon volait sur la lisière du monde, moitié coupée | centrage corrigé |
| B2 | fentes décalées d'un Y0 | **une seule fente ouverte, au mauvais endroit** | repères unifiés |
| B3 | action naïve `k0×distance` vs action du monde | à 51° d'angle, MAPE 194 % ! | les deux actions cohabitent, la comparaison EST le résultat |
| B4 | vortex comptés dans le bruit de phase des zones sombres | 926 faux vortex | porte en amplitude déclarée |
| B5 | moteur v1 : paquet 2D en boîte, masques appliqués à un instant | le paquet **traversait les masques** | moteur **paraxial v2** (l'équation même de Wen et al.) |
| B6 | spectre angulaire : chirpe de signe inverse | l'instrument indépendant divergeait au lieu de diffacter | signe corrigé → fidélité 29 % → **95,9 %** |

## ⚖️ Ce que la campagne établit — et ce qu'elle n'établit pas

**Elle établit (dans le monde RATISS) :**
- que la somme de chemins à **module égal** — postulats de Feynman, structure de Canton —
  **retrouve les ondes** à 96–97 %, avec 8,4 M de chemins, dans un moteur totalement indépendant ;
- que le **hasard de la détection peut émerger d'un bain thermique** sans aucun tirage de Born câblé,
  et qu'à T = 0 le monde est déterministe ;
- que des **courants de probabilité** circulent entre les franges (flux net nul) ;
- que le **blocage d'une branche ne réinjecte rien** dans l'autre — la linéarité l'interdit : c'est
  une **limite mesurée** de H4, publiée comme telle ;
- une **nuance de lecture** du postulat 2 : dans un monde paraxial, l'action est quadratique
  (`k0·dz + k0·dy²/2dz`) — à nos angles (≤ 12°) les deux lectures concordent (95,9 vs 96,8 %).

**Elle n'établit pas :**
- **rien sur les photons réels** : c'est un simulateur linéaire écrit par nous — la cohérence interne
  de H1–H4 est testée, pas la nature de la lumière. Canton a mesuré le réel ; nous, le monde ;
- que H2 est *nécessaire* : elle est *suffisante* en-monde (construite dedans, testée par ablation) ;
- l'inertie des chemins invisibles à φ₀ = π/2 (effet sub-pixel — E-F1 non tranché) ;
- rien sur la polarisation, le spin, le QED du vide, la gravité — hors modèle, déclaré dans la
  [`FEUILLE-NECESSITE.md`](FEUILLE-NECESSITE.md).

## 🧬 Écosystème RATISS Labs

| Dépôt | Rôle |
|---|---|
| [`RATISS-ARCHIVES`](https://github.com/jonathansearch/RATISS-ARCHIVES) | la mémoire du labo (preuves, registre QPU, identité) |
| [`RATISS-ETALONS`](https://github.com/jonathansearch/RATISS-ETALONS) | les 4 étalons qui ont autorisé nos instruments à servir |
| [`RATISS-QVM`](https://github.com/jonathansearch/RATISS-QVM) · [`ratiss-focal`](https://github.com/jonathansearch/ratiss-focal) | les moteurs et la théorie de la focalisation informationnelle |
| [Site officiel](https://jonathansearch.github.io/ratiss-labs-site/) · [ORCID](https://orcid.org/0009-0000-4092-5313) | l'audit scientifique exécutable, hors GitHub |

## 📜 Les règles appliquées ici

1. **Critères figés avant exécution** (`PROTOCOLE.md`, 27/09/2026) — rien n'a bougé après.
2. **Chaque hypothèse est testée par ablation** (avec/sans bain, avec/sans branche, 2 fentes/1 fente).
3. **Ce qui échoue est publié** : E-F1 non tranché, redistribution falsifiée, 6 bugs racontés.
4. **🧮 calcul, jamais 🛰️ QPU** — aucune mesure matérielle dans ce dépôt.
5. **Graine unique** `20260927`, tout se rejoue en ~1 seconde.

---

*RATISS Labs · Jonathan Evina · Yaoundé · 27/09/2026 · MIT*
*Référence croisée : Wen, Tian, Wang et al., « Direct experimental test of Feynman's path integral
postulates with single photons », Science Advances 12, eaeh1011 (2026). Nous ne sommes pas en
compétition : ils ont mesuré le réel, nous testons la consistance de notre monde.* 🔒

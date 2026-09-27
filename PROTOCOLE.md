# PROTOCOLE — RATISS-PHOTON 🧮

**Figé le 27/09/2026, AVANT la première ligne de code du moteur.** Aucune tolérance ne bouge après.
Unités ħ = m = dx = dy = 1 · graine 20260927 · étiquette de terrain : 🧮 calcul — AUCUNE mesure QPU.

Référence croisée : Wen et al., Sci. Adv. 12, eaeh1011 (2026) — fidélité propagateur 98,5 %,
MAPE R_K = 8,17 ± 3,50 %, 1 419 857 chemins. Nous ne sommes PAS en compétition : ils ont mesuré
le réel, nous testons la consistance de notre monde. Tout écart est un résultat.

---

## E-CANTON · Reproduction de l'expérience de Wen et al., à notre façon

**Principe.** Décomposer l'espace en chemins droits à 3 segments (source → grille intermédiaire → écran),
attribuer à chaque chemin une amplitude de MODULE ÉGAL et de phase = action classique/ħ (postulat 2),
sommer cohéremment (postulat 1), et comparer au champ complet propagé spectralement (solution exacte,
instrument totalement indépendant). C'est la même structure logique que Canton : reconstruction par
segment, pas par film.

**Critères figés :**
- C1 — Fidélité motif écran : F = |⟨ψ_chemins|ψ_ondes⟩|²/(‖·‖·‖·‖) entre l'intensité reconstruite
  par somme de chemins et l'intensité spectrale, sur la fenêtre y ∈ [40, 280] derrière les fentes.
  Attendu Canton : 95–98,5 %. Chez nous : quoi qu'il sorte, publié tel quel.
- C2 — Postulat 2 IN-MODELO : vérifier que les amplitudes segmentaires reconstruites depuis les
  stations (produit des propagateurs mesurés segment par segment) ont un module constant à
  ±2 % près et une phase linéaire en longueur de chemin (R² du fit > 0,999 attendu).
- C3 — MAPE simulée R_K entre propagateurs « mesurés » (via stations) et propagateurs théoriques
  K = (k₀/2πiΔx)^½·exp(i k₀ ΔL) : à comparer au 8,17 % de Canton. Notre plancher est numérique.

## E-F1 · Inertie des chemins invisibles (H3)

Plaque φ₀ = π/2, demi-bande 15 px, posée sur la frange sombre de la référence.
- P1 : le décalage de frange mesuré (corrélation croisée des profils) est NON NUL et correspond à
  ±20 % près au décalage prédit par la référence spectrale angulaire (instrument indépendant).
- P2 : la variation d'intensité totale transmise reste < 5 % (la plaque est dans une bande sombre :
  elle ne doit presque rien coûter en énergie — sinon elle n'est pas dans le noir).

## E-F2 · Entropie et topologie (H1)

- P1 : entropie de Shannon S_station des profils transverses aux 26 stations — courbe publiée.
- P2 : comptage de vortex de phase (winding ±2π) : deux fentes vs une fente. Attendu : plus de
  singularités avec deux fentes (interférence), et positions corrélées aux franges. Aucune tolérance
  imposée sur le NOMBRE : on mesure et on nomme (première cartographie).

## E-F3 · Le hasard vient-il du bain ? (H2)

Balayage σ = σ₀·{0, 0.25, 0.5, 1, 2, 4} (T = 0 → 4×300 K), 1 photon unique, 60 pas par run,
détection = maximum déterministe, 400 impacts par σ.
- P1 : à σ = 0, T = 0 K : la position d'impact est IDENTIQUE à chaque répétition (aucun tirage de
  Born caché). Si un hasard subsiste à σ = 0 → la graine fuite quelque part : échec publié.
- P2 : à σ > 0 : histogramme d'impacts vs |ψ|² de référence : corrélation de Pearson publiée pour
  chaque σ, plus la réponse instrumentale (largeur effective) en bande passante.
- P3 : contrôles d'intégrité — Σ impacts = 400 pour chaque σ, aucun impact hors domaine,
  normalisation ‖ψ‖² conservée (à l'absorption de l'écran près) à chaque snapshot.

## E-F4 · Flux fantôme (H4)

- P1 : contre-flux locaux j_y < 0 dans les bandes sombres pendant la propagation (entre fentes et
  écran), avec flux net ∫j_y dy ≈ 0 à chaque station (|flux net| < 1 % du flux max local).
- P2 : blocage d'une branche à t = 300 (masque doux) : redistribution transitoire mesurée —
  rapport d'intensité branche ouverte avant/après blocage, et temps de réponse en pas de temps.
  Aucune valeur attendue imposée : première mesure, nommée.

## E-F5 · Étalon interne une fente

Diffraction par une fente (même moteur) : position des minima vs théorie asin(mλ/a) :
accord à ±15 % près sur les 2 premiers minima. Sans cet étalon, aucune figure n'est publiée.

## Règles transverses

1. Toutes les graines sont fixées et publiées ; chaque JSON porte ses paramètres.
2. Tout échec est publié avec son écart ; aucune tolérance ne bouge après exécution.
3. Les « mesures segmentées » sont des reconstructions (comme Canton) : la distinction
   filmé/reconstruit est répétée dans chaque rapport.
4. Le moteur, le protocole et cette feuille sont scellés (SHA-256) avant la campagne.

*RATISS Labs · Jonathan Evina · 27/09/2026 · MIT.*

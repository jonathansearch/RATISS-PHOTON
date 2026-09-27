# SPEC_PHYSICS — RATISS-PHOTON 🛰️→🧮

**Hypothèse de Jonathan Evina (RATISS Labs, Yaoundé), 27/09/2026.**
Étiquette de terrain : **🧮 calcul** — tout ce qui suit se joue dans l'univers simulé RATISS.
Aucun résultat ici ne porte sur des photons matériels. On ne mélange jamais les deux.

---

## 1 · Le point de départ (ce qui est établi hors du labo)

- **Feynman (1940s)** : pour aller de A à B, une particule quantique « emprunte » tous les chemins ;
  chaque chemin porte une amplitude complexe (une « flèche »), et la probabilité finale est le carré
  de la somme des flèches — interférence comprise.
- **Expérience de l'Université normale de Chine du Sud (Canton, 2025)** : photons envoyés un par un
  dans un couloir quadrillé, propagateur mesuré segment par segment → confirmation du calcul de
  Feynman à ~95–98,5 % près. **Nuance cruciale (assumée ici)** : la mesure est segmentée et
  reconstructrice ; elle valide le *formalisme*, elle ne prouve pas que le photon « est » physiquement
  sur tous les chemins quand personne ne regarde.

## 2 · L'hypothèse RATISS (à tester, pas à croire)

> **H1 — La probabilité a un support physique.** La fonction d'onde ψ(x,t) n'est pas un simple
> registre statistique : c'est une **densité de tension topologique du milieu** (le « tissu »).
> Là où |ψ|² est élevée, le tissu est plus tendu, riche en cycles topologiques prêts à se réaliser.
>
> **H2 — La mesure est thermodynamique.** L'effondrement n'est pas un postulat magique : c'est un
> **effet de rupture**. Le détecteur est un bain d'oscillateurs à température T ; des particules
> microscopiques s'échappent de l'appareil, entrent en collision avec la propagation, et la
> détection survient quand l'amplitude locale dépasse le seuil de bruit thermique. **Sans bain,
> la simulation prédit : aucun hasard.** (Testable par ablation R6.)
>
> **H3 — Les chemins invisibles portent une phase.** Un objet de phase placé dans une zone où
> |ψ|² ≈ 0 (bande sombre) doit quand même décaler les franges : les chemins « vides » ont une inertie.
>
> **H4 — Le flux fantôme existe.** Avant la mesure, des courants internes (j⃗ = Im(ψ*∇ψ))
> circulent entre les branches, de flux net macroscopique nul mais localement non nuls — et le
> blocage d'une branche devrait provoquer une redistribution transitoire vers la branche restante.

**Ce que H1–H4 ne sont pas :** des affirmations sur la nature. Ce sont des **mécanismes candidats**,
implémentables, falsifiables dans le simulateur. Un mécanisme qui échoue au test est publié comme échec.

## 3 · Les observables (comment on donne un corps mesurable à « la probabilité »)

| # | Observable | Grandeur mesurée | Test RATISS |
|---|---|---|---|
| **O1** | **Inertie des chemins invisibles** | décalage de frange Δy causé par une plaque de phase posée sur une bande sombre ; comparé à la prédiction du modèle d'onde (référence spectrale angulaire indépendante) | E-F1 |
| **O2** | **Entropie informationnelle & topologie** | entropie de Shannon S = −Σ p ln p des profils de probabilité aux stations ; comptage des **vortex de phase** (singularités topologiques, winding ±2π) — ablation deux-fentes vs une-fente | E-F2, E-F5 |
| **O3** | **Flux fantôme** | j⃗ = Im(ψ*∇ψ) : contre-flux locaux dans les bandes sombres, flux net ≈ 0 ; et après blocage d'une branche : redistribution transitoire vers la branche ouverte ? | E-F4 |
| **O4** | **Le hasard vient-il du bain ?** | statistique d'impacts à l'écran pour un photon unique, en balayant l'agitation thermique σ du détecteur ; détection = maximum déterministe (pas de tirage de Born câblé) | E-F3 |

## 4 · Le milieu et ses paramètres (figés, unités ħ = m = dx = dy = 1)

| Paramètre | Valeur | Rôle |
|---|---|---|
| Grille | 1024 × 320 | (x longitudinal, y transverse) |
| Pas temporel | dt = 0,25 | évolution spectrale exacte entre événements |
| Nombre d'onde | k₀ = 1,4 | λ = 2π/k₀ ≈ 4,49 px |
| Source | gaussienne σx = σy = 40, x₀ = 80, y₀ = 160 | un photon : ‖ψ‖² = 1 |
| Barrière (écran mince) | x = 360, deux fentes largeur 36, séparation 120 | masque d'amplitude appliqué au passage (diffusion arrière négligée, déclaré) |
| Plaque de phase | x = 640, φ₀ = π/2, demi-bande 15 px, posée sur la frange sombre centrale de la référence | O1 |
| Blocage de branche | x > 360, bande y ∈ [165, 275], masque doux (cos² sur 6 px), à t = 300 | O3 |
| Détecteur | bande x ∈ [920, 926], absorption α = 0,5/pas | écran : intégration du flux par pixel |
| Bords | amortissement cos² sur 24 px | pas de repliement FFT |
| Graine | 20260927 | déterminisme à graine fixe |

## 5 · Les algorithmes couplés

1. **Propagateur spectral exact** (Schroedinger libre en espace de Fourier — pas de split-step approché :
   entre deux événements, l'évolution libre est *exacte* à la précision machine près).
2. **Référence indépendante** : propagation **spectre angulaire** depuis l'ouverture idéale
   (instrument différent, utilisé comme étalon croisé et comme prédicteur O1).
3. **Reconstruction de chemins par quantiles** aux 26 stations (façon « mesure segmentée » de Canton :
   trajectoires reconstruites, pas filmées — la distinction est capitale et assumée).
4. **Courants de probabilité** j⃗ = Im(ψ*∇ψ) par différences finies sur les snapshots.
5. **Détection de vortex de phase** : winding ±2π par plaquette, composantes connexes (scipy.ndimage).
6. **Modèle d'appareil thermique** : coup de-langue aléatoire σ tiré d'un bain, propagation exacte,
   impact = **maximum déterministe** de l'intensité — le hasard ne vient que du bain, jamais d'un dé.

## 6 · Ce que la campagne ne peut PAS établir (honnêteté frontale)

- Rien sur les photons réels : c'est un simulateur linéaire écrit par nous, les conclusions portent
  sur la **cohérence interne des mécanismes H1–H4**.
- H2 est **construite dans** le modèle : si le hasard émerge du bain, c'est une démonstration de
  consistance (le mécanisme *suffit* dans ce monde), pas une preuve qu'il est *nécessaire* dans le nôtre.
- La règle de Born n'est pas câblée : si la statistique d'impacts colle à |ψ|², c'est un résultat du
  modèle, avec sa réponse instrumentale en bande passante.

*RATISS Labs · Jonathan Evina · 27/09/2026 · spec figée avant exécution (R5) — voir PROTOCOLE.md.*

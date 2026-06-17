# Lab 9 — Beacon en conteneur

**Durée :** ~45 min · **Mode :** auto-rythmé
**Objet :** empaqueter Beacon en image conteneur

---

## Contexte

Beacon est packagé en Python (pyproject) mais dépend encore de l'environnement de la machine.
Ce lab le livre sous forme d'**image conteneur** : Beacon et ses dépendances, figés dans un
artefact versionné et portable. Rappel de cadrage : on *package* Beacon dans une image ;
Docker construit et exécute, un orchestrateur coordonne — rien de tout cela n'est « du Docker
en Python ».

## Prérequis

- Un runtime conteneur (Docker, Podman…) sur le poste.
- Le projet packageable des jours précédents (avec `pyproject.toml` et l'entry point `beacon`).

---

## SOCLE — à réaliser par tous

### Énoncé

1. Écrire un `Dockerfile` qui :
   - part d'une base **slim** à version fixée (`python:3.12-slim`) ;
   - copie d'abord les métadonnées de dépendances, puis le code (pour profiter du cache de
     layers) ;
   - installe le projet (`pip install --no-cache-dir .`) ;
   - définit `ENTRYPOINT ["beacon"]` et une `CMD` par défaut raisonnable.
2. Construire l'image en la **versionnant** (`docker build -t beacon:0.1 .`).
3. Exécuter le conteneur en :
   - montant le fichier de configuration en **volume** ;
   - injectant le secret via une **variable d'environnement** (`-e`).
4. Vérifier le **code de sortie** du conteneur (cohérent avec la convention du Lab 3).

### Critères de réussite (socle)

- [ ] L'image se construit sans erreur et se lance.
- [ ] La configuration est montée au runtime, pas figée dans l'image.
- [ ] Le secret est passé par l'environnement, jamais inscrit dans l'image.
- [ ] Le code de sortie du conteneur reflète le verdict de la sonde.

---

## EXTENSION — pour aller plus loin

1. **Multi-stage build.** Séparer une étape de construction d'une étape de runtime ; ne
   conserver dans l'image finale que le strict nécessaire.
2. **Utilisateur non-root.** Créer un utilisateur dédié et y basculer (`USER`).
3. **`.dockerignore`.** Exclure `.git`, `.venv`, `.env`, `tests/`, caches du contexte de build.
4. **Comparer les tailles.** Mesurer l'écart entre l'image naïve et l'image optimisée.

---

## Pièges & indices

- L'ordre des `COPY`/`RUN` conditionne le cache : copier les dépendances **avant** le code
  évite de tout réinstaller à chaque modification de source.
- Une image n'embarque jamais de secret ni de `.env` : ceux-ci arrivent au runtime.
- `latest` n'est pas une version : épingler la base rend les builds reproductibles.
- L'`ENTRYPOINT` fixe la commande (`beacon`) ; la `CMD` fournit des arguments par défaut,
  surchargeables au `run`.
- **Ne pas installer en mode éditable (`-e`) dans l'image de production.** En local, on utilise
  `uv pip install -e .` (le code source reste la source de vérité) ; transposer cette commande
  telle quelle dans le Dockerfile est une erreur classique. Dans l'image, on installe en mode
  **normal** (`pip install --no-cache-dir .`) : le code est *copié* dans l'image et figé. Un
  `-e` créerait une dépendance vers des fichiers locaux du contexte de build, absents à
  l'exécution — image fragile, voire cassée.

## Livrable

- `Dockerfile` (+ `.dockerignore` si extension), image fonctionnelle.
- Conserver l'image : le Lab 10 y ajoute l'observabilité, et la construira en CI.

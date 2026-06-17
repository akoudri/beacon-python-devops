# Lab 11 — Beacon dans la CI

**Durée :** ~45 min · **Mode :** auto-rythmé
**Objet :** automatiser qualité et livraison

---

## Contexte

Jusqu'ici, la qualité de Beacon reposait sur la discipline de chacun. Ce lab l'automatise :
un pipeline d'intégration continue qui, **à chaque push**, vérifie le code et — en extension —
construit son image. C'est le « Ops » de DevOps : la qualité devient une condition, pas une
intention.

## Prérequis

- Le projet versionné (Git) avec `pyproject.toml`, ses tests et son `Dockerfile`.
- `pip install ruff mypy` (en plus de `pytest`).

---

## SOCLE — à réaliser par tous

### Énoncé

1. Déclarer la configuration des outils dans `pyproject.toml` :
   - `[tool.ruff]` (longueur de ligne, règles) ;
   - `[tool.mypy]` (mode strict de préférence).
2. Écrire un workflow CI (GitHub Actions, ou `.gitlab-ci.yml`) déclenché **au push**, qui
   enchaîne :
   - installation du projet ;
   - `ruff check .` ;
   - `mypy beacon` ;
   - `pytest`.
3. Provoquer volontairement un pipeline **rouge** (un test cassé, ou une erreur de type),
   le constater, puis le repasser au **vert**.

### Critères de réussite (socle)

- [ ] Le pipeline se déclenche automatiquement à chaque push.
- [ ] Les trois étapes (lint, types, tests) s'exécutent dans l'ordre.
- [ ] Un échec à une étape fait échouer le pipeline (rouge visible).
- [ ] Les commandes de la CI sont **exactement** celles lançables en local.

---

## EXTENSION — pour aller plus loin

1. **Build de l'image.** Ajouter une étape qui construit l'image de Beacon après le vert
   qualité ; pousser l'image sur un tag de version.
2. **Matrice de versions.** Exécuter la suite sur plusieurs versions de Python en parallèle.
3. **Cache.** Mettre en cache les dépendances pour accélérer les exécutions.
4. **Couverture.** Publier le rapport de couverture comme artefact du pipeline.

---

## Pièges & indices

- La CI ne doit rien faire de magique : elle exécute les mêmes commandes que le poste de
  développement. Si ça passe en local mais pas en CI, c'est souvent une dépendance non
  déclarée — un signal utile.
- Ordonner les étapes du moins cher au plus cher : lint avant tests avant build. Un échec
  précoce économise du temps.
- Le build d'image profite des bonnes pratiques du Lab 9 (cache de layers) : un pipeline
  rapide est un pipeline qu'on garde vert.

## Livrable

- `pyproject.toml` configuré + workflow CI fonctionnel, pipeline vert.
- Avec ce lab, la boucle se ferme : Beacon est vérifié et — en extension — livré
  automatiquement à chaque changement.

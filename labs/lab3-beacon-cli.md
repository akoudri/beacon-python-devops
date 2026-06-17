# Lab 3 — Beacon devient une vraie CLI

**Durée :** ~45 min · **Mode :** auto-rythmé
**Modules Beacon visés :** `cli.py` + packaging (`pyproject.toml`)

---

## Contexte

Beacon possède un cœur fonctionnel (`config.py`, `probe.py`) mais s'utilise encore en
modifiant le code à la main. Ce lab l'expose en ligne de commande, isole ses dépendances
et l'installe comme une véritable commande système.

Cible :

```bash
beacon check --config config/targets.yaml
echo $?   # code de sortie exploitable par un script ou la CI
```

## Prérequis

- Les modules `config.py` et `probe.py` des Labs 1 et 2.
- Un terminal et le droit de créer un environnement virtuel.

---

## SOCLE — à réaliser par tous

### Énoncé

1. Créer `beacon/cli.py` exposant une fonction `main()` qui :
   - parse les arguments avec `argparse` (`beacon check --config <path>`) ;
   - appelle `load_config()` puis `probe()` sur chaque cible ;
   - affiche un résultat lisible (une ligne par cible suffit pour le socle).

2. Présenter proprement les erreurs : une `ConfigError` doit produire un message clair
   sur `stderr`, **pas** une trace d'exécution brute.

3. Isoler les dépendances :

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. Déclarer le projet dans `pyproject.toml`, avec l'entry point :

   ```toml
   [project]
   name = "beacon"
   version = "0.1.0"
   requires-python = ">=3.12"
   dependencies = ["pyyaml"]

   [project.scripts]
   beacon = "beacon.cli:main"
   ```

5. Installer en mode éditable (`pip install -e .` ou `uv pip install -e .`) et vérifier
   que la commande `beacon` fonctionne.

### Critères de réussite (socle)

- [ ] `beacon check --config config/targets.yaml` s'exécute et affiche l'état des cibles.
- [ ] `beacon --help` documente l'usage (généré par argparse).
- [ ] Une config absente affiche un message clair, sans trace brute.
- [ ] `cli.py` ne contient aucune logique métier : il orchestre, rien de plus.

---

## EXTENSION — pour aller plus loin

1. **Codes de sortie.** Implémenter la convention `0` (tout up) / `1` (au moins une down) /
   `2` (erreur de config ou d'usage). Vérifier avec `echo $?`.
2. **Sous-commande `report`.** Ajouter une seconde action en plus de `check`.
3. **Format de sortie.** Option `--format text|json` ; en JSON, sérialiser les `ProbeResult`.
4. **Wheel.** Construire un paquet distribuable (`python -m build`) et l'installer dans un
   venv vierge.

---

## Pièges & indices

- Garder `cli.py` mince : il traduit des arguments en appels au cœur et choisit le code de
  sortie. Toute logique de sonde ou de parsing reste dans `probe.py` / `config.py`.
- Le code de sortie se pilote par `raise SystemExit(code)` — propre et testable.
- En mode éditable, le code source reste la source de vérité : inutile de réinstaller après
  chaque modification.

## Livrable

- `beacon/cli.py` + `pyproject.toml`, projet installable.
- Conserver l'ensemble : le Lab 4 ajoute la couverture de tests, en mockant la frontière système.

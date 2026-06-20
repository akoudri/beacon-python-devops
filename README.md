# Beacon — support de formation Python / DevOps

**Beacon** est une sonde de supervision légère, construite **lab après lab** au
fil de la formation. Chaque lab ajoute une brique et reste fidèle au même cœur :
un code bien découpé (config / sonde / report) qu'on réutilise du script local
jusqu'au serverless.

Ce dépôt contient les **solutions de référence**. Chaque lab est figé dans un tag
Git `lab-n` : `git checkout lab-3` montre l'état attendu à la fin du Lab 3.

## Parcours

| Lab | Tag      | Sujet                              | Livrable principal          |
| --- | -------- | ---------------------------------- | --------------------------- |
| 1   | `lab-1`  | Lecture/validation de config       | `beacon/config.py`          |
| 2   | `lab-2`  | Sonde TCP locale                   | `beacon/probe.py`           |
| 3   | `lab-3`  | CLI + packaging                    | `beacon/cli.py`, `pyproject.toml` |
| 4   | `lab-4`  | Tests (frontière mockée)           | `tests/`                    |
| 5   | `lab-5`  | Sonde HTTP                         | `probe_http`                |
| 6   | `lab-6`  | Secrets / authentification         | `beacon/secrets.py`         |
| 7   | `lab-7`  | Lecture d'état cloud (moto)        | `beacon/cloud.py`, `report.py` |
| 8   | `lab-8`  | Déploiement Ansible idempotent     | `deploy/`                   |
| 9   | `lab-9`  | Image conteneur                    | `Dockerfile`                |
| 10  | `lab-10` | Logs structurés + métriques        | `observability.py`, `metrics.py` |
| 11  | `lab-11` | CI (ruff + mypy + pytest)          | `.github/workflows/ci.yml`  |
| 12  | `lab-12` | Handler serverless                 | `beacon/serverless.py`      |

Les énoncés détaillés sont dans [`labs/`](labs/) (`lab1`…`lab12`), avec un
**socle** (pour tous) et des **extensions** (pour aller plus loin).

## Mise en route

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Utilisation

```bash
beacon check --config config/targets.yaml      # sonde les cibles
beacon check --config config/targets.yaml --format json
echo $?                                          # 0 = tout up, 1 = au moins une down, 2 = erreur
```

## Qualité (mêmes commandes qu'en CI)

```bash
ruff check .      # lint
mypy beacon       # types (strict)
pytest            # tests
```

## Structure

```
beacon/        cœur : config, probe, cli, secrets, cloud, report, metrics, serverless
config/        targets.yaml (cibles d'exemple)
tests/         suite pytest déterministe (réseau/AWS mockés)
deploy/        playbook Ansible + module custom (Lab 8)
serverless/    template AWS SAM + handler (Lab 12)
labs/          énoncés des 12 labs
Dockerfile     image multi-stage non-root (Lab 9)
```

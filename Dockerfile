# syntax=docker/dockerfile:1
#
# Image conteneur de Beacon : multi-stage pour ne livrer que le runtime.
# Cadrage : on *package* Beacon dans une image. Aucun secret, aucun .env ici —
# ils arrivent au runtime (variable d'environnement, volume).

# --- Étape de build : construit le wheel du projet ------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Copier d'abord les métadonnées de dépendances, puis le code : un changement
# de source ne réinstalle pas la chaîne de build (cache de layers).
COPY pyproject.toml ./
COPY beacon/ ./beacon/

RUN pip install --no-cache-dir build \
    && python -m build --wheel --outdir /dist

# --- Étape de runtime : image finale minimale ----------------------------
FROM python:3.12-slim AS runtime

# Utilisateur non-root dédié.
RUN useradd --create-home --uid 10001 beacon

WORKDIR /app

# Installer uniquement le wheel construit (et ses dépendances).
COPY --from=builder /dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

USER beacon

# ENTRYPOINT fixe la commande ; CMD fournit des arguments par défaut,
# surchargeables au `docker run`.
ENTRYPOINT ["beacon"]
CMD ["check", "--config", "/config/targets.yaml"]

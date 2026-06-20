"""Gestion des credentials : lecture depuis l'environnement, jamais en dur.

Deux garanties :
- un secret requis et absent fait échouer Beacon **immédiatement et clairement**
  (pas un échec obscur plus tard) ;
- aucun secret ne fuit dans les logs : `redact()` masque les jetons avant
  journalisation.

En production, l'environnement provient de l'orchestrateur ou d'un gestionnaire
de secrets. Le code, lui, reste identique — il lit toujours l'environnement.
"""

from __future__ import annotations

import os
import re

ENV_TOKEN = "BEACON_TOKEN"

# Masque "Bearer <token>" et les valeurs de header Authorization.
_BEARER_RE = re.compile(r"(Bearer\s+)\S+", re.IGNORECASE)


class MissingSecretError(RuntimeError):
    """Un secret requis est absent de l'environnement."""


def require_token(env: str = ENV_TOKEN) -> str:
    """Renvoie le token lu dans l'environnement, ou échoue clairement.

    On préfère l'échec explicite au démarrage à un `.get()` silencieux qui
    laisserait la requête partir sans authentification.
    """
    try:
        return os.environ[env]
    except KeyError as e:
        raise MissingSecretError(
            f"Variable d'environnement {env} absente. "
            f"Exporte-la avant de lancer Beacon : export {env}=..."
        ) from e


def auth_headers(token: str) -> dict[str, str]:
    """Construit l'en-tête d'authentification Bearer."""
    return {"Authorization": f"Bearer {token}"}


def redact(message: str) -> str:
    """Masque tout jeton Bearer dans un message destiné aux logs."""
    return _BEARER_RE.sub(r"\1****", message)

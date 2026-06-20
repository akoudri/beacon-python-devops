"""Logging structuré pour Beacon.

Un logger nommé (`beacon`), un événement par sonde avec le contexte en champs
(cible, statut, latence). Le logging structuré rend les logs **requêtables** :
un message libre n'est pas exploitable à grande échelle.

Aucun secret ne doit transiter ici — voir `beacon.secrets.redact`.
"""

from __future__ import annotations

import json
import logging

LOGGER_NAME = "beacon"


class JsonFormatter(logging.Formatter):
    """Formatter émettant chaque ligne en JSON, prête pour une stack de logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname.lower(),
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Champs de contexte passés via `extra=...`.
        for key, value in getattr(record, "context", {}).items():
            payload[key] = value
        return json.dumps(payload)


def configure_logging(level: int = logging.INFO, *, json_format: bool = False) -> None:
    """Configure le logger `beacon` (idempotent)."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.handlers.clear()

    handler = logging.StreamHandler()
    if json_format:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
    logger.addHandler(handler)
    logger.propagate = False


def get_logger() -> logging.Logger:
    """Renvoie le logger `beacon`."""
    return logging.getLogger(LOGGER_NAME)

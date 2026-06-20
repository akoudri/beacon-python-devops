"""Point d'entrée serverless : un handler qui *câble* le cœur de Beacon.

Le handler ne réécrit aucune logique de sonde : il appelle `load_config` et
`probe_all` (lesquels routent vers `probe_http`/`probe`). C'est le dividende
d'un code bien découpé : seul le point d'entrée change.

L'initialisation coûteuse (lecture de la config) est faite **hors** du handler,
une seule fois, puis réutilisée entre invocations « chaudes » — ce qui limite le
cold start.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from beacon.config import Target, load_config
from beacon.probe import probe_all
from beacon.report import build_report

# Cache de la config, peuplé au premier appel (cold start) puis réutilisé.
_TARGETS: list[Target] | None = None


def _get_targets() -> list[Target]:
    global _TARGETS
    if _TARGETS is None:
        config_path = Path(os.environ.get("BEACON_CONFIG", "config/targets.yaml"))
        _TARGETS = load_config(config_path)
    return _TARGETS


def handler(event: dict[str, Any], context: Any = None) -> dict[str, Any]:
    """Handler serverless : sonde les cibles et renvoie un résumé.

    La signature `(event, context)` est celle attendue par AWS Lambda ; la
    logique se transpose à Google Cloud Functions et consorts.
    """
    results = probe_all(_get_targets())
    report = build_report(results)
    all_up = bool(results) and all(r.status == "up" for r in results)

    return {
        "statusCode": 200 if all_up else 503,
        "body": report,
    }

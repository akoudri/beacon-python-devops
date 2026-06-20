"""Sondes : transformer une cible en un résultat structuré.

`probe()` ouvre une connexion TCP, mesure la latence et renvoie un
`ProbeResult`. Le module ne dépend de `config` que pour le type `Target`, et
n'affiche jamais rien : produire la donnée et l'afficher sont deux
responsabilités distinctes.
"""

from __future__ import annotations

import logging
import socket
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from beacon.config import Target

DEFAULT_HTTP_TIMEOUT = 5.0


@dataclass
class ProbeResult:
    """Résultat structuré d'une sonde, consommable par report et métriques."""

    target: str
    status: str  # "up" | "down"
    latency_ms: float
    checked_at: str  # horodatage ISO 8601 (UTC)


def probe(target: Target, timeout: float = 2.0) -> ProbeResult:
    """Sonde une cible TCP et renvoie son statut.

    Une cible injoignable produit `status == "down"` ; aucune exception réseau
    ne remonte au-delà de cette fonction.
    """
    # Chrono démarré avant le try : on veut la latence même sur un échec rapide
    # (un refus immédiat n'a pas la même latence qu'un timeout).
    start = time.perf_counter()
    try:
        with socket.create_connection((target.host, target.port), timeout=timeout):
            status = "up"
    except OSError:
        status = "down"
    latency_ms = (time.perf_counter() - start) * 1000

    return ProbeResult(
        target=target.name,
        status=status,
        latency_ms=round(latency_ms, 2),
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


def probe_http(
    target: Target,
    client: httpx.Client | None = None,
    headers: dict[str, str] | None = None,
) -> ProbeResult:
    """Sonde HTTP : `up` si le service répond avec un statut < 400.

    Le contrat de sortie (`ProbeResult`) est identique à la sonde TCP : report
    et métriques restent inchangés. Toute erreur de transport (timeout, refus,
    DNS) est traduite en `down` — aucune exception ne remonte.

    Args:
        target: cible disposant d'une `url`.
        client: client httpx réutilisable (mutualise les connexions). Optionnel.
        headers: en-têtes additionnels (ex. authentification Bearer). Optionnel.
            Ne jamais journaliser leur contenu — voir `beacon.secrets.redact`.
    """
    if not target.url:
        raise ValueError(f"La cible {target.name!r} n'a pas d'URL à sonder.")

    timeout = target.timeout or DEFAULT_HTTP_TIMEOUT

    # Chrono démarré avant le try : latence mesurée même sur un échec rapide.
    start = time.perf_counter()
    try:
        if client is not None:
            response = client.get(target.url, timeout=timeout, headers=headers)
        else:
            response = httpx.get(target.url, timeout=timeout, headers=headers)
        status = "up" if response.status_code < 400 else "down"
    except httpx.RequestError:
        status = "down"
    latency_ms = (time.perf_counter() - start) * 1000

    return ProbeResult(
        target=target.name,
        status=status,
        latency_ms=round(latency_ms, 2),
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


def probe_all(targets: list[Target], timeout: float = 2.0) -> list[ProbeResult]:
    """Sonde toutes les cibles ; l'échec d'une cible n'interrompt pas les autres.

    Une cible dotée d'une `url` est sondée en HTTP, sinon en TCP. Chaque sonde
    émet un événement de log structuré et alimente les métriques Prometheus.
    """
    # Imports locaux : isolent les dépendances d'observabilité du cœur de sonde
    # et évitent un import circulaire (metrics importe ProbeResult d'ici).
    from beacon import metrics
    from beacon.observability import get_logger

    logger = get_logger()
    results: list[ProbeResult] = []

    for target in targets:
        probe_type = "http" if target.url else "tcp"
        result = probe_http(target) if target.url else probe(target, timeout=timeout)

        metrics.record_probe(result, probe_type)
        level = logging.INFO if result.status == "up" else logging.WARNING
        logger.log(
            level,
            "probe %s -> %s",
            result.target,
            result.status,
            extra={
                "context": {
                    "target": result.target,
                    "status": result.status,
                    "latency_ms": result.latency_ms,
                    "probe_type": probe_type,
                }
            },
        )
        results.append(result)

    metrics.set_targets_up(results)
    return results

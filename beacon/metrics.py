"""Métriques Prometheus exposées par Beacon.

Cadrage : Beacon **expose** des métriques brutes sur `/metrics` ; Prometheus
les collecte et Grafana les affiche. On ne construit pas de tableau de bord en
Python.

Choix des types :
- `Counter` (ne fait que croître) pour le nombre de sondes ;
- `Histogram` pour la distribution des latences ;
- `Gauge` (monte et descend) pour le nombre instantané de cibles up.
"""

from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram, start_http_server

from beacon.probe import ProbeResult

# Label `status` (up/down) et `probe_type` (tcp/http) : faible cardinalité.
PROBES_TOTAL = Counter(
    "beacon_probes_total",
    "Nombre total de sondes effectuées.",
    ["status", "probe_type"],
)

PROBE_LATENCY = Histogram(
    "beacon_probe_latency_seconds",
    "Distribution des latences de sonde (secondes).",
    ["probe_type"],
)

TARGETS_UP = Gauge(
    "beacon_targets_up",
    "Nombre de cibles actuellement up.",
)


def record_probe(result: ProbeResult, probe_type: str) -> None:
    """Alimente compteur et histogramme à partir d'un résultat de sonde."""
    PROBES_TOTAL.labels(status=result.status, probe_type=probe_type).inc()
    PROBE_LATENCY.labels(probe_type=probe_type).observe(result.latency_ms / 1000)


def set_targets_up(results: list[ProbeResult]) -> None:
    """Recalcule la gauge du nombre de cibles up (valeur instantanée)."""
    TARGETS_UP.set(sum(r.status == "up" for r in results))


def serve_metrics(port: int = 9100) -> None:
    """Démarre le serveur d'exposition `/metrics`."""
    start_http_server(port)

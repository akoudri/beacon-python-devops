"""Agrégation : un rapport unifié réseau + cloud.

`report.py` ne fait pas d'I/O réseau ni d'affichage console : il assemble des
résultats déjà collectés (`ProbeResult`, `ResourceState`) en un résumé
structuré, prêt à être sérialisé ou affiché par la CLI.
"""

from __future__ import annotations

from beacon.cloud import ResourceState
from beacon.probe import ProbeResult


def build_report(
    probes: list[ProbeResult],
    resources: list[ResourceState] | None = None,
) -> dict[str, object]:
    """Construit un rapport agrégé des sondes réseau et états cloud."""
    resources = resources or []
    return {
        "probes": {
            "total": len(probes),
            "up": sum(p.status == "up" for p in probes),
            "down": sum(p.status == "down" for p in probes),
            "results": [p.__dict__ for p in probes],
        },
        "cloud": {
            "total": len(resources),
            "results": [r.__dict__ for r in resources],
        },
    }

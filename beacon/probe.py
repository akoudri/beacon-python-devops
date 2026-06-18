from dataclasses import dataclass
from beacon.config import Target
import socket
import time
from datetime import datetime, timezone


@dataclass
class ProbeResult:
    """Résultat structuré d'une sonde, consommable par report et métriques"""

    target: str
    status: str        # "up" | "down"
    latency_ms: float
    checked_at: str    # horodatage ISO 8601


def probe(target : Target, timeout: float = 2.0) -> ProbeResult:
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
        checked_at=datetime.now(timezone.utc).isoformat()
    )

def probe_all(targets : list[Target], timeout: float = 2.0) -> list[ProbeResult]:
    return [probe(target, timeout=timeout) for target in targets]


from dataclasses import dataclass
from beacon.config import Target, ConfigError
import socket
import time
import httpx
from datetime import datetime, timezone

DEFAULT_HTTP_TIMEOUT = 5.0

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

def probe_http(
        target: Target, 
        client: httpx.Client | None = None,
        headers: dict[str, str] | None = None
    ) -> ProbeResult:
    if not target.url:
        raise ConfigError(f"La cibre {target.name} n'a pas d'url à sonder")
    timeout = target.timeout or DEFAULT_HTTP_TIMEOUT
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
        checked_at=datetime.now(timezone.utc).isoformat()
    )

def probe_all(targets : list[Target], timeout: float = 2.0) -> list[ProbeResult]:
    #return [probe(target, timeout=timeout) for target in targets]
    return [
        probe_http(target) if target.url else probe(target, timeout=timeout)
        for target in targets
    ]

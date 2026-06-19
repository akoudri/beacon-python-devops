from beacon.cloud import ResourceState
from beacon.probe import ProbeResult


def build_report(
        probes: list[ProbeResult],
        resources: list[ResourceState]
) -> dict[str, object]:
    return {
        "probes": {
            "total": len(probes),
            "up": sum(p.status == "up" for p in probes),
            "down": sum(p.status == "down" for p in probes),
            "results": [p.__dict__ for p in probes]
        },
        "cloud": {
            "total": len(resources),
            "results": [r.__dict__ for r in resources]
        }
    }
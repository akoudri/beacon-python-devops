"""Tests des métriques Prometheus : alimentation et exposition."""

from prometheus_client import generate_latest

from beacon import metrics
from beacon.probe import ProbeResult


def test_record_probe_increments_counter() -> None:
    before = metrics.PROBES_TOTAL.labels(status="up", probe_type="tcp")._value.get()
    metrics.record_probe(ProbeResult("api", "up", 12.0, "t"), "tcp")
    after = metrics.PROBES_TOTAL.labels(status="up", probe_type="tcp")._value.get()
    assert after == before + 1


def test_set_targets_up_gauge() -> None:
    results = [
        ProbeResult("a", "up", 1.0, "t"),
        ProbeResult("b", "down", 1.0, "t"),
        ProbeResult("c", "up", 1.0, "t"),
    ]
    metrics.set_targets_up(results)
    assert metrics.TARGETS_UP._value.get() == 2


def test_metrics_exposition_contains_series() -> None:
    metrics.record_probe(ProbeResult("api", "up", 5.0, "t"), "http")
    exposition = generate_latest().decode()
    assert "beacon_probes_total" in exposition
    assert "beacon_probe_latency_seconds" in exposition
    assert "beacon_targets_up" in exposition

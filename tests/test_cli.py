"""Tests des codes de sortie de la CLI (extension Lab 4).

On simule l'état des cibles en mockant `probe_all` et `load_config` : aucun
réseau, aucun fichier réel.
"""

import pytest

from beacon import cli
from beacon.config import ConfigError, Target
from beacon.probe import ProbeResult


def _result(name: str, status: str) -> ProbeResult:
    return ProbeResult(target=name, status=status, latency_ms=1.0, checked_at="t")


def test_main_exit_0_all_up(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "load_config", lambda p: [Target("a", "h", 1)])
    monkeypatch.setattr(cli, "probe_all", lambda t: [_result("a", "up")])
    assert cli.main(["check", "--config", "x"]) == 0


def test_main_exit_1_some_down(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli, "load_config", lambda p: [Target("a", "h", 1)])
    monkeypatch.setattr(
        cli, "probe_all", lambda t: [_result("a", "up"), _result("b", "down")]
    )
    assert cli.main(["check", "--config", "x"]) == 1


def test_main_exit_2_config_error(monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(path: object) -> None:
        raise ConfigError("nope")

    monkeypatch.setattr(cli, "load_config", _boom)
    assert cli.main(["check", "--config", "x"]) == 2

"""Tests de `probe` : le réseau réel est mocké à la frontière (la socket)."""

import socket

import httpx
import pytest

from beacon.config import Target
from beacon.probe import ProbeResult, probe, probe_http


def test_probe_up(monkeypatch: pytest.MonkeyPatch) -> None:
    # On substitue la socket LÀ OÙ elle est utilisée (beacon.probe.socket...).
    class _FakeConn:
        def __enter__(self) -> "_FakeConn":
            return self

        def __exit__(self, *exc: object) -> None:
            return None

    monkeypatch.setattr(
        socket, "create_connection", lambda *a, **k: _FakeConn()
    )

    result = probe(Target("api", "127.0.0.1", 8080))
    assert isinstance(result, ProbeResult)
    assert result.status == "up"
    assert result.target == "api"


def test_probe_down(monkeypatch: pytest.MonkeyPatch) -> None:
    def _refuse(*args: object, **kwargs: object) -> None:
        raise OSError("connection refused")

    monkeypatch.setattr(socket, "create_connection", _refuse)

    # probe() doit absorber l'OSError et renvoyer "down", sans lever.
    result = probe(Target("api", "127.0.0.1", 9))
    assert result.status == "down"


def _http_target() -> Target:
    return Target("svc", "example.test", 80, url="http://example.test/health")


@pytest.mark.parametrize(
    ("status_code", "expected"),
    [(200, "up"), (204, "up"), (404, "down"), (500, "down")],
)
def test_probe_http_status_mapping(status_code: int, expected: str) -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(status_code))
    with httpx.Client(transport=transport) as client:
        result = probe_http(_http_target(), client=client)
    assert isinstance(result, ProbeResult)
    assert result.status == expected


def test_probe_http_transport_error_is_down() -> None:
    def _boom(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    with httpx.Client(transport=httpx.MockTransport(_boom)) as client:
        result = probe_http(_http_target(), client=client)
    assert result.status == "down"

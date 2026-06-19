import socket
import pytest

from beacon.config import Target
from beacon.probe import ProbeResult, probe

def test_probe_up(monkeypatch: pytest.MonkeyPatch) -> None:
    class _FakeConn:
        def __enter__(self) -> "_FakeConn":
            return self
        
        def __exit__(self, *exc: object) -> None:
            return None
    monkeypatch.setattr(
        socket, "create_connection", lambda *a, **k: _FakeConn()
    )
    res = probe(Target("api", "127.0.0.1", 8080))
    assert isinstance(res, ProbeResult)
    assert res.status == "up"
    assert res.target == "api"



def test_probe_down(monkeypatch: pytest.MonkeyPatch) -> None:
    def _refuse(*args: object, **kwargs: object) -> None:
        raise OSError("Connection refused")
    
    monkeypatch.setattr(socket, "create_connection", _refuse)
    
    res = probe(Target("api", "127.0.0.1", 8080))
    assert res.status == "down"
    
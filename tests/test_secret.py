import pytest

from beacon.secret import (
    MissingSecretError,
    auth_header,
    redact,
    require_token
)

def test_require_token_present(monkeypatch : pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BEACON_TOKEN", "password123")
    # print(monkeypatch)
    assert require_token() == "password123"


def test_require_token_absent(monkeypatch : pytest.MonkeyPatch) -> None:
    with pytest.raises(MissingSecretError):
        require_token()

def test_auth_header() -> None:
    assert auth_header("xyz") == {"Authorization": "Bearer xyz"}


def test_redact_mask_token() -> None:
    secret = "password123"
    masked = redact(f"Authorization: Bearer {secret}")
    assert secret not in masked
    assert "Bearer *****" in masked


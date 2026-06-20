"""Tests de la gestion des secrets : lecture, en-têtes, redaction."""

import pytest

from beacon.secrets import (
    MissingSecretError,
    auth_headers,
    redact,
    require_token,
)


def test_require_token_present(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BEACON_TOKEN", "abc123")
    assert require_token() == "abc123"


def test_require_token_absent(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BEACON_TOKEN", raising=False)
    with pytest.raises(MissingSecretError):
        require_token()


def test_auth_headers() -> None:
    assert auth_headers("xyz") == {"Authorization": "Bearer xyz"}


def test_redact_masks_bearer_token() -> None:
    secret = "super-secret-value"
    masked = redact(f"Authorization: Bearer {secret}")
    assert secret not in masked
    assert "Bearer ****" in masked

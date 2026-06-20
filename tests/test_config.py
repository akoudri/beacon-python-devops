"""Tests de `load_config` : cas nominal, échecs, et quelques cas limites."""

from pathlib import Path

import pytest

from beacon.config import ConfigError, Target, load_config


def test_load_config_nominal(tmp_path: Path) -> None:
    cfg = tmp_path / "targets.yaml"
    cfg.write_text(
        "targets:\n  - name: api\n    host: 127.0.0.1\n    port: 8080\n",
        encoding="utf-8",
    )
    targets = load_config(cfg)
    assert targets == [Target("api", "127.0.0.1", 8080)]


def test_load_config_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError):
        load_config(tmp_path / "absent.yaml")


def test_load_config_invalid_yaml(tmp_path: Path) -> None:
    cfg = tmp_path / "bad.yaml"
    cfg.write_text("targets: [unclosed\n", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(cfg)


@pytest.mark.parametrize(
    "content",
    [
        "",  # fichier vide -> None
        "autre_cle: 1\n",  # clé 'targets' absente
        "targets: []\n",  # liste vide
        "targets:\n  - name: api\n    host: h\n",  # champ 'port' manquant
    ],
)
def test_load_config_rejects_invalid_structure(tmp_path: Path, content: str) -> None:
    cfg = tmp_path / "c.yaml"
    cfg.write_text(content, encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(cfg)

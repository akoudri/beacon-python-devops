from pathlib import Path
import pytest
from beacon.config import load_config, Target, ConfigError

def test_load_config_nominal(tmp_path : Path) -> None :
    cfg = tmp_path / "targets.yaml"
    cfg.write_text(
        "targets:\n - name: api\n   host: 127.0.0.1\n   port: 8080\n",
        encoding="utf-8"
    )
    targets = load_config(cfg)
    assert targets == [Target("api", "127.0.0.1", 8080)]


def test_load_config_missing_file(tmp_path : Path) -> None :
    with pytest.raises(ConfigError):
        load_config(tmp_path / "absent.yaml")


def test_load_config_invalid_file(tmp_path : Path) -> None :
    cfg = tmp_path / "targets.yaml"
    cfg.write_text(
        "targets:\n - pouet: api\n   host: 127.0.0.1\n   port: 8080\n",
        encoding="utf-8"
    )
    with pytest.raises(ConfigError):
        load_config(cfg)


@pytest.mark.parametrize(
    "content",
    [
        "",
        "pouet: 1\n",
        "targets: []",
        "targets:\n - pouet: api\n   host: 127.0.0.1\n   port: 8080\n"
    ]      
)
def test_load_config_invalid_files(tmp_path : Path, content : str) -> None :
    cfg = tmp_path / "targets.yaml"
    cfg.write_text(
        content,
        encoding="utf-8"
    )
    with pytest.raises(ConfigError):
        load_config(cfg)
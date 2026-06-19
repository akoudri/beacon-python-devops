"""Lecture et validation de la configuration des cibles.

Ce module n'a qu'une responsabilité : transformer un fichier YAML en une liste
d'objets `Target` validés. Il ne fait ni réseau, ni CLI — ces préoccupations
vivent dans `probe.py` et `cli.py`.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


class ConfigError(Exception):
    """Erreur de configuration présentable à l'utilisateur.

    C'est cette exception — et non une `FileNotFoundError` ou une
    `yaml.YAMLError` nue — que la CLI saura afficher proprement.
    """


@dataclass
class Target:
    """Une cible à surveiller : un nom logique et un point réseau.

    `url` et `timeout` sont optionnels : une cible dotée d'une `url` est sondée
    en HTTP (`probe_http`), sinon en TCP (`probe`).
    """

    name: str
    host: str
    port: int
    url: str | None = None
    timeout: float | None = None


def load_config(path: Path) -> list[Target]:
    """Charge et valide la configuration des cibles depuis un fichier YAML.

    Args:
        path: chemin du fichier de configuration.

    Returns:
        La liste des cibles déclarées.

    Raises:
        ConfigError: fichier absent, YAML invalide ou structure incorrecte.
    """
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        raise ConfigError(f"Fichier de configuration {path} introuvable")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError:
        raise ConfigError(f"Fichier YAML {path} invalide")

    if not isinstance(data, dict) or "targets" not in data:
        raise ConfigError(f"Clef 'targets' absente ou fichier {path} vide")

    entries = data["targets"]
    if not isinstance(entries, list) or not entries:
        raise ConfigError("La liste des cibles doit être non vide")

    targets: list[Target] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ConfigError(f"Cible #{index + 1} : un mapping est attendu")
        missing = [field for field in ("name", "host", "port") if field not in entry]
        if missing:
            raise ConfigError(f"Cible #{index + 1} - Champs manquants")
        targets.append(
            Target(
                name=entry["name"],
                host=entry["host"],
                port=entry["port"],
                url=entry.get("url"),
                timeout=entry.get("timeout"),
            )
        )
    return targets

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

    `host`/`port` servent la sonde TCP ; `url` (optionnelle) active la sonde
    HTTP du Lab 5. `timeout` surcharge éventuellement le délai par défaut.
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
    except FileNotFoundError as e:
        raise ConfigError(f"Fichier de configuration introuvable : {path}") from e

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        raise ConfigError(f"YAML invalide dans {path} : {e}") from e

    # Un fichier vide est parsé en `None`, pas en `{}`.
    if not isinstance(data, dict) or "targets" not in data:
        raise ConfigError(f"Clé 'targets' absente ou fichier vide dans {path}.")

    entries = data["targets"]
    if not isinstance(entries, list) or not entries:
        raise ConfigError("'targets' doit être une liste non vide.")

    targets: list[Target] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise ConfigError(f"Cible #{index + 1} : un mapping est attendu.")
        missing = [field for field in ("name", "host", "port") if field not in entry]
        if missing:
            raise ConfigError(
                f"Cible #{index + 1} : champ(s) manquant(s) : {', '.join(missing)}."
            )
        timeout = entry.get("timeout")
        targets.append(
            Target(
                name=entry["name"],
                host=entry["host"],
                port=int(entry["port"]),
                url=entry.get("url"),
                timeout=float(timeout) if timeout is not None else None,
            )
        )

    return targets

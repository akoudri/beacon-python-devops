"""Lecture et validation de la configuration des cibles.

Ce module n'a qu'une responsabilité : transformer un fichier YAML en une liste
d'objets `Target` validés. Il ne fait ni réseau, ni CLI — ces préoccupations
vivront dans `probe.py` et `cli.py`.

Lab 1 — squelette à compléter. Remplace les `TODO` et les `...` par ton code.
"""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError


class ConfigError(Exception):
    """Erreur de configuration présentable à l'utilisateur.

    C'est cette exception — et non une `FileNotFoundError` ou une
    `yaml.YAMLError` nue — que la CLI (cet après-midi) saura afficher proprement.
    """


class Target(BaseModel):
    """Une cible à surveiller : un nom logique et un point réseau.

    Pydantic se charge de valider la présence et le type de chaque champ ; le
    port est en plus contraint à la plage TCP valide.
    """

    model_config = {"extra": "forbid"}

    name: str
    host: str
    port: int = Field(ge=1, le=65535)


class _ConfigFile(BaseModel):
    """Structure attendue du fichier YAML : une clef `targets` non vide."""

    model_config = {"extra": "forbid"}

    targets: list[Target] = Field(min_length=1)


def _format_errors(error: ValidationError) -> str:
    """Transforme les erreurs Pydantic en un message lisible en français."""
    details = []
    for err in error.errors():
        location = ".".join(str(part) for part in err["loc"]) or "(racine)"
        details.append(f"{location} : {err['msg']}")
    return " ; ".join(details)


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

    try:
        config = _ConfigFile.model_validate(data)
    except ValidationError as error:
        raise ConfigError(f"Configuration {path} invalide — {_format_errors(error)}")

    return config.targets

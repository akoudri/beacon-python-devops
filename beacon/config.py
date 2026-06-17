"""Lecture et validation de la configuration des cibles.

Ce module n'a qu'une responsabilité : transformer un fichier YAML en une liste
d'objets `Target` validés. Il ne fait ni réseau, ni CLI — ces préoccupations
vivront dans `probe.py` et `cli.py`.

Lab 1 — squelette à compléter. Remplace les `TODO` et les `...` par ton code.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


class ConfigError(Exception):
    """Erreur de configuration présentable à l'utilisateur.

    C'est cette exception — et non une `FileNotFoundError` ou une
    `yaml.YAMLError` nue — que la CLI (cet après-midi) saura afficher proprement.
    """


@dataclass
class Target:
    """Une cible à surveiller : un nom logique et un point réseau."""

    # TODO : déclarer les trois champs attendus — name (str), host (str), port (int).
    ...


def load_config(path: Path) -> list[Target]:
    """Charge et valide la configuration des cibles depuis un fichier YAML.

    Étapes attendues :
      1. Lire le fichier avec `pathlib` et un encodage explicite (`utf-8`).
         Fichier absent (`FileNotFoundError`) -> lève une `ConfigError` claire.
      2. Parser avec `yaml.safe_load` (jamais `yaml.load`).
         YAML invalide (`yaml.YAMLError`) -> lève une `ConfigError`,
         en chaînant l'exception d'origine (`raise ConfigError(...) from e`).
      3. Valider la structure minimale : clé `targets` présente, liste non vide,
         et chaque entrée possède les champs `name`, `host`, `port`.
      4. Renvoyer la liste des `Target`.

    Indice : `yaml.safe_load` d'un fichier vide renvoie `None`, pas `{}`.

    Args:
        path: chemin du fichier de configuration.

    Returns:
        La liste des cibles déclarées.

    Raises:
        ConfigError: fichier absent, YAML invalide ou structure incorrecte.
    """
    # TODO : implémenter les 4 étapes décrites ci-dessus.
    raise NotImplementedError("Lab 1 : implémente load_config().")

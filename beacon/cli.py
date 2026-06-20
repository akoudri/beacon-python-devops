"""Interface en ligne de commande de Beacon.

`cli.py` est mince : il traduit des arguments en appels au cœur (`config`,
`probe`), choisit un format de sortie et un code de retour. Aucune logique de
sonde ou de parsing ne vit ici.

Convention de code de sortie :
    0 — toutes les cibles sont `up`
    1 — au moins une cible est `down`
    2 — erreur de configuration ou d'usage
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from beacon.config import ConfigError, load_config
from beacon.observability import configure_logging
from beacon.probe import ProbeResult, probe_all

EXIT_OK = 0
EXIT_DOWN = 1
EXIT_CONFIG = 2


def _format_text(results: list[ProbeResult]) -> str:
    lines = [
        f"{r.status.upper():4} {r.target:12} {r.latency_ms:8.2f} ms" for r in results
    ]
    up = sum(r.status == "up" for r in results)
    lines.append(f"--- {up}/{len(results)} cible(s) up ---")
    return "\n".join(lines)


def _format_json(results: list[ProbeResult]) -> str:
    return json.dumps([r.__dict__ for r in results], indent=2)


def _cmd_check(args: argparse.Namespace) -> int:
    targets = load_config(Path(args.config))
    results = probe_all(targets)

    rendered = _format_json(results) if args.format == "json" else _format_text(results)
    print(rendered)

    return EXIT_OK if all(r.status == "up" for r in results) else EXIT_DOWN


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="beacon", description="Sonde l'état des cibles déclarées en configuration."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser(
        "check", help="Sonde toutes les cibles et affiche leur état."
    )
    check.add_argument(
        "--config", default="config/targets.yaml", help="Chemin du fichier de cibles."
    )
    check.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Format de sortie (défaut : text).",
    )
    check.add_argument(
        "--json-logs",
        action="store_true",
        help="Émettre les logs au format JSON (défaut : texte).",
    )
    check.set_defaults(func=_cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée. Renvoie le code de sortie (utilisé par le console_script)."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    configure_logging(json_format=getattr(args, "json_logs", False))
    try:
        exit_code: int = args.func(args)
        return exit_code
    except ConfigError as e:
        print(f"Erreur de configuration : {e}", file=sys.stderr)
        return EXIT_CONFIG


if __name__ == "__main__":
    sys.exit(main())

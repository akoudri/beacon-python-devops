
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from beacon.config import ConfigError, load_config
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

    check = sub.add_parser("check", help="Sonde toutes les cibles et affiche leur état.")
    check.add_argument(
        "--config", default="config/targets.yaml", help="Chemin du fichier de cibles."
    )
    check.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Format de sortie (défaut : text).",
    )
    check.set_defaults(func=_cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Point d'entrée. Renvoie le code de sortie (utilisé par le console_script)."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ConfigError as e:
        print(f"Erreur de configuration : {e}", file=sys.stderr)
        return EXIT_CONFIG


if __name__ == "__main__":
    sys.exit(main())
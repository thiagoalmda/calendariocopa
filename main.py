"""CLI: busca os jogos da Copa na API e gera o calendário .ics.

Uso:
    python main.py                       # busca a API e gera output/copa-2026.ics
    python main.py --output meu.ics
    python main.py --check               # apenas mostra o resumo
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.api_client import APIError
from src.ics_generator import build_calendar, write_ics
from src.loader import load_matches, matches_summary

ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "output" / "copa-2026.ics"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gerador de calendário .ics da Copa do Mundo 2026.")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Caminho do .ics gerado (padrão: {DEFAULT_OUTPUT.relative_to(ROOT)}).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Não escreve arquivo; apenas mostra um resumo dos jogos carregados.",
    )
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()

    try:
        matches, source = load_matches(dict(os.environ))
    except APIError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1

    badge = "🌐 API ao vivo" if source == "api" else "💾 cache local"
    print(f"{badge} • {len(matches)} jogos carregados")
    for phase, count in matches_summary(matches).items():
        print(f"  • {phase}: {count}")

    resolved = sum(1 for m in matches if m.is_fully_resolved)
    print(f"  • Confrontos com ambos os times definidos: {resolved}/{len(matches)}")

    if args.check:
        return 0

    namespace = os.getenv("CALENDAR_NAMESPACE", "worldcup-2026@calendariocopa")
    calendar = build_calendar(matches, namespace=namespace)
    output_path = write_ics(calendar, args.output)

    print(f"\n✅ Arquivo gerado em: {output_path}")
    print("Importe-o no Google Agenda em: Configurações → Importar e exportar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

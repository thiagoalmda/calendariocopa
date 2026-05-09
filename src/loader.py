"""Carrega partidas da football-data.org e normaliza para o formato interno.

Fluxo:
1. Bate na API ao vivo (single source of truth).
2. Em caso de sucesso, persiste a resposta crua em data/cache/matches.json
   para que a execução possa continuar offline em caso de queda da API.
3. Em caso de falha + cache disponível, usa o cache emitindo um aviso.

⚠️ O cache é gerado automaticamente. Não é editável: edição manual seria
desfeita na próxima execução com sucesso na API.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from data.flags import PLACEHOLDER_FLAG, resolve
from src.api_client import APIConfig, APIError, fetch_matches

ROOT = Path(__file__).resolve().parent.parent
CACHE_PATH = ROOT / "data" / "cache" / "matches.json"


# Stages que a API costuma retornar para um Mundial.
STAGE_LABELS: dict[str, str] = {
    "GROUP_STAGE": "Fase de Grupos",
    "PLAY_OFFS": "Repescagem",
    "PRELIMINARY_ROUND": "Rodada Preliminar",
    "ROUND_OF_32": "Trigésimas-de-final",
    "LAST_32": "Trigésimas-de-final",
    "ROUND_OF_16": "Oitavas de Final",
    "LAST_16": "Oitavas de Final",
    "QUARTER_FINALS": "Quartas de Final",
    "SEMI_FINALS": "Semifinais",
    "THIRD_PLACE": "Disputa de 3º Lugar",
    "3RD_PLACE_FINAL": "Disputa de 3º Lugar",
    "FINAL": "Final",
}


@dataclass(frozen=True)
class Match:
    id: str
    phase: str
    round_label: str
    team_a_name: str
    team_a_flag: str
    team_b_name: str
    team_b_flag: str
    kickoff_utc: datetime
    venue: str | None
    status: str
    score: str | None

    @property
    def is_fully_resolved(self) -> bool:
        return self.team_a_flag != PLACEHOLDER_FLAG and self.team_b_flag != PLACEHOLDER_FLAG


def load_matches(env: dict[str, str]) -> tuple[list[Match], str]:
    """Retorna (jogos, origem) onde origem é 'api' ou 'cache'."""
    raw_matches: list[dict[str, Any]]
    source = "api"
    try:
        config = APIConfig.from_env(env)
        raw_matches = fetch_matches(config)
        _save_cache(raw_matches)
    except APIError as exc:
        if not CACHE_PATH.exists():
            raise APIError(
                f"{exc}\n\nNenhum cache local disponível — não há como gerar o calendário. "
                "Configure a chave da API e rode novamente."
            ) from exc
        print(
            f"⚠️  Falha ao consultar a API ({exc}). Usando cache local de "
            f"{_cache_age_human()} atrás. Tente novamente mais tarde para sincronizar.",
            file=sys.stderr,
        )
        raw_matches = _load_cache()
        source = "cache"

    return [_to_match(raw) for raw in raw_matches], source


def _to_match(raw: dict[str, Any]) -> Match:
    home = raw.get("homeTeam") or {}
    away = raw.get("awayTeam") or {}

    team_a_flag, team_a_name = resolve(home.get("tla"), home.get("name"))
    team_b_flag, team_b_name = resolve(away.get("tla"), away.get("name"))

    stage_raw = (raw.get("stage") or "").upper()
    phase = STAGE_LABELS.get(stage_raw, stage_raw.replace("_", " ").title() or "Copa do Mundo")

    matchday = raw.get("matchday")
    group = raw.get("group")
    if group and matchday and stage_raw == "GROUP_STAGE":
        round_label = f"{_humanize_group(group)} - Rodada {matchday}"
    elif group:
        round_label = _humanize_group(group)
    elif matchday:
        round_label = f"{phase} - Jogo {matchday}"
    else:
        round_label = phase

    kickoff_str = raw.get("utcDate")
    if not kickoff_str:
        raise ValueError(f"Partida sem utcDate: {raw.get('id')}")
    kickoff = datetime.strptime(kickoff_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)

    venue = raw.get("venue")
    if isinstance(venue, dict):
        venue = venue.get("name")

    score = _format_score(raw.get("score"))
    status = raw.get("status") or "SCHEDULED"

    return Match(
        id=str(raw["id"]),
        phase=phase,
        round_label=round_label,
        team_a_name=team_a_name,
        team_a_flag=team_a_flag,
        team_b_name=team_b_name,
        team_b_flag=team_b_flag,
        kickoff_utc=kickoff,
        venue=venue if venue else None,
        status=status,
        score=score,
    )


def _humanize_group(group: str) -> str:
    if group.upper().startswith("GROUP_"):
        return f"Grupo {group.split('_', 1)[1]}"
    return group


def _format_score(score: dict[str, Any] | None) -> str | None:
    if not score:
        return None
    full = score.get("fullTime") or {}
    home, away = full.get("home"), full.get("away")
    if home is None or away is None:
        return None
    return f"{home} x {away}"


def _save_cache(raw_matches: list[dict[str, Any]]) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "saved_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "matches": raw_matches,
    }
    CACHE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_cache() -> list[dict[str, Any]]:
    payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return payload["matches"]


def _cache_age_human() -> str:
    payload = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    saved = datetime.strptime(payload["saved_at"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - saved
    hours = int(delta.total_seconds() // 3600)
    if hours < 1:
        return f"{int(delta.total_seconds() // 60)} min"
    if hours < 24:
        return f"{hours} h"
    return f"{hours // 24} d"


def matches_summary(matches: list[Match]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for m in matches:
        summary[m.phase] = summary.get(m.phase, 0) + 1
    return summary

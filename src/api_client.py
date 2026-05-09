"""Cliente HTTP para a football-data.org.

Plano gratuito atende ao caso de uso (Copa do Mundo é uma das competições
liberadas no Free Tier). Cadastro de chave: https://www.football-data.org/client/register
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

BASE_URL = "https://api.football-data.org/v4"
DEFAULT_TIMEOUT = 15
DEFAULT_COMPETITION = "WC"  # FIFA World Cup


class APIError(RuntimeError):
    """Erro ao comunicar com a football-data.org."""


@dataclass(frozen=True)
class APIConfig:
    token: str
    competition: str = DEFAULT_COMPETITION
    season: int | None = None  # ex.: 2026; None usa a temporada vigente

    @classmethod
    def from_env(cls, env: dict[str, str]) -> "APIConfig":
        token = env.get("FOOTBALL_DATA_TOKEN", "").strip()
        if not token:
            raise APIError(
                "Variável FOOTBALL_DATA_TOKEN não definida. "
                "Crie uma chave gratuita em https://www.football-data.org/client/register "
                "e copie .env.example para .env."
            )
        season_raw = env.get("FOOTBALL_DATA_SEASON", "").strip()
        season = int(season_raw) if season_raw else None
        return cls(
            token=token,
            competition=env.get("FOOTBALL_DATA_COMPETITION", DEFAULT_COMPETITION).strip() or DEFAULT_COMPETITION,
            season=season,
        )


def fetch_matches(config: APIConfig) -> list[dict[str, Any]]:
    """Busca todas as partidas da competição configurada.

    Levanta APIError em caso de falha (rede, autenticação, rate limit etc.).
    """
    url = f"{BASE_URL}/competitions/{config.competition}/matches"
    headers = {"X-Auth-Token": config.token}
    params: dict[str, Any] = {}
    if config.season is not None:
        params["season"] = config.season

    try:
        response = requests.get(url, headers=headers, params=params, timeout=DEFAULT_TIMEOUT)
    except requests.RequestException as exc:
        raise APIError(f"Falha de rede ao consultar football-data.org: {exc}") from exc

    if response.status_code in (400, 401) and "token" in response.text.lower():
        raise APIError(
            "Token rejeitado pela API. Confira FOOTBALL_DATA_TOKEN no .env "
            "(gere uma chave em https://www.football-data.org/client/register)."
        )
    if response.status_code == 403:
        raise APIError(
            "Acesso negado (403). Sua chave gratuita pode não ter permissão para esta competição. "
            "Confira o painel em https://www.football-data.org/account."
        )
    if response.status_code == 429:
        raise APIError("Limite de requisições atingido (429). Aguarde alguns minutos e tente de novo.")
    if response.status_code >= 400:
        raise APIError(f"Erro HTTP {response.status_code}: {response.text[:300]}")

    payload = response.json()
    matches = payload.get("matches")
    if not isinstance(matches, list):
        raise APIError("Resposta inesperada da API (campo 'matches' ausente).")
    return matches

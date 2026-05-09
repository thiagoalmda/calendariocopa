"""Mapa de seleções: TLA FIFA -> (emoji da bandeira, nome em PT-BR).

A football-data.org devolve `homeTeam.tla` (sigla FIFA de 3 letras), que é
o identificador estável usado aqui para resolver bandeira e tradução.
Quando uma seleção não está no mapa, exibimos o nome enviado pela API
com uma bandeira genérica.
"""
from __future__ import annotations

PLACEHOLDER_FLAG = "🏳️"

# (emoji, nome PT-BR)
TEAMS: dict[str, tuple[str, str]] = {
    # Anfitriões
    "USA": ("🇺🇸", "Estados Unidos"),
    "MEX": ("🇲🇽", "México"),
    "CAN": ("🇨🇦", "Canadá"),
    # AFC
    "KSA": ("🇸🇦", "Arábia Saudita"),
    "AUS": ("🇦🇺", "Austrália"),
    "KOR": ("🇰🇷", "Coreia do Sul"),
    "IRN": ("🇮🇷", "Irã"),
    "IRQ": ("🇮🇶", "Iraque"),
    "JPN": ("🇯🇵", "Japão"),
    "JOR": ("🇯🇴", "Jordânia"),
    "QAT": ("🇶🇦", "Catar"),
    "UZB": ("🇺🇿", "Uzbequistão"),
    # CAF
    "ALG": ("🇩🇿", "Argélia"),
    "CMR": ("🇨🇲", "Camarões"),
    "CIV": ("🇨🇮", "Costa do Marfim"),
    "EGY": ("🇪🇬", "Egito"),
    "GHA": ("🇬🇭", "Gana"),
    "MAR": ("🇲🇦", "Marrocos"),
    "NGA": ("🇳🇬", "Nigéria"),
    "SEN": ("🇸🇳", "Senegal"),
    "TUN": ("🇹🇳", "Tunísia"),
    # CONCACAF
    "CRC": ("🇨🇷", "Costa Rica"),
    "HON": ("🇭🇳", "Honduras"),
    "JAM": ("🇯🇲", "Jamaica"),
    "PAN": ("🇵🇦", "Panamá"),
    "CUW": ("🇨🇼", "Curaçao"),
    "HAI": ("🇭🇹", "Haiti"),
    # CONMEBOL
    "ARG": ("🇦🇷", "Argentina"),
    "BOL": ("🇧🇴", "Bolívia"),
    "BRA": ("🇧🇷", "Brasil"),
    "CHI": ("🇨🇱", "Chile"),
    "COL": ("🇨🇴", "Colômbia"),
    "ECU": ("🇪🇨", "Equador"),
    "PAR": ("🇵🇾", "Paraguai"),
    "PER": ("🇵🇪", "Peru"),
    "URU": ("🇺🇾", "Uruguai"),
    "VEN": ("🇻🇪", "Venezuela"),
    # OFC
    "NZL": ("🇳🇿", "Nova Zelândia"),
    # UEFA
    "GER": ("🇩🇪", "Alemanha"),
    "AUT": ("🇦🇹", "Áustria"),
    "BEL": ("🇧🇪", "Bélgica"),
    "CRO": ("🇭🇷", "Croácia"),
    "DEN": ("🇩🇰", "Dinamarca"),
    "SCO": ("🏴\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f", "Escócia"),
    "SVK": ("🇸🇰", "Eslováquia"),
    "ESP": ("🇪🇸", "Espanha"),
    "FRA": ("🇫🇷", "França"),
    "GEO": ("🇬🇪", "Geórgia"),
    "HUN": ("🇭🇺", "Hungria"),
    "ENG": ("🏴\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f", "Inglaterra"),
    "ITA": ("🇮🇹", "Itália"),
    "NOR": ("🇳🇴", "Noruega"),
    "NED": ("🇳🇱", "Países Baixos"),
    "POL": ("🇵🇱", "Polônia"),
    "POR": ("🇵🇹", "Portugal"),
    "CZE": ("🇨🇿", "República Tcheca"),
    "ROU": ("🇷🇴", "Romênia"),
    "SRB": ("🇷🇸", "Sérvia"),
    "SWE": ("🇸🇪", "Suécia"),
    "SUI": ("🇨🇭", "Suíça"),
    "TUR": ("🇹🇷", "Turquia"),
    "UKR": ("🇺🇦", "Ucrânia"),
    "WAL": ("🏴\U000e0067\U000e0062\U000e0077\U000e006c\U000e0073\U000e007f", "País de Gales"),
    "IRL": ("🇮🇪", "Irlanda"),
}


def resolve(tla: str | None, fallback_name: str | None = None) -> tuple[str, str]:
    """Retorna (emoji, nome_pt_br). Faz fallback para nome enviado pela API."""
    if tla and tla in TEAMS:
        return TEAMS[tla]
    name = fallback_name or tla or "A definir"
    return PLACEHOLDER_FLAG, name

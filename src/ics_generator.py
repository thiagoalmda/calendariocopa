"""Geração do .ics da Copa.

Cada partida vira um VEVENT com UID estável baseado no ID retornado pela
football-data.org (ex.: match-498675-worldcup-2026@calendariocopa). Como
esse ID é imutável, re-importar o arquivo atualiza o evento existente no
Google Agenda em vez de duplicar.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from icalendar import Calendar, Event

from src.loader import Match

DEFAULT_DURATION = timedelta(hours=2)


def _title(match: Match) -> str:
    return f"{match.team_a_flag} {match.team_a_name} vs {match.team_b_name} {match.team_b_flag}"


def _description(match: Match) -> str:
    lines = [
        f"Fase: {match.phase}",
        f"Rodada: {match.round_label}",
    ]
    if match.venue:
        lines.append(f"Estádio: {match.venue}")
    lines.append(f"Status: {_humanize_status(match.status)}")
    if match.score:
        lines.append(f"Placar: {match.score}")
    lines.append(f"ID da partida: {match.id}")
    if not match.is_fully_resolved:
        lines.append(
            "Os times definitivos serão preenchidos automaticamente "
            "quando você re-importar o arquivo após uma nova execução."
        )
    return "\n".join(lines)


def _humanize_status(status: str) -> str:
    mapping = {
        "SCHEDULED": "Agendado",
        "TIMED": "Confirmado",
        "IN_PLAY": "Em andamento",
        "PAUSED": "Pausado (intervalo)",
        "FINISHED": "Encerrado",
        "POSTPONED": "Adiado",
        "SUSPENDED": "Suspenso",
        "CANCELED": "Cancelado",
        "CANCELLED": "Cancelado",
    }
    return mapping.get(status.upper(), status.title())


def build_calendar(matches: list[Match], namespace: str) -> Calendar:
    cal = Calendar()
    cal.add("prodid", "-//Calendario Copa//github.com/calendariocopa//PT-BR")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", "Copa do Mundo FIFA 2026")
    cal.add("x-wr-timezone", "UTC")
    cal.add("x-wr-caldesc", "Calendário da Copa do Mundo 2026 com atualização automática via API.")

    now = datetime.now(timezone.utc)
    for match in matches:
        event = Event()
        event.add("uid", f"match-{match.id}-{namespace}")
        event.add("summary", _title(match))
        event.add("dtstart", match.kickoff_utc)
        event.add("dtend", match.kickoff_utc + DEFAULT_DURATION)
        event.add("dtstamp", now)
        if match.venue:
            event.add("location", match.venue)
        event.add("description", _description(match))
        event.add("categories", ["Copa do Mundo", match.phase])
        event.add("status", "CANCELLED" if match.status.upper() in {"CANCELED", "CANCELLED"} else "CONFIRMED")
        event.add("transp", "OPAQUE")
        cal.add_component(event)

    return cal


def write_ics(calendar: Calendar, output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(calendar.to_ical())
    return output_path

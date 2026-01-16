from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable


_TS_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # 2026-01-17T06:12:33Z
    (re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?)(?P<z>Z)?\b"), "iso"),
    # 2026-01-17 06:12:33
    (re.compile(r"^(?P<ts>\d{4}-\d{2}-\d{2})[ T](?P<t>\d{2}:\d{2}:\d{2}(?:\.\d+)?)\b"), "ymd"),
    # 06:12:33
    (re.compile(r"^(?P<t>\d{2}:\d{2}:\d{2}(?:\.\d+)?)\b"), "hms"),
]

# session-ish hints
_RE_KV = re.compile(r"\b(?P<k>src|dst|client|server|conn|session|sid)=(?P<v>[^\s\]]+)")
_RE_BRACKET = re.compile(r"\[(?P<body>[^\]]+)\]")


@dataclass
class Event:
    ts: datetime | None
    raw_ts: str | None
    session: str
    level: str | None
    message: str
    line_no: int


def _parse_ts(line: str, *, default_date: datetime | None) -> tuple[datetime | None, str | None, str]:
    s = line.lstrip()
    for pat, kind in _TS_PATTERNS:
        m = pat.match(s)
        if not m:
            continue
        if kind == "iso":
            ts_raw = m.group("ts") + ("Z" if m.group("z") else "")
            ts = datetime.fromisoformat(m.group("ts")).replace(tzinfo=timezone.utc)
            rest = s[m.end() :].lstrip(" -\t")
            return ts, ts_raw, rest

        if kind == "ymd":
            ts_raw = f"{m.group('ts')} {m.group('t')}"
            ts = datetime.fromisoformat(f"{m.group('ts')}T{m.group('t')}")
            rest = s[m.end() :].lstrip(" -\t")
            return ts, ts_raw, rest

        if kind == "hms":
            # if we only have HH:MM:SS, we anchor it to default_date if available
            ts_raw = m.group("t")
            ts = None
            if default_date:
                t = datetime.fromisoformat(f"1970-01-01T{m.group('t')}")
                ts = default_date.replace(hour=t.hour, minute=t.minute, second=t.second, microsecond=t.microsecond)
            rest = s[m.end() :].lstrip(" -\t")
            return ts, ts_raw, rest

    return None, None, line


def _guess_level(text: str) -> str | None:
    m = re.search(r"\b(DEBUG|INFO|WARN|WARNING|ERROR|FATAL|TRACE)\b", text)
    if not m:
        return None
    lvl = m.group(1)
    return "WARN" if lvl == "WARNING" else lvl


def _guess_session(text: str) -> str:
    parts: list[str] = []

    # bracket KV blocks
    for b in _RE_BRACKET.findall(text):
        for m in _RE_KV.finditer(b):
            parts.append(f"{m.group('k')}={m.group('v')}")

    # inline kvs
    for m in _RE_KV.finditer(text):
        parts.append(f"{m.group('k')}={m.group('v')}")

    if not parts:
        return "(none)"

    # keep it stable + short
    uniq: list[str] = []
    seen = set()
    for p in parts:
        if p in seen:
            continue
        seen.add(p)
        uniq.append(p)
        if len(uniq) >= 3:
            break

    return ",".join(uniq)


def parse_events(lines: Iterable[str], *, anchor_date: datetime | None = None) -> list[Event]:
    out: list[Event] = []
    default_date = anchor_date

    for i, line in enumerate(lines, start=1):
        line = line.rstrip("\n")
        ts, ts_raw, rest = _parse_ts(line, default_date=default_date)

        # if we see a full date once, use it to anchor subsequent HH:MM:SS lines
        if ts and ts.tzinfo is None:
            default_date = ts

        lvl = _guess_level(rest)
        session = _guess_session(rest)

        out.append(Event(ts=ts, raw_ts=ts_raw, session=session, level=lvl, message=rest.strip(), line_no=i))

    # stable ordering: timestamp first, else keep file order
    out.sort(key=lambda e: (e.ts is None, e.ts or datetime.min.replace(tzinfo=timezone.utc), e.line_no))
    return out

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .html_report import render_report
from .parser import parse_events


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="logloom", description="log prettifier: parse timestamps/sessions -> timeline")
    p.add_argument("path", help="input log file")
    p.add_argument("--limit", type=int, default=None, help="limit number of events printed")
    p.add_argument("--group", type=str, default="auto", help="(reserved) grouping strategy; v1 uses best-effort")
    p.add_argument("--html", type=str, default=None, help="write self-contained HTML report")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)

    p = Path(args.path)
    if not p.exists():
        print(f"logloom: file not found: {p}", file=sys.stderr)
        return 2

    lines = p.read_text(encoding="utf-8", errors="replace").splitlines(True)
    events = parse_events(lines)

    if args.limit is not None:
        events = events[: max(0, args.limit)]

    # terminal output
    for e in events:
        ts = e.raw_ts or (e.ts.isoformat(timespec="seconds") if e.ts else "")
        lvl = e.level or ""
        print(f"{ts:>24}  {e.session:<28}  {lvl:<5}  {e.message}")

    if args.html:
        out = Path(args.html)
        out.write_text(render_report(events, title=f"logloom • {p.name}"), encoding="utf-8")
        print(f"\nwrote html: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

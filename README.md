# logloom

packet/app log prettifier: turns messy text logs into a clean timeline + optional HTML report.

works best with logs that contain timestamps (ISO-8601, `YYYY-MM-DD HH:MM:SS`, or `HH:MM:SS`).

## install

```bash
python -m pip install -e .
```

## usage

```bash
# pretty-print a log
logloom in.log

# write html report
logloom in.log --html report.html

# limit + group
logloom in.log --limit 300 --group auto
```

## input formats (v1)
- ISO timestamps: `2026-01-17T06:12:33Z ...`
- common timestamps: `2026-01-17 06:12:33 ...`
- short timestamps: `06:12:33 ...`

sessions/grouping is best-effort. v1 tries to detect:
- `src=... dst=...`
- `client=... server=...`
- bracket keyvals like `[conn=ABC]` `[session=123]`

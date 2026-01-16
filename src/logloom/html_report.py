from __future__ import annotations

import html
from datetime import datetime

from .parser import Event


def render_report(events: list[Event], *, title: str = "logloom") -> str:
    def esc(s: str) -> str:
        return html.escape(s, quote=True)

    rows = []
    for e in events:
        ts = e.raw_ts or (e.ts.isoformat(timespec="seconds") if e.ts else "")
        lvl = e.level or ""
        rows.append(
            f"<tr>"
            f"<td class='muted mono'>{esc(ts)}</td>"
            f"<td class='pill mono'>{esc(e.session)}</td>"
            f"<td class='lvl mono'>{esc(lvl)}</td>"
            f"<td class='msg'><code>{esc(e.message)}</code></td>"
            f"</tr>"
        )

    return f"""<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8' />
  <meta name='viewport' content='width=device-width,initial-scale=1' />
  <title>{esc(title)}</title>
  <style>
    :root{{ --bg:#070707; --panel:rgba(255,255,255,.06); --border:rgba(255,255,255,.12);
      --text:#f6f6f6; --muted:#b9b9c2; --pink:#ff78c8; --pink2:#ffb3e6; }}
    body{{ margin:0; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; background:var(--bg); color:var(--text); }}
    .wrap{{ max-width:1120px; margin:0 auto; padding:24px; }}
    .card{{ background:var(--panel); border:1px solid var(--border); border-radius:14px; padding:16px; margin:14px 0; }}
    .muted{{ color:var(--muted); }}
    .mono{{ font-variant-ligatures:none; }}
    table{{ width:100%; border-collapse:collapse; }}
    th,td{{ padding:10px 10px; border-bottom:1px solid rgba(255,255,255,.08); vertical-align:top; }}
    th{{ text-align:left; color:var(--muted); font-weight:600; }}
    code{{ color:var(--pink2); }}
    .pill{{ color:var(--pink2); max-width:280px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
    .lvl{{ width:90px; }}
    .msg{{ width:55%; }}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='card'>
      <h1 style='margin:0 0 8px'>{esc(title)}</h1>
      <div class='muted'>generated {datetime.now().isoformat(timespec='seconds')} • events: {len(events)}</div>
    </div>

    <div class='card'>
      <table>
        <thead>
          <tr><th>time</th><th>session</th><th>lvl</th><th>message</th></tr>
        </thead>
        <tbody>
          {''.join(rows)}
        </tbody>
      </table>
    </div>
  </div>
</body>
</html>"""

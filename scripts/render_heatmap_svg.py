"""Render contribution JSON as an animated, self-contained SVG calendar."""
from __future__ import annotations

import html
import json
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "contributions.json"
OUT_PATH = ROOT / "contrib-heatmap.svg"

WIDTH, HEIGHT = 860, 205
CELL, GAP, STEP = 11, 4, 15
LEFT, TOP = 44, 38
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    days = payload.get("days", [])
    lookup = {date.fromisoformat(d["date"]): d for d in days}
    if not lookup:
        raise RuntimeError("No contribution days found in data/contributions.json")

    end = max(lookup)
    start = end - timedelta(days=364)
    start -= timedelta(days=(start.weekday() + 1) % 7)  # Sunday on or before first day
    stats = payload.get("stats", {})
    total = int(stats.get("total_last_year", 0))
    streak = int(stats.get("current_streak", 0))

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Krish Gupta contribution calendar</title>',
        '<desc id="desc">Contribution activity from the public GitHub profile, revealed box by box.</desc>',
        '<rect width="100%" height="100%" rx="12" fill="#0d1117" stroke="#30363d"/>',
        '<style>text{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}.cell{opacity:0;animation:reveal .45s ease-out forwards}@keyframes reveal{to{opacity:1}}.muted{fill:#8b949e}.bright{fill:#c9d1d9}</style>',
        '<text x="22" y="23" font-size="12" class="bright">GITHUB CONTRIBUTIONS</text>',
        '<text x="838" y="23" font-size="10" text-anchor="end" class="muted">LAST 365 DAYS</text>',
    ]

    # Month labels are positioned on the week containing each month's first day.
    for week in range(53):
        week_start = start + timedelta(days=week * 7)
        label_date = next(
            (week_start + timedelta(days=i) for i in range(7)
             if (week_start + timedelta(days=i)).day == 1),
            None,
        )
        if label_date:
            x = LEFT + week * STEP
            out.append(f'<text x="{x}" y="33" font-size="9" class="muted">{html.escape(label_date.strftime("%b"))}</text>')

    for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
        y = TOP + row * STEP + 9
        out.append(f'<text x="5" y="{y}" font-size="9" class="muted">{label}</text>')

    for week in range(53):
        for row in range(7):
            current = start + timedelta(days=week * 7 + row)
            if current > end:
                continue
            item = lookup.get(current, {})
            count = int(item.get("count", 0))
            level = int(item.get("level", 0))
            if count > 0 and level == 0:
                level = 1 if count < 4 else 2 if count < 7 else 3 if count < 10 else 4
            level = max(0, min(4, level))
            x, y = LEFT + week * STEP, TOP + row * STEP
            delay = (week + row) * 18
            title = f'{count} contribution{"s" if count != 1 else ""} on {current.isoformat()}'
            out.append(
                f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" '
                f'fill="{PALETTE[level]}" style="animation-delay:{delay}ms">'
                f'<title>{html.escape(title)}</title></rect>'
            )

    footer_y = 174
    out.append(f'<text x="22" y="{footer_y}" font-size="11" class="bright">{total:,} contributions</text>')
    out.append(f'<text x="205" y="{footer_y}" font-size="11" class="muted">Current streak: {streak} days</text>')
    out.append('<text x="655" y="174" font-size="9" class="muted">Less</text>')
    for i, color in enumerate(PALETTE):
        out.append(f'<rect x="{687 + i * 15}" y="163" width="11" height="11" rx="3" fill="{color}"/>')
    out.append('<text x="768" y="174" font-size="9" class="muted">More</text>')
    out.append('<text x="22" y="194" font-size="9" class="muted">Source: github.com/users/Krish-labs/contributions</text>')
    out.append('</svg>')

    OUT_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Rendered {OUT_PATH}")


if __name__ == "__main__":
    main()

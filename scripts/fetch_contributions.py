"""Fetch the public GitHub contribution calendar without a personal access token."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "Krish-labs"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = ROOT / "data" / "contributions.json"


def get_count(node) -> int:
    raw = node.get("data-count")
    if raw is not None:
        try:
            return int(raw)
        except ValueError:
            pass
    label = " ".join([
        node.get("aria-label", ""),
        node.get("title", ""),
        node.get_text(" ", strip=True),
    ])
    match = re.search(r"(\d[\d,]*)\s+contributions?", label, re.I)
    if match:
        return int(match.group(1).replace(",", ""))
    return 0


def streaks(days: list[dict]) -> tuple[int, int]:
    counts = {date.fromisoformat(d["date"]): d["count"] for d in days}
    if not counts:
        return 0, 0
    latest = max(counts)
    cursor = latest if counts.get(latest, 0) else latest - timedelta(days=1)
    current = 0
    while counts.get(cursor, 0) > 0:
        current += 1
        cursor -= timedelta(days=1)
    longest = run = 0
    for day in sorted(counts):
        run = run + 1 if counts[day] > 0 else 0
        longest = max(longest, run)
    return current, longest


def main() -> None:
    response = requests.get(
        URL,
        timeout=30,
        headers={"User-Agent": "Krish-labs-profile-art/1.0"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    nodes = soup.select("[data-date][data-level]")
    if not nodes:
        raise RuntimeError(
            "GitHub's contribution cells were not found. The public HTML may "
            "have changed or the request may have been rate-limited."
        )

    by_date: dict[str, dict] = {}
    for node in nodes:
        day = node.get("data-date")
        try:
            date.fromisoformat(day)
        except (TypeError, ValueError):
            continue
        count = get_count(node)
        try:
            level = int(node.get("data-level", 0))
        except ValueError:
            level = 0
        by_date[day] = {
            "date": day,
            "count": count,
            "level": max(0, min(4, level)),
        }

    days = [by_date[key] for key in sorted(by_date)]
    if not days:
        raise RuntimeError("The contribution calendar had no valid dates.")

    today = max(date.fromisoformat(d["date"]) for d in days)
    year_ago = today - timedelta(days=364)
    total = sum(d["count"] for d in days if date.fromisoformat(d["date"]) >= year_ago)
    current_streak, longest_streak = streaks(days)
    best = max(days, key=lambda d: d["count"])
    monthly = Counter()
    for item in days:
        if date.fromisoformat(item["date"]) >= year_ago:
            monthly[item["date"][:7]] += item["count"]

    payload = {
        "username": USERNAME,
        "fetched_on": date.today().isoformat(),
        "days": days,
        "stats": {
            "total_last_year": total,
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best["date"],
            "best_day_count": best["count"],
            "monthly_totals": dict(sorted(monthly.items())),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(days)} contribution days to {OUT}")
    print(f"Last-year contributions: {total}; current streak: {current_streak} days")


if __name__ == "__main__":
    main()

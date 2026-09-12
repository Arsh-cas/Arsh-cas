
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "Arsh-cas"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT = Path("data/contributions.json")


def fetch_contributions():
    response = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    cells = soup.select(
        "td.ContributionCalendar-day[data-date]"
    )

    if not cells:
        raise RuntimeError(
            "No contribution cells found."
        )

    days = []

    for cell in cells:
        day_date = cell.get("data-date")
        level = int(cell.get("data-level", 0))

        days.append({
            "date": day_date,
            "level": level,
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(days, indent=2),
        encoding="utf-8",
    )

    print(f"Saved {len(days)} days to {OUTPUT}")


if __name__ == "__main__":
    fetch_contributions()
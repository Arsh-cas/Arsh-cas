
import json
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

# GitHub-inspired contribution colors.
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
    "#69f0a0",
]

CELL = 12
GAP = 3
STEP = CELL + GAP

LEFT = 12
TOP = 18
LABEL_WIDTH = 32

GRID_X = LEFT + LABEL_WIDTH
GRID_Y = TOP + 20

WIDTH = GRID_X + 53 * STEP + 12
HEIGHT = GRID_Y + 7 * STEP + 65


def load_data():
    with INPUT.open(encoding="utf-8") as f:
        return json.load(f)


def build_svg(days):
    lookup = {item["date"]: item for item in days}

    # Build a 53-week x 7-day grid.
    dates = sorted(lookup.keys())

    if not dates:
        raise RuntimeError("No contribution data found.")

    start = datetime.strptime(dates[0], "%Y-%m-%d").date()

    # Align the first day to Sunday.
    start = start.fromordinal(
        start.toordinal() - (start.weekday() + 1) % 7
    )

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}">',

        "<style>",
        ".cell { animation: reveal 0.45s ease-out both; }",
        "@keyframes reveal {",
        "from { opacity: 0; transform: translateY(-5px); }",
        "to { opacity: 1; transform: translateY(0); }",
        "}",
        "</style>",

        '<rect width="100%" height="100%" rx="12" fill="#0d1117"/>',

        '<text x="12" y="16" fill="#8b949e" '
        'font-family="monospace" font-size="10">'
        'CONTRIBUTIONS'
        '</text>',
    ]

    # Day labels.
    for label, row in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        y = GRID_Y + row * STEP + 9

        svg.append(
            f'<text x="{LEFT}" y="{y}" fill="#8b949e" '
            f'font-family="monospace" font-size="9">'
            f'{label}'
            f'</text>'
        )

    # Contribution cells.
    for week in range(53):
        for day in range(7):
            current = start.fromordinal(
                start.toordinal() + week * 7 + day
            )

            key = current.isoformat()
            item = lookup.get(key, {"count": 0, "level": 0})

            level = max(0, min(5, int(item.get("level", 0))))
            color = PALETTE[level]

            x = GRID_X + week * STEP
            y = GRID_Y + day * STEP

            delay = (week * 7 + day) * 0.004

            svg.append(
                f'<rect class="cell" x="{x}" y="{y}" '
                f'width="{CELL}" height="{CELL}" rx="2" '
                f'fill="{color}" '
                f'style="animation-delay:{delay:.3f}s"/>'
            )

    # Legend.
    legend_y = GRID_Y + 7 * STEP + 20

    svg.append(
        f'<text x="{GRID_X}" y="{legend_y}" '
        'fill="#8b949e" font-family="monospace" font-size="9">'
        'Less'
        '</text>'
    )

    for i, color in enumerate(PALETTE):
        x = GRID_X + 30 + i * STEP

        svg.append(
            f'<rect x="{x}" y="{legend_y - 9}" '
            f'width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{color}"/>'
        )

    svg.append(
        f'<text x="{GRID_X + 30 + 6 * STEP}" '
        f'y="{legend_y}" fill="#8b949e" '
        'font-family="monospace" font-size="9">'
        'More'
        '</text>'
    )

    total = sum(int(item.get("count", 0)) for item in days)

    svg.append(
        f'<text x="{LEFT}" y="{HEIGHT - 12}" '
        'fill="#8b949e" font-family="monospace" font-size="10">'
        'Contribution activity — last year'
        '</text>'
    )
    svg.append("</svg>")

    return "\n".join(svg)


def main():
    days = load_data()
    svg = build_svg(days)

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
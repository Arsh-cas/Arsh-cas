
from pathlib import Path
from xml.sax.saxutils import escape

OUTPUT = Path("info-card.svg")

NAME = "Arshdeep Singh Munde"
ROLE = "Full Stack Developer & AI Builder"
STACK = "C++, Java, Python"
HIGHLIGHTS = "Building web apps and AI projects"


def build_svg():
    width = 490
    height = 300

    rows = [
        ("Name", NAME),
        ("Role", ROLE),
        ("Stack", STACK),
        ("Highlights", HIGHLIGHTS),
    ]

    svg = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" '
        'width="490" height="300" viewBox="0 0 490 300">',
        '<rect width="490" height="300" rx="12" fill="#0d1117"/>',
        '<rect width="490" height="42" rx="12" fill="#161b22"/>',
        '<rect y="30" width="490" height="12" fill="#161b22"/>',

        '<circle cx="20" cy="21" r="6" fill="#ff5f56"/>',
        '<circle cx="40" cy="21" r="6" fill="#ffbd2e"/>',
        '<circle cx="60" cy="21" r="6" fill="#27c93f"/>',

        '<text x="82" y="26" fill="#8b949e" '
        'font-family="monospace" font-size="13">'
        'arshdeep@github ~'
        '</text>',
    ]

    for i, (key, value) in enumerate(rows):
        y = 85 + i * 48

        svg.append(
            f'<text x="28" y="{y}" fill="#58a6ff" '
            f'font-family="monospace" font-size="14">'
            f'{escape(key)}:'
            f'</text>'
        )

        svg.append(
            f'<text x="145" y="{y}" fill="#c9d1d9" '
            f'font-family="monospace" font-size="14">'
            f'{escape(value)}'
            f'</text>'
        )

    svg.append(
        '<text x="28" y="278" fill="#8b949e" '
        'font-family="monospace" font-size="12">'
        'Status: Building cool things'
        '</text>'
    )

    svg.append("</svg>")

    return "\n".join(svg)


if __name__ == "__main__":
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Saved: {OUTPUT}")
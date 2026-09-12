
from pathlib import Path
import os

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
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">',
        '<rect width="490" height="300" rx="12" fill="#0d1117"/>',
        '<rect width="490" height="42" rx="12" fill="#161b22"/>',
        '<rect y="30" width="490" height="12" fill="#161b22"/>',
        '<circle cx="20" cy="21" r="6" fill="#ff5f56"/>',
        '<circle cx="40" cy="21" r="6" fill="#ffbd2e"/>',
        '<circle cx="60" cy="21" r="6" fill="#27c93f"/>',
        '<text x="82" y="26" fill="#8b949e" font-family="monospace" font-size="13">arshdeep@github ~</text>',
    ]

    for i, (key, value) in enumerate(rows):
        y = 85 + i * 48
        delay = i * 0.2

        svg.append(
            f'<g opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'dur="0.4s" begin="{delay}s" fill="freeze"/>'
            f'<text x="28" y="{y}" fill="#58a6ff" '
            f'font-family="monospace" font-size="14">{key}:</text>'
            f'<text x="145" y="{y}" fill="#c9d1d9" '
            f'font-family="monospace" font-size="14">{value}</text>'
            f'</g>'
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
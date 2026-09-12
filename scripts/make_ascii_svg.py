
from pathlib import Path
import html

from PIL import Image


# File paths
INPUT = Path("source-prepped.png")
OUTPUT = Path("arshdeep-ascii.svg")

# ASCII density ramp: bright (sparse) -> dark (dense)
RAMP = " .`:-=+*cs#%@"

# Portrait settings
WIDTH = 100
CHAR_ASPECT = 0.5

# SVG appearance
FONT_SIZE = 10
LINE_HEIGHT = 12
CHAR_WIDTH = 0.6
TEXT_COLOR = "#b8b8b8"


def image_to_ascii(image_path):
    image = Image.open(image_path).convert("L")

    # Preserve the original aspect ratio.
    ratio = image.height / image.width
    height = max(1, round(WIDTH * ratio * CHAR_ASPECT))

    image = image.resize((WIDTH, height))

    pixels = list(image.getdata())
    rows = []

    for y in range(height):
        row = []

        for x in range(WIDTH):
            brightness = pixels[y * WIDTH + x]

            # Dark pixels receive denser characters.
            index = int(
                (255 - brightness)
                / 255
                * (len(RAMP) - 1)
            )

            row.append(RAMP[index])

        rows.append("".join(row))

    return rows


def build_svg(rows):
    width = WIDTH * FONT_SIZE * CHAR_WIDTH
    height = len(rows) * LINE_HEIGHT + 20

    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" '
        'style="background:transparent;">',

        # Preserve every space in the ASCII art.
        '<style>'
        'text { '
        'font-family: "Courier New", monospace; '
        'font-size: 10px; '
        'font-weight: normal; '
        'white-space: pre; '
        '}'
        '</style>',

        "<defs>"
    ]

    # Create a clip path for each row.
    for i in range(len(rows)):
        y = i * LINE_HEIGHT

        svg.append(
            f'<clipPath id="clip{i}">'
            f'<rect x="0" y="{y}" width="0" '
            f'height="{LINE_HEIGHT}">'
            f'<animate attributeName="width" '
            f'from="0" to="{width}" '
            f'dur="2.8s" '
            f'begin="{i * 0.025}s" '
            f'fill="freeze"/>'
            f'</rect>'
            f'</clipPath>'
        )

    svg.append("</defs>")

    # Render each ASCII row.
    for i, row in enumerate(rows):
        y = (i + 1) * LINE_HEIGHT
        escaped = html.escape(row)

        svg.append(
            f'<text x="0" y="{y}" '
            f'fill="{TEXT_COLOR}" '
            f'xml:space="preserve" '
            f'clip-path="url(#clip{i})">'
            f'{escaped}'
            f'</text>'
        )

    svg.append("</svg>")

    return "\n".join(svg)


def main():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Missing {INPUT}. "
            "Run prep_photo.py first."
        )

    rows = image_to_ascii(INPUT)
    svg = build_svg(rows)

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
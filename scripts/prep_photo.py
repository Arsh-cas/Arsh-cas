
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep_photo(input_path):
    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Photo not found: {input_path}")

    output_path = input_path.with_name("source-prepped.png")

    # Remove the background.
    original = Image.open(input_path).convert("RGBA")
    foreground = remove(original)

    # Composite the subject onto a pure white background.
    white_bg = Image.new("RGBA", foreground.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, foreground).convert("RGB")

    # Convert to grayscale.
    gray = cv2.cvtColor(np.array(composited), cv2.COLOR_RGB2GRAY)

    # Enhance local contrast using CLAHE.
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Save the processed image.
    Image.fromarray(enhanced).save(output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python prep_photo.py source-photo.jpg")
        sys.exit(1)

    prep_photo(sys.argv[1])
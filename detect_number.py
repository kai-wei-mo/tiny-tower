import os
import re

import cv2
import numpy as np
from PIL import Image

# Stores templates as {int: (gray_template, w, h)}
DIGIT_TEMPLATES = {}


def load_number_templates(img_dir="imgs"):
    pattern = re.compile(r"^(\d+)\.png$")
    for filename in os.listdir(img_dir):
        match = pattern.match(filename)
        if match:
            digit = int(match.group(1))
            path = os.path.join(img_dir, filename)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                h, w = img.shape
                DIGIT_TEMPLATES[digit] = (img, w, h)
            else:
                print(f"⚠️ Failed to read image: {path}")


# Load on import
load_number_templates()


def get_number_from_image(pil_image, threshold=0.7):
    """
    Identify the best matching number template from a PIL image.

    Args:
        pil_image (PIL.Image): Image containing a number.
        threshold (float): Minimum confidence to accept match.

    Returns:
        int or None: Detected number, or None if no match above threshold.
    """
    image_np = np.array(pil_image.convert("L"))  # Grayscale
    best_match = None
    best_conf = -1.0

    for digit, (template, w, h) in DIGIT_TEMPLATES.items():
        # Template larger than image
        if image_np.shape[0] < h or image_np.shape[1] < w:
            continue  #

        result = cv2.matchTemplate(image_np, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, _, _ = cv2.minMaxLoc(result)

        if max_val > best_conf:
            best_conf = max_val
            best_match = digit

    print(f"Best match: {best_match} with confidence {best_conf:.2f}")

    return best_match if best_conf >= threshold else None

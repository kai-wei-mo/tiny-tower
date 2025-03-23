import os

import cv2
import numpy as np

# Global dictionary to hold templates
TEMPLATES = {}


# Load all templates from imgs directory
def load_templates(template_dir="imgs"):
    for filename in os.listdir(template_dir):
        if filename.endswith(".png"):
            name = os.path.splitext(filename)[
                0
            ]  # Use filename without extension as key
            img_path = os.path.join(template_dir, filename)
            img_color = cv2.imread(img_path, cv2.IMREAD_COLOR)
            img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            w, h = img_gray.shape[::-1]
            TEMPLATES[name] = {"gray": img_gray, "w": w, "h": h}


# Run once at import
load_templates()


def detect_template(name, screenshot_np, screen_width, screen_height, threshold):
    """
    Detects a UI element based on a named template

    Args:
        name (str): template name (e.g., "elevator_red")
        screenshot_np (np.ndarray): screenshot as BGR image
        screen_width (int): width of screen
        screen_height (int): height of screen
        threshold (float): optional confidence threshold

    Returns:
        tuple: (x, y, w, h, confidence) or None if not found or below threshold
    """
    if name not in TEMPLATES:
        raise ValueError(f"Template '{name}' not found.")

    template = TEMPLATES[name]
    screen_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screen_gray, template["gray"], cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    x, y = max_loc
    x = min(max(x, 0), screen_width - template["w"])
    y = min(max(y, 0), screen_height - template["h"])

    print(f"[{name}] Match at ({x}, {y}) with confidence {max_val:.2f}")

    if max_val >= threshold:
        return x, y, template["w"], template["h"], max_val

    return None

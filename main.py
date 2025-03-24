import os
import time

import numpy as np
import pyautogui
from PIL import ImageGrab

from detect_number import get_number_from_image
from detect_template import detect_template
from utils import perform_click

# OPTIONAL: Disable failsafe (only if you're sure)
pyautogui.FAILSAFE = False

screen_width, screen_height = pyautogui.size()
print(f"Detected screen size: {screen_width}x{screen_height}")

threshold = float(os.getenv("THRESHOLD", 0.94))
elevator_speed = float(os.getenv("ELEVATOR_SPEED", 11.25))  # floors per second
interval = float(os.getenv("INTERVAL", 1))  # seconds
vip = bool(os.getenv("VIP", False))

# Which buttons to click every tick
buttons_to_click = ["red_x", "cancel", "continue_button", "elevator_red"]

print("Script running. Mouse will move to detected matches and click.")
print("Press Ctrl+C in terminal to stop.")

try:
    while True:
        time.sleep(interval)

        # Capture screen
        screenshot = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))
        screenshot_np = np.array(screenshot)
        screenshot.save("screenshot.debug.png")

        # Buttons to click
        for name in buttons_to_click:
            result = detect_template(
                name, screenshot_np, screen_width, screen_height, threshold
            )
            if not result:
                print(f"❌ {name} not found or below threshold")
                continue

            x, y, w, h, confidence = result
            center_x = x + w // 2
            center_y = y + h // 2

            print(f"✅ {name} exceeds threshold: {confidence:.2f}")
            print(f"Clicking it at {center_x, center_y}")

            perform_click(center_x, center_y)

        if vip:
            continue

        # Detect speech bubble
        result = detect_template(
            "speech_bubble", screenshot_np, screen_width, screen_height, threshold
        )

        if result:
            x, y, w, h, confidence = result
            if not confidence >= threshold:
                continue

            print(f"Speech bubble found with confidence {confidence}")

            crop_x = x + 19
            crop_y = y + h

            # Crop speech bubble
            crop_x = max(0, min(crop_x, screen_width - 50))
            crop_y = max(0, min(crop_y, screen_height - 50))
            cropped_img = screenshot.crop((crop_x, crop_y, crop_x + 20, crop_y + 14))
            cropped_img.save("speech.debug.png")

            number = get_number_from_image(cropped_img)

            if not number:
                continue

            # Move mouse upwards
            pyautogui.moveRel(0, -60)

            # Hold for time
            pyautogui.mouseDown()
            time.sleep(0.65 * number - 0.1)
            pyautogui.mouseUp()

            while detect_template(
                "elevator_buttons",
                screenshot_np,
                screen_width,
                screen_height,
                threshold,
            ):
                time.sleep(1.1)
                pyautogui.mouseDown()
                pyautogui.mouseUp()

                screenshot = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height))
                screenshot_np = np.array(screenshot)

except KeyboardInterrupt:
    print("Ctrl+C pressed. Exiting.")

finally:
    print("Script terminated.")

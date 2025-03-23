import time

import pyautogui


def perform_click(center_x, center_y):
    """
    Move to the specified coordinates and perform a click
    """
    # Move mouse to position
    pyautogui.moveTo(center_x, center_y, duration=0.25)
    print(f"Moved cursor to position ({center_x}, {center_y})")

    # Click the button
    pyautogui.click()
    print("🖱️ Clicked!")

    # Wait a bit before next detection
    time.sleep(1.0)

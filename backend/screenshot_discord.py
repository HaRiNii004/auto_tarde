import pyautogui
import pygetwindow as gw
import os
import time

# --- CONFIGURATION ---
SAVE_PATHS = {
    "eva_panda": "backend/screenshots/eva_panda",
    "the_mountain": "backend/screenshots/the_mountain"
}
for path in SAVE_PATHS.values():
    os.makedirs(path, exist_ok=True)

# Custom regions for each chat window (left, top, width, height)
CHAT_REGIONS = {
    "the_mountain": (350, 80, 600, 900),   # Mountain on the left
    "eva_panda": (1300, 200, 600, 800)     # EvaPanda on the right
}


def find_discord_windows():
    """Finds and returns the Discord windows for The Mountain (left) and EvaPanda (right)."""
    windows = gw.getWindowsWithTitle("Discord")
    if len(windows) < 2:
        print("🔴 Please open two separate Discord windows (EvaPanda and The Mountain).")
        return None, None

    # Sort windows based on horizontal screen position
    sorted_windows = sorted(windows, key=lambda w: w.left)

    # Assign based on position
    win_mountain = sorted_windows[0]  # Left window
    win_eva = sorted_windows[1]       # Right window

    print(f"✅ The Mountain window assigned (Left): {win_mountain.title} at ({win_mountain.left}, {win_mountain.top})")
    print(f"✅ EvaPanda window assigned (Right): {win_eva.title} at ({win_eva.left}, {win_eva.top})")

    return win_eva, win_mountain


def capture_discord_chat(target_file_path, region_or_window, window_title=None):
    """Captures a Discord chat region or window and saves it to a file."""

    # If a full window object is passed, extract coordinates
    if hasattr(region_or_window, "left"):
        left = region_or_window.left
        top = region_or_window.top
        right = region_or_window.right
        bottom = region_or_window.bottom
        width = right - left
        height = bottom - top
        window_title = window_title or region_or_window.title
    else:
        # region_or_window is already a tuple (left, top, width, height)
        left, top, width, height = region_or_window

    print(f"📸 Capturing {window_title} region: ({left}, {top}, {width}, {height})")

    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    screenshot.save(target_file_path)

    return True



if __name__ == '__main__':
    win_eva, win_mountain = find_discord_windows()
    if win_eva and win_mountain:
        ts = time.strftime("%Y%m%d_%H%M%S")

        # Capture for The Mountain
        mountain_path = os.path.join(SAVE_PATHS["the_mountain"], f"ss_mountain_{ts}.png")
        if capture_discord_chat(mountain_path, CHAT_REGIONS["the_mountain"], "The Mountain"):
            print(f"✅ The Mountain capture saved to: {mountain_path}")
        else:
            print("❌ Failed to capture The Mountain chat box.")

        # Capture for Eva Panda
        eva_path = os.path.join(SAVE_PATHS["eva_panda"], f"ss_eva_{ts}.png")
        if capture_discord_chat(eva_path, CHAT_REGIONS["eva_panda"], "Eva Panda"):
            print(f"✅ Eva Panda capture saved to: {eva_path}")
        else:
            print("❌ Failed to capture Eva Panda chat box.")

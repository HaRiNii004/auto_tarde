import pyautogui
import pygetwindow as gw
import os
import time

# --- CONFIGURATION (Match this path in message_checker.py) ---
SAVE_PATH = "screenshots/raw"
os.makedirs(SAVE_PATH, exist_ok=True)

# Adjust these offsets based on your Discord layout
CHAT_REGION_OFFSETS = {
    'left_offset': 400,
    'top_offset': 80,
    'width_deduction': 420,
    'height_deduction': 150
}


def find_discord_window():
    """Finds and returns the Discord window object."""
    windows = gw.getWindowsWithTitle("Discord")
    if not windows:
        print("🔴 Discord window not found! Please open Discord.")
        return None

    # Choose the first window that is visible and not minimized
    for win in windows:
        if win.visible and not win.isMinimized:
            print(f"✅ Found Discord window: {win.title}")
            return win


    print("🟡 Found Discord window(s) but they are minimized or hidden.")
    return None


def capture_discord_chat(target_file_path, discord_win):
    """
    Captures the chat box and saves it to the target file path.
    Returns True if captured, False otherwise.
    """
    # --- Ensure window is not minimized or covered ---
    if discord_win.isMinimized or not discord_win.visible:
        print("🟡 Discord window is minimized or hidden — skipping screenshot.")
        return False

    # --- Bring Discord to the foreground ---
    try:
        discord_win.activate()
        time.sleep(0.4)  # Give OS time to bring it forward
    except Exception as e:
        print(f"⚠️ Could not focus Discord window: {e}")
        return False

    # --- Calculate capture region ---
    offsets = CHAT_REGION_OFFSETS
    left, top, width, height = discord_win.left, discord_win.top, discord_win.width, discord_win.height

    chat_left = left + offsets['left_offset']
    chat_top = top + offsets['top_offset']
    chat_width = width - offsets['width_deduction']
    chat_height = height - offsets['height_deduction']

    # --- Take screenshot only if Discord is in front ---
    print("📸 Capturing chat area from Discord...")
    screenshot = pyautogui.screenshot(region=(chat_left, chat_top, chat_width, chat_height))
    screenshot.save(target_file_path)
    return True


if __name__ == '__main__':
    # Example usage (won't run when imported)
    discord_win = find_discord_window()
    if discord_win:
        test_file = os.path.join(SAVE_PATH, "test_capture.png")
        if capture_discord_chat(test_file, discord_win):
            print(f"✅ Test capture saved to: {test_file}")
        else:
            print("❌ Failed to capture chat box.")

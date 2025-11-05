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

# Adjust these offsets based on your Discord layout
CHAT_REGION_OFFSETS = {
    'left_offset': 400,
    'top_offset': 80,
    'width_deduction': 420,
    'height_deduction': 150
}

def find_discord_windows():
    """Finds and returns the Discord window objects for eva_panda and the_mountain."""
    windows = gw.getWindowsWithTitle("Discord")
    if len(windows) < 2:
        print("🔴 Please open two Discord windows.")
        return None, None

    # THIS IS A PLACEHOLDER - you might need to adjust this logic
    # It assumes one window has "eva_panda" in the title and the other has "the_mountain"
    # If the titles are just "Discord", you may need to rely on window position
    win_eva = None
    win_mountain = None
    
    # You will need to figure out how to distinguish your windows.
    # For example, if you are using the web version, one might have a different title.
    # If you can't distinguish by title, you'll have to do it by position.
    # For now, we'll assume the first window is eva_panda and the second is the_mountain
    
    print(f"Found {len(windows)} Discord windows.")
    
    # A simple way to distinguish if you can't do it by title is to position them yourself
    # and then use their position. For example, the leftmost window is always eva_panda.
    
    sorted_windows = sorted(windows, key=lambda w: w.left)
    win_eva = sorted_windows[0]
    win_mountain = sorted_windows[1]
    
    print(f"✅ Eva Panda window: {win_eva.title} at ({win_eva.left}, {win_eva.top})")
    print(f"✅ The Mountain window: {win_mountain.title} at ({win_mountain.left}, {win_mountain.top})")

    return win_eva, win_mountain


def capture_discord_chat(target_file_path, discord_win):
    """
    Captures the chat box and saves it to the target file path.
    Returns True if captured, False otherwise.
    """
    if discord_win.isMinimized or not discord_win.visible:
        print(f"🟡 {discord_win.title} is minimized or hidden — skipping.")
        return False

    try:
        discord_win.minimize()
        discord_win.restore()
        time.sleep(1)  # Give OS time to bring it forward
    except Exception as e:
        print(f"⚠️ Could not focus Discord window: {e}")
        return False

    offsets = CHAT_REGION_OFFSETS
    left, top, width, height = discord_win.left, discord_win.top, discord_win.width, discord_win.height

    chat_left = left + offsets['left_offset']
    chat_top = top + offsets['top_offset']
    chat_width = width - offsets['width_deduction']
    chat_height = height - offsets['height_deduction']

    print(f"📸 Capturing chat area from {discord_win.title}...")
    screenshot = pyautogui.screenshot(region=(chat_left, chat_top, chat_width, chat_height))
    screenshot.save(target_file_path)
    return True

if __name__ == '__main__':
    win_eva, win_mountain = find_discord_windows()
    if win_eva and win_mountain:
        ts = time.strftime("%Y%m%d_%H%M%S")
        
        # Capture for Eva Panda
        eva_path = os.path.join(SAVE_PATHS["eva_panda"], f"ss_eva_{ts}.png")
        if capture_discord_chat(eva_path, win_eva):
            print(f"✅ Eva Panda capture saved to: {eva_path}")
        else:
            print("❌ Failed to capture Eva Panda chat box.")

        # Capture for The Mountain
        mountain_path = os.path.join(SAVE_PATHS["the_mountain"], f"ss_mountain_{ts}.png")
        if capture_discord_chat(mountain_path, win_mountain):
            print(f"✅ The Mountain capture saved to: {mountain_path}")
        else:
            print("❌ Failed to capture The Mountain chat box.")

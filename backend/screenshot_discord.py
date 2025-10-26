import pyautogui
import pygetwindow as gw
import time
import datetime
import os

SAVE_PATH = "screenshots/raw"
os.makedirs(SAVE_PATH, exist_ok=True)

# Find the Discord window
windows = gw.getWindowsWithTitle("Discord")
if not windows:
    print("Discord window not found! Please open Discord.")
    exit()

discord_win = windows[0]
print("✅ Found Discord window:", discord_win.title)

while True:
    if discord_win.isMinimized:
        print("🟡 Discord window is minimized, skipping...")
    else:
        # Get window position and size
        left, top, width, height = discord_win.left, discord_win.top, discord_win.width, discord_win.height

        # Define chat box region
        chat_left = left + 400           # adjust based on your Discord layout
        chat_top = top + 80              # skip title bar
        chat_width = width - 420         # rest of window width
        chat_height = height - 150       # exclude bottom input area

        # Capture screenshot of chat box only
        screenshot = pyautogui.screenshot(region=(chat_left, chat_top, chat_width, chat_height))

        # Save with timestamp
        filename = f"{SAVE_PATH}/chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        screenshot.save(filename)
        print(f"💬 Captured chat box: {filename}")

    time.sleep(3)

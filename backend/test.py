import pyautogui
import time

left, top, width, height = 1300, 200, 600, 800  # adjust here
time.sleep(3)
pyautogui.alert("Move your mouse to see the capture area.")
pyautogui.screenshot("test_area.png", region=(left, top, width, height))
print("✅ Saved test screenshot as test_area.png")

import os
import time
import datetime
from PIL import Image
import pytesseract
from screenshot_discord import find_discord_window, capture_discord_chat, SAVE_PATH

# --- CONFIGURATION ---
CHECK_INTERVAL_SECONDS = 5  # delay between captures
OUTPUT_FOLDER = "Extracted_Messages"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

OUTPUT_FILENAME = f"new_discord_messages_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
OUTPUT_PATH = os.path.join(OUTPUT_FOLDER, OUTPUT_FILENAME)

FILE_A = os.path.join(SAVE_PATH, "screenshot_A.png")
FILE_B = os.path.join(SAVE_PATH, "screenshot_B.png")

NEW_MESSAGES_STORAGE = []


# --- OCR AND FILE UTILITIES ---
def get_chat_text(image_path):
    """Extracts and cleans text from an image."""
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # convert to grayscale
        text = pytesseract.image_to_string(img)

        # clean lines
        cleaned_lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 3]
        return cleaned_lines

    except FileNotFoundError:
        return []
    except pytesseract.TesseractNotFoundError:
        print("🔴 Tesseract not found! Please install it and add to PATH.")
        return []


def delete_screenshot(path):
    """Delete a file if it exists."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError as e:
        print(f"Error deleting file {path}: {e}")


def find_new_messages(current_lines, previous_lines):
    """Finds lines that are new compared to the previous capture."""
    new_messages = []
    previous_set = set(previous_lines)
    for line in current_lines:
        if line not in previous_set:
            new_messages.append(line)
            previous_set.add(line)
    return new_messages


def save_new_messages():
    """Save all new messages collected to text file."""
    if not NEW_MESSAGES_STORAGE:
        print("✅ No new messages to save.")
        return

    with open(OUTPUT_PATH, 'a', encoding='utf-8') as f:
        for timestamp, message in NEW_MESSAGES_STORAGE:
            f.write(f"[{timestamp}] {message}\n")

    print(f"\n💾 Saved {len(NEW_MESSAGES_STORAGE)} new messages to {OUTPUT_FILENAME}")
    NEW_MESSAGES_STORAGE.clear()  # reset after saving


# --- MAIN EXECUTION ---
if __name__ == '__main__':
    print("⏳ Starting Discord chat monitoring in 10 seconds...")
    time.sleep(10)

    discord_win = find_discord_window()
    if not discord_win:
        print("❌ Discord window not found. Exiting.")
        exit()

    print("✅ Discord window found. Initializing...")

    # Take initial screenshot A
    if not capture_discord_chat(FILE_A, discord_win):
        print("❌ Failed to take initial screenshot. Exiting.")
        exit()

    previous_text_lines = get_chat_text(FILE_A)
    print(f"📸 Baseline captured ({len(previous_text_lines)} lines). Starting loop...")

    # --- LOOP ---
    try:
        while True:
            # Wait before next capture
            time.sleep(CHECK_INTERVAL_SECONDS)

            # Take new screenshot B
            if not capture_discord_chat(FILE_B, discord_win):
                print("⚠️ Failed to capture new screenshot. Skipping this round.")
                continue

            # Extract text
            current_text_lines = get_chat_text(FILE_B)

            if current_text_lines == previous_text_lines:
                # same content → delete A and move B → A
                delete_screenshot(FILE_A)
                os.replace(FILE_B, FILE_A)
                print("🔁 No new messages. Continuing...", end='\r')
                continue

            # Different → extract new messages
            new_messages = find_new_messages(current_text_lines, previous_text_lines)
            if new_messages:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for msg in new_messages:
                    NEW_MESSAGES_STORAGE.append((timestamp, msg))
                save_new_messages()

            # Update reference: B becomes new A
            delete_screenshot(FILE_A)
            os.replace(FILE_B, FILE_A)
            previous_text_lines = current_text_lines

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
        save_new_messages()
        delete_screenshot(FILE_A)
        delete_screenshot(FILE_B)

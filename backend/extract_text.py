import os
import datetime
from PIL import Image
import pytesseract
from .screenshot_discord import SAVE_PATHS

# --- CONFIGURATION ---
OUTPUT_FOLDER = "backend/Extracted_Messages"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

OUTPUT_FILENAMES = {
    "eva_panda": os.path.join(OUTPUT_FOLDER, "eva_panda_messages.txt"),
    "the_mountain": os.path.join(OUTPUT_FOLDER, "the_mountain_messages.txt"),
}

# --- OCR AND FILE UTILITIES ---
def get_chat_text(image_path):
    """Extracts and cleans text from an image."""
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # convert to grayscale
        text = pytesseract.image_to_string(img)
        cleaned_lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 3]
        return cleaned_lines
    except FileNotFoundError:
        return []
    except pytesseract.TesseractNotFoundError:
        print("🔴 Tesseract not found! Please install it and add to PATH.")
        return []

def find_new_messages(current_lines, previous_lines):
    """Finds lines that are new compared to the previous capture."""
    return [line for line in current_lines if line not in previous_lines]

def save_new_messages(channel_name, messages):
    """Save all new messages for a channel to its text file."""
    if not messages:
        return

    output_path = OUTPUT_FILENAMES[channel_name]
    with open(output_path, 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for message in messages:
            f.write(f"[{timestamp}] {message}\n")
    print(f"💾 Saved {len(messages)} new messages for {channel_name} to {os.path.basename(output_path)}")

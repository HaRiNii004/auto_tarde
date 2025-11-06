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


# --- OCR EXTRACTION ---
def get_chat_text(image_path):
    """Extracts and cleans text from an image."""
    try:
        img = Image.open(image_path)
        img = img.convert("L")  # grayscale
        text = pytesseract.image_to_string(img)
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        return lines
    except FileNotFoundError:
        return []
    except pytesseract.TesseractNotFoundError:
        print("🔴 Tesseract not found! Please install it and add to PATH.")
        return []


# --- GROUPING MESSAGES ---
def group_by_marker(lines, marker):
    """
    Groups OCR-extracted lines by user marker (e.g. 'Chewbacka (The Mountain)').
    Each group includes timestamp, username line, and all message lines
    until the next marker or date header.
    """
    grouped = []
    current_block = []
    pending_timestamp = None

    for line in lines:
        if not line.strip():
            continue

        if any(month in line for month in ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
            if current_block:
                grouped.append("\n".join(current_block))
            current_block = [line]
            pending_timestamp = None
        elif line.startswith("[20"):
            pending_timestamp = line
        elif marker in line:
            if current_block:
                grouped.append("\n".join(current_block))
            
            current_block = []
            if pending_timestamp:
                current_block.append(pending_timestamp)
            current_block.append(line)
            pending_timestamp = None
        elif current_block:
            current_block.append(line)

    if current_block:
        grouped.append("\n".join(current_block))

    return grouped



def find_new_messages(current_blocks, previous_blocks):
    """Finds new grouped messages not seen before."""
    return [block for block in current_blocks if block not in previous_blocks]


def save_new_messages(channel_name, new_blocks):
    """Appends grouped messages to their respective files."""
    if not new_blocks:
        return

    output_path = OUTPUT_FILENAMES[channel_name]

    with open(output_path, "a", encoding="utf-8") as f:
        for block in new_blocks:
            f.write(f"\n{block}\n")
            f.write("-" * 60 + "\n")

    print(f"💾 Saved {len(new_blocks)} grouped messages for {channel_name}.")


def process_channel(image_path, channel_name):
    """Full pipeline: extract, group by marker, compare, and save."""
    current_lines = get_chat_text(image_path)

    # Choose the correct marker for grouping
    if channel_name == "the_mountain":
        marker = "Chewbacka (The Mountain)"
    elif channel_name == "eva_panda":
        marker = "EvaPanda Alerts"
    else:
        print("❌ Unknown channel name.")
        return

    current_blocks = group_by_marker(current_lines, marker)
    print(f"Current blocks for {channel_name}: {current_blocks}")

    output_path = OUTPUT_FILENAMES[channel_name]
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            previous_text = f.read()
        previous_blocks = previous_text.split("-" * 60)
    else:
        previous_blocks = []

    new_blocks = find_new_messages(current_blocks, previous_blocks)
    save_new_messages(channel_name, new_blocks)

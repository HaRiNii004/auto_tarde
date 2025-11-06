
'''
This script processes an extracted text file and groups messages based on sender markers.

It reads an input file, applies the grouping logic from 'extract_text.py',
and saves the organized messages to a new output file.
'''

import os
from extract_text import group_by_marker, OUTPUT_FILENAMES

# --- CONFIGURATION ---
INPUT_FILENAME = OUTPUT_FILENAMES["eva_panda"]
OUTPUT_FILENAME = os.path.join(os.path.dirname(INPUT_FILENAME), "eva_panda_messages_grouped.txt")
MARKER = "Chewbacka (The Mountain)"  # Marker to identify the start of a message block


def clean_and_group_messages(input_path, output_path, marker):
    '''Reads, cleans, and groups messages, then saves them to a file.'''
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            # Split by the 60-char separator used in save_new_messages
            raw_blocks = f.read().split("-" * 60)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return

    # Clean up blocks: remove timestamps and strip whitespace
    cleaned_lines = []
    for block in raw_blocks:
        lines = block.strip().split('\n')
        # Filter out timestamp lines and empty lines
        for line in lines:
            if line.strip() and not line.startswith('[20'):
                cleaned_lines.append(line)

    # Use the existing grouping logic
    grouped_messages = group_by_marker(cleaned_lines, marker)

    # Save the grouped messages
    with open(output_path, 'w', encoding='utf-8') as f:
        for message in grouped_messages:
            f.write(message + '\n\n')

    print(f"Successfully grouped messages saved to {output_path}")


if __name__ == "__main__":
    clean_and_group_messages(INPUT_FILENAME, OUTPUT_FILENAME, MARKER)

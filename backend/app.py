import os
import time
from backend.screenshot_discord import find_discord_windows, capture_discord_chat, SAVE_PATHS
from backend.extract_text import get_chat_text, find_new_messages, save_new_messages, group_by_marker

# --- CONFIGURATION ---
CHECK_INTERVAL_SECONDS = 5  # delay between captures

def run_monitoring():
    print("⏳ Starting Discord chat monitoring in 5 seconds...")
    time.sleep(5)

    win_eva, win_mountain = find_discord_windows()
    if not win_eva or not win_mountain:
        print("❌ Could not find both Discord windows. Exiting.")
        return

    print("✅ Both Discord windows found. Initializing...")

    # State tracking for each channel
    windows = {"eva_panda": win_eva, "the_mountain": win_mountain}
    file_paths = {
        name: {
            'A': os.path.join(SAVE_PATHS[name], f"{name}_A.png"),
            'B': os.path.join(SAVE_PATHS[name], f"{name}_B.png")
        } for name in windows.keys()
    }
    previous_blocks = {name: [] for name in windows.keys()}

    # --- INITIAL CAPTURE ---
    for name, win in windows.items():
        if not capture_discord_chat(file_paths[name]['A'], win):
            print(f"❌ Failed to take initial screenshot for {name}. Exiting.")
            return
        
        if name == "the_mountain":
            marker = "Chewbacka (The Mountain)"
        elif name == "eva_panda":
            marker = "EvaPanda Alerts"
        else:
            marker = "" # Should not happen

        previous_blocks[name] = group_by_marker(get_chat_text(file_paths[name]['A']), marker)
        print(f"📸 Baseline for {name} captured ({len(previous_blocks[name])} blocks).")

    print("\n🚀 Starting monitoring loop... Press Ctrl+C to stop.")

    # --- LOOP ---
    try:
        while True:
            time.sleep(CHECK_INTERVAL_SECONDS)

            for name, win in windows.items():
                path_A = file_paths[name]['A']
                path_B = file_paths[name]['B']

                # 1. Capture Screenshot B
                if not capture_discord_chat(path_B, win):
                    print(f"⚠️ Failed to capture new screenshot for {name}. Skipping.")
                    continue

                # 2. Extract Text from B
                current_lines = get_chat_text(path_B)

                # 3. Group messages
                if name == "the_mountain":
                    marker = "Chewbacka (The Mountain)"
                elif name == "eva_panda":
                    marker = "EvaPanda Alerts"
                else:
                    marker = "" # Should not happen
                
                current_blocks = group_by_marker(current_lines, marker)

                # 4. Compare
                if current_blocks == previous_blocks[name]:
                    # No change
                    os.remove(path_A)
                    os.rename(path_B, path_A)
                    print(f"🔁 No new messages for {name}.", end='\r')
                else:
                    # Content changed
                    new_messages = find_new_messages(current_blocks, previous_blocks[name])
                    if new_messages:
                        save_new_messages(name, new_messages)
                    
                    # Update reference
                    previous_blocks[name] = current_blocks
                    os.remove(path_A)
                    os.rename(path_B, path_A)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
    finally:
        # Clean up screenshot files
        for name in windows.keys():
            for path in file_paths[name].values():
                if os.path.exists(path):
                    os.remove(path)

if __name__ == '__main__':
    run_monitoring()

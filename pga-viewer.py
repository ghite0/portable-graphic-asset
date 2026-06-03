import os
import sys
import curses

def parse_pga(file_path):
    metadata = {"Name": "Image", "Author": "Unknown", "X": 0, "Y": 0, "Pixels": []}
    if not os.path.exists(file_path): 
        return None

    with open(file_path, 'r') as f:
        lines = f.readlines()

    pixel_mode = False
    all_tokens = []
    
    for line in lines:
        line = line.strip()
        if not line: 
            continue
        if line.startswith("Pixels:"):
            pixel_mode = True
            continue
            
        if not pixel_mode:
            if ":" in line:
                key, value = line.split(":", 1)
                key, value = key.strip(), value.strip()
                if key in ["X", "Y"]:
                    metadata[key] = int(value) if value.isnumeric() or (value.startswith('-') and value[1:].isnumeric()) else 0
                elif key == "Name":
                    metadata[key] = value if value else "Image"
                elif key == "Author":
                    metadata[key] = value if value else "Unknown"
        else:
            all_tokens.extend(line.split())
            
    for i in range(0, 100, 10):
        row = all_tokens[i:i+10]
        while len(row) < 10:
            row.append("none")
        metadata["Pixels"].append(row)
            
    return metadata

def color_name_to_ansi(color_name):
    color = color_name.lower().strip()
    
    if color in ["none", "clear", "blank"]:
        return "\033[0m "
        
    color_map = {
        "red":     "\033[48;2;255;0;0m  ",
        "blue":    "\033[48;2;0;0;255m  ",
        "yellow":  "\033[48;2;255;255;0m  ",
        "green":   "\033[48;2;0;255;0m  ",
        "orange":  "\033[48;2;255;165;0m  ",
        "purple":  "\033[48;2;128;0;128m  ",
        "white":   "\033[48;2;255;255;255m  ",
        "black":   "\033[48;2;0;0;0m  ",
        "cyan":    "\033[48;2;0;255;255m  ",
        "magenta": "\033[48;2;255;0;255m  "
    }
    
    return color_map.get(color, "\033[0m ")

def draw_menu(stdscr, selected_idx, files):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    title = "--- PORTABLE GRAPHIC ASSET VIEWER ---"
    stdscr.addstr(1, max(0, (w - len(title)) // 2), title, curses.A_BOLD)
    stdscr.addstr(3, 2, "Use UP/DOWN arrows. Press ENTER to open file. Press 'q' to quit.")
    stdscr.addstr(4, 2, "-" * (w - 4))
    
    if not files:
        stdscr.addstr(6, 4, "No .pga files found in this directory!")
    else:
        for idx, file in enumerate(files):
            if idx == selected_idx:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(6 + idx, 4, f"> {file}")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(6 + idx, 4, f"  {file}")
    stdscr.refresh()

def curses_main(stdscr):
    curses.curs_set(0)
    files = [f for f in os.listdir('.') if f.endswith('.pga')]
    selected_idx = 0
    while True:
        draw_menu(stdscr, selected_idx, files)
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_idx > 0: selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(files) - 1: selected_idx += 1
        elif key in [curses.KEY_ENTER, 10, 13] and files: return files[selected_idx]
        elif key == ord('q'): return None

if __name__ == "__main__":
    target_file = curses.wrapper(curses_main)
    if target_file:
        data = parse_pga(target_file)
        if data:
            print("\033[H\033[J", end="") 
            print("=== PORTABLE GRAPHIC ASSET ===")
            print(f"Name:        {data['Name']}")
            print(f"Author:      {data['Author']}")
            print(f"Coordinates: X={data['X']}, Y={data['Y']}")
            print("==============================")
            
            for row in data['Pixels']:
                row_string = ""
                for pixel in row:
                    row_string += color_name_to_ansi(pixel)
                print(row_string + "\033[0m")
                    
            print("\nPress Enter to exit...")
            input()
        else:
            print("Failed to read data structure.")
    else:
        print("Viewer closed.")

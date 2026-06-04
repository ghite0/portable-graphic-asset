import curses
import os
import sys

def parse_pga(file_path):
    metadata = {}
    pixels = []
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
    if not lines:
        print("Error: Empty file.")
        sys.exit(1)
        
    header_parts = lines[0].split()
    for i in range(0, len(header_parts), 2):
        if i + 1 < len(header_parts):
            key = header_parts[i].replace(':', '')
            val = header_parts[i+1]
            metadata[key] = val
            
    for line in lines[1:]:
        pixels.append(line.split())
        
    return metadata, pixels

def draw_ui(stdscr, file_path):
    curses.curs_set(0)
    curses.start_color()
    
    if curses.COLORS < 256:
        stdscr.addstr(0, 0, "Warning: Your terminal doesn't support 256 colors.")
        stdscr.refresh()
        stdscr.getch()

    for pair_id in range(1, 256):
        curses.init_pair(pair_id, pair_id, pair_id)

    metadata, pixels = parse_pga(file_path)
    
    while True:
        stdscr.clear()
        
        stdscr.addstr(1, 2, "=== PGA IMAGE VIEWER ===", curses.A_BOLD)
        stdscr.addstr(3, 2, f"File:   {os.path.basename(file_path)}")
        stdscr.addstr(4, 2, f"Name:   {metadata.get('name', 'Unknown')}")
        stdscr.addstr(5, 2, f"Author: {metadata.get('author', 'Unknown')}")
        stdscr.addstr(6, 2, f"X Pos:  {metadata.get('x', '0')}")
        stdscr.addstr(7, 2, f"Y Pos:  {metadata.get('y', '0')}")
        stdscr.addstr(9, 2, "Press 'q' to exit.")

        start_y = 3
        start_x = 30
        
        stdscr.addstr(start_y - 1, start_x, "Data:")
        
        for y, row in enumerate(pixels):
            for x, color in enumerate(row):
                try:
                    color_id = int(color)
                    if not (0 <= color_id <= 255):
                        color_id = 16
                except ValueError:
                    color_id = 16
                
                color_attr = curses.color_pair(color_id) if color_id > 0 else curses.color_pair(16)
                
                try:
                    stdscr.addstr(start_y + y, start_x + (x * 2), "  ", color_attr)
                except curses.error:
                    pass 

        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pga_viewer.py <filename.pga>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    curses.wrapper(draw_ui, target_file)

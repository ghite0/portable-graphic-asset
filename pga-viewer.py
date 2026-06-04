import os
import sys
import re

def parse_pga(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return None

    metadata = {}
    
    with open(filename, 'r') as f:
        content = f.read()

    pattern = r'(\w+)\s*=\s*\["(.*?)"\]'
    matches = re.findall(pattern, content, re.DOTALL)

    for key, value in matches:
        if key in ['Name', 'Author', 'Date']:
            metadata[key] = value.strip()
        elif key == 'Data':
            try:
                clean_data = value.replace('\n', ' ').replace('\r', ' ')
                metadata['Data'] = [int(x.strip()) for x in clean_data.split(',') if x.strip()]
            except ValueError:
                print("Error: Invalid pixel data format in .pga file.")
                return None

    return metadata

def display_pga(metadata):
    print("=== Portable Graphic Asset Info ===")
    print(f"Name:   {metadata.get('Name', 'Unknown')}")
    print(f"Author: {metadata.get('Author', 'Unknown')}")
    print(f"Date:   {metadata.get('Date', 'Unknown')}")
    print("===================================\n")

    pixels = metadata.get('Data', [])
    
    if len(pixels) != 256:
        print(f"Error: A PGA image requires exactly 256 pixels. Found {len(pixels)}.")
        return

    for row in range(16):
        row_string = ""
        for col in range(16):
            pixel_index = row * 16 + col
            color_code = pixels[pixel_index]
            
            if not (0 <= color_code <= 255):
                color_code = 0
            
            row_string += f"\033[48;5;{color_code}m  "
            
        row_string += "\033[0m"
        print(row_string)
    print() 

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 pga-viewer.py <filename.pga>")
        sys.exit(1)
        
    pga_file = sys.argv[1]
    
    pga_data = parse_pga(pga_file)
    if pga_data:
        display_pga(pga_data)

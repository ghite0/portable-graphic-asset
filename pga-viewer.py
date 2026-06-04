import sys
import re
import os

os.system('cls' if os.name == 'nt' else 'clear')

def parse_pga(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    metadata = {}
    for key in ['Name', 'Author', 'Date', 'X', 'Y']:
        match = re.search(fr'{key}\s*=\s*\["?(.*?)"?\]', content)
        if match:
            metadata[key] = match.group(1)

    data_match = re.search(r'Data\s*=\s*\[\s*"(.*?)"\s*\]', content, re.DOTALL)
    if data_match:
        raw_data = data_match.group(1)
        pixels = [p.strip() for p in raw_data.replace('\n', '').split(',') if p.strip()]
        metadata['Data'] = pixels
        
    return metadata

def display_pga(metadata):
    print("-" * 40)
    print(f"Asset Name : {metadata.get('Name')}")
    print(f"Author     : {metadata.get('Author')}")
    print(f"Date       : {metadata.get('Date')}")
    print(f"Position   : ({metadata.get('X')}, {metadata.get('Y')})")
    print("-" * 40)
    
    pixels = metadata.get('Data', [])
    if len(pixels) != 100:
        print("Error: Invalid or incomplete pixel data (Expected 100 pixels).")
        return

    for i in range(10):
        row = pixels[i*10:(i+1)*10]
        row_str = ""
        for color_code in row:
            try:
                code = int(color_code)
                row_str += f"\033[48;5;{code}m  \033[0m"
            except ValueError:
                row_str += "  "
        print(row_str)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pga-viewer.py <filename.pga>")
        sys.exit(1)
        
    try:
        meta = parse_pga(sys.argv[1])
        display_pga(meta)
    except FileNotFoundError:
        print(f"Error: File '{sys.argv[1]}' not found.")

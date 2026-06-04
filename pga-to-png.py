import sys
import re
import zlib
import struct

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

def ansi_8bit_to_rgb(code):
    try:
        code = int(code)
    except ValueError:
        return (0, 0, 0)

    standard_colors = [
        (0,0,0), (128,0,0), (0,128,0), (128,128,0), (0,0,128), (128,0,128), (0,128,128), (192,192,192),
        (128,128,128), (255,0,0), (0,255,0), (255,255,0), (0,0,255), (255,0,255), (0,255,255), (255,255,255)
    ]
    if 0 <= code <= 15:
        return standard_colors[code]
    if 16 <= code <= 231:
        code -= 16
        return ((code // 36) * 51, ((code % 36) // 6) * 51, (code % 6) * 51)
    if 232 <= code <= 255:
        gray = (code - 232) * 10 + 8
        return (gray, gray, gray)
    return (0, 0, 0)

def create_png_chunk(tag, data):
    return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", zlib.crc32(tag + data))

def save_png_pure(pixels, filename, scale=20):
    pga_rgb = [ansi_8bit_to_rgb(p) for p in pixels]
    
    src_w, src_h = 10, 10
    out_w, out_h = src_w * scale, src_h * scale
    
    raw_data = bytearray()
    for y in range(out_h):
        raw_data.append(0)
        src_y = y // scale
        for x in range(out_w):
            src_x = x // scale
            r, g, b = pga_rgb[src_y * src_w + src_x]
            raw_data.extend([r, g, b])

    png_signature = b'\x89PNG\r\n\x1a\n'
    
    ihdr_data = struct.pack("!IIBBBBB", out_w, out_h, 8, 2, 0, 0, 0)
    ihdr_chunk = create_png_chunk(b'IHDR', ihdr_data)
    
    idat_chunk = create_png_chunk(b'IDAT', zlib.compress(raw_data))
    img_iend_chunk = create_png_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(png_signature + ihdr_chunk + idat_chunk + img_iend_chunk)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
        
    try:
        metadata = parse_pga(sys.argv[1])
        if len(metadata.get('Data', [])) != 100:
            sys.exit(1)
            
        asset_name = metadata.get('Name', 'output').lower().replace(' ', '_')
        output_filename = f"{asset_name}.png"
        
        save_png_pure(metadata['Data'], output_filename, scale=20)
        
    except FileNotFoundError:
        pass

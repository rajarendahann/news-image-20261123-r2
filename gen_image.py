#!/usr/bin/env python3
import os
import struct
import zlib
import datetime
import math
import random

# 5x7 Bitmap font for rendering text
FONT_5X7 = {
    ' ': [0, 0, 0, 0, 0, 0, 0],
    'A': [0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    'B': [0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E],
    'C': [0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E],
    'D': [0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E],
    'E': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F],
    'F': [0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10],
    'G': [0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0E],
    'H': [0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11],
    'I': [0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E],
    'J': [0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C],
    'K': [0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11],
    'L': [0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F],
    'M': [0x11, 0x1B, 0x15, 0x11, 0x11, 0x11, 0x11],
    'N': [0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11],
    'O': [0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    'P': [0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10],
    'Q': [0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D],
    'R': [0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11],
    'S': [0x0E, 0x11, 0x10, 0x0E, 0x01, 0x11, 0x0E],
    'T': [0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04],
    'U': [0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E],
    'V': [0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04],
    'W': [0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11],
    'X': [0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11],
    'Y': [0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04],
    'Z': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F],
    '0': [0x0E, 0x13, 0x15, 0x15, 0x15, 0x19, 0x0E],
    '1': [0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E],
    '2': [0x0E, 0x11, 0x01, 0x06, 0x08, 0x10, 0x1F],
    '3': [0x1F, 0x01, 0x02, 0x0E, 0x01, 0x11, 0x0E],
    '4': [0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02],
    '5': [0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E],
    '6': [0x0E, 0x10, 0x10, 0x1E, 0x11, 0x11, 0x0E],
    '7': [0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08],
    '8': [0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E],
    '9': [0x0E, 0x11, 0x11, 0x0F, 0x01, 0x01, 0x0E],
    ',': [0x00, 0x00, 0x00, 0x00, 0x06, 0x04, 0x08],
    '.': [0x00, 0x00, 0x00, 0x00, 0x00, 0x06, 0x06],
    ':': [0x00, 0x06, 0x06, 0x00, 0x06, 0x06, 0x00],
    '-': [0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00],
    '/': [0x01, 0x02, 0x04, 0x08, 0x10, 0x00, 0x00],
    '\'': [0x04, 0x04, 0x02, 0x00, 0x00, 0x00, 0x00],
    '&': [0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D],
    '?': [0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04],
}

def draw_rect_filled(img, x1, y1, x2, y2, color, W=1600, H=2000):
    x1 = max(0, min(W - 1, x1))
    x2 = max(0, min(W - 1, x2))
    y1 = max(0, min(H - 1, y1))
    y2 = max(0, min(H - 1, y2))
    if x1 > x2 or y1 > y2:
        return
    r, g, b = color
    for y in range(y1, y2 + 1):
        row = img[y]
        for x in range(x1, x2 + 1):
            idx = x * 3
            row[idx] = r
            row[idx + 1] = g
            row[idx + 2] = b

def draw_line(img, x1, y1, x2, y2, color, thickness=1, W=1600, H=2000):
    if y1 == y2:
        draw_rect_filled(img, min(x1, x2), y1 - thickness // 2, max(x1, x2), y1 + thickness // 2, color, W, H)
    elif x1 == x2:
        draw_rect_filled(img, x1 - thickness // 2, min(y1, y2), x1 + thickness // 2, max(y1, y2), color, W, H)
    else:
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        x, y = x1, y1
        while True:
            draw_rect_filled(img, x, y, x + thickness - 1, y + thickness - 1, color, W, H)
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

def draw_text(img, text, x, y, scale=1, color=(0, 0, 0), W=1600, H=2000):
    cx = x
    for ch in text.upper():
        glyph = FONT_5X7.get(ch) or FONT_5X7['?']
        for row_idx, row_val in enumerate(glyph):
            for col_idx in range(5):
                if (row_val >> (4 - col_idx)) & 1:
                    rx = cx + col_idx * scale
                    ry = y + row_idx * scale
                    draw_rect_filled(img, rx, ry, rx + scale - 1, ry + scale - 1, color, W, H)
        cx += (5 + 1) * scale

def create_chunk(chunk_type, data):
    length = struct.pack('>I', len(data))
    crc = struct.pack('>I', zlib.crc32(chunk_type + data) & 0xffffffff)
    return length + chunk_type + data + crc

def write_png(filename, img, W, H):
    signature = b'\x89PNG\r\n\x1a\n'
    ihdr_data = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    ihdr_chunk = create_chunk(b'IHDR', ihdr_data)
    
    raw_data = bytearray()
    for row in img:
        raw_data.append(0)
        raw_data.extend(row)
        
    compressed = zlib.compress(raw_data, level=6)
    idat_chunk = create_chunk(b'IDAT', compressed)
    iend_chunk = create_chunk(b'IEND', b'')
    
    with open(filename, 'wb') as f:
        f.write(signature)
        f.write(ihdr_chunk)
        f.write(idat_chunk)
        f.write(iend_chunk)

def main():
    random.seed(42)
    W, H = 1600, 2000
    
    # White paper background
    img = [bytearray(b'\xff' * (W * 3)) for _ in range(H)]
    
    margin = 80
    
    # Top metadata bar
    draw_text(img, "VOL. CXXIV NO. 42", margin, margin - 15, scale=2, color=(70, 70, 70))
    draw_text(img, "MONDAY, 23 NOVEMBER 2026", (W // 2) - 170, margin - 15, scale=2, color=(70, 70, 70))
    draw_text(img, "PRICE: $2.00", W - margin - 180, margin - 15, scale=2, color=(70, 70, 70))
    
    draw_line(img, margin, margin + 12, W - margin, margin + 12, (0, 0, 0), thickness=1)

    # Enlarged Masthead Title: THE DAILY LEDGER
    masthead = "THE DAILY LEDGER"
    scale_m = 9
    text_w = len(masthead) * 6 * scale_m
    mx = (W - text_w) // 2
    my = margin + 25
    draw_text(img, masthead, mx, my, scale=scale_m, color=(0, 0, 0))
    
    # Sub-masthead byline / editorial info row
    submeta_y = my + 7 * scale_m + 12
    draw_text(img, "FOUNDED 1894 • THE VOICE OF GLOBAL COMMERCE & INDEPENDENT JOURNALISM", (W // 2) - 460, submeta_y, scale=2, color=(90, 90, 90))
    
    # Thin double rule below masthead
    rule_y = submeta_y + 30
    draw_line(img, margin, rule_y, W - margin, rule_y, (0, 0, 0), thickness=4)
    draw_line(img, margin, rule_y + 6, W - margin, rule_y + 6, (0, 0, 0), thickness=1)
    
    # Red accent rule
    accent_y = rule_y + 18
    draw_line(img, margin, accent_y, W - margin, accent_y, (200, 30, 30), thickness=4)
    
    # Primary Headline & Byline row
    headline_y = accent_y + 30
    draw_text(img, "GLOBAL MARKETS REACH HISTORIC PEAK", margin, headline_y, scale=4, color=(0, 0, 0))
    draw_text(img, "AS TECHNOLOGY GIANTS SURGE IN TRADING", margin, headline_y + 40, scale=4, color=(0, 0, 0))
    
    byline_y = headline_y + 88
    draw_text(img, "BY J. A. VANCE, SENIOR FINANCIAL EDITOR", margin, byline_y, scale=2, color=(110, 110, 110))
    
    # Second Headline
    sec_head_y = byline_y + 35
    draw_text(img, "SECOND LEADING STORY: RENEWABLE ENERGY MILESTONE", margin, sec_head_y, scale=3, color=(20, 20, 20))
    
    sub_y = sec_head_y + 35
    draw_text(img, "International consortium commits record capital to next-generation green infrastructure projects.", margin, sub_y, scale=2, color=(90, 90, 90))
    
    # Divider line before columns
    div_y = sub_y + 35
    draw_line(img, margin, div_y, W - margin, div_y, (0, 0, 0), thickness=2)
    
    # Three text columns with ragged right edges
    col_y_start = div_y + 30
    col_width = 410
    col_gap = 45
    num_cols = 3
    total_cols_width = num_cols * col_width + (num_cols - 1) * col_gap
    start_x = (W - total_cols_width) // 2
    col_height = H - margin - col_y_start - 30
    
    col_titles = ["MARKET ANALYSIS", "GLOBAL TECH IMPACT", "ECONOMIC OUTLOOK"]
    for c in range(num_cols):
        cx = start_x + c * (col_width + col_gap)
        cy = col_y_start
        
        draw_text(img, col_titles[c], cx, cy, scale=2, color=(0, 0, 0))
        draw_line(img, cx, cy + 22, cx + col_width, cy + 22, (120, 120, 120), thickness=1)
        
        cy += 32
        # Determine column bottom limit (leave room for lower right box in column 3)
        current_col_height = col_height
        if c == 2:
            current_col_height = col_height - 350
            
        while cy < col_y_start + current_col_height:
            # Ragged right edges: vary line lengths significantly
            line_w = random.randint(col_width - 150, col_width)
            draw_rect_filled(img, cx, cy, cx + line_w, cy + 6, (110, 110, 110))
            cy += 14
            if random.random() < 0.22:
                cy += 12  # Paragraph gap
                
        if c < num_cols - 1:
            sep_x = cx + col_width + col_gap // 2
            draw_line(img, sep_x, col_y_start, sep_x, col_y_start + col_height, (210, 210, 210), thickness=1)

    # Boxed Section moved to the lower right corner
    box_x1 = start_x + 2 * (col_width + col_gap)
    box_y1 = H - margin - 350
    box_x2 = W - margin
    box_y2 = H - margin - 20
    
    blue_header_color = (30, 90, 180)
    draw_rect_filled(img, box_x1, box_y1, box_x2, box_y2, (240, 246, 255))
    draw_line(img, box_x1, box_y1, box_x2, box_y1, blue_header_color, thickness=3)
    draw_line(img, box_x1, box_y2, box_x2, box_y2, blue_header_color, thickness=3)
    draw_line(img, box_x1, box_y1, box_x1, box_y2, blue_header_color, thickness=3)
    draw_line(img, box_x2, box_y1, box_x2, box_y2, blue_header_color, thickness=3)
    
    banner_h = 35
    draw_rect_filled(img, box_x1, box_y1, box_x2, box_y1 + banner_h, blue_header_color)
    draw_text(img, "MARKET INDICES & WEATHER", box_x1 + 15, box_y1 + 10, scale=2, color=(255, 255, 255))
    
    bx = box_x1 + 20
    by = box_y1 + banner_h + 20
    box_items = [
        "S&P 500: 5,912.45 (+1.2%)",
        "NASDAQ: 18,850.10 (+1.8%)",
        "DOW JONES: 43,450.20 (+0.5%)",
        "FTSE 100: 8,240.12 (-0.3%)",
        "WEATHER: SUNNY 72 F",
    ]
    for item in box_items:
        draw_text(img, item, bx, by, scale=2, color=(20, 20, 20))
        by += 28

    # Output directory handling
    output_dir = os.environ.get('MAKEFUN_OUTPUT_DIR', '.')
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'entry.png')
    
    write_png(out_path, img, W, H)
    print(f"wrote entry.png {W} x {H}")

if __name__ == '__main__':
    main()

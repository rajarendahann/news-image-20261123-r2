#!/usr/bin/env python3
"""Front-page news image generator - stdlib only."""
import os, struct, zlib, datetime

W, H = 1600, 2000
INK = (24, 24, 28); PAPER = (247, 245, 240)
ACCENT = (179, 27, 27); GREY = (110, 110, 118)
LIGHT = (226, 223, 216); SECT = (28, 60, 110)

STORIES = [
    ("WORLD", "Ceasefire talks resume in Geneva as both sides send envoys", 2),
    ("WORLD", "Parliament in Berlin passes sweeping energy transition bill", 2),
    ("WORLD", "Aid convoy reaches flood-hit provinces after weeks of delay", 2),
    ("US", "Senate unveils bipartisan infrastructure funding framework", 2),
    ("US", "Coastal cities adopt new storm-resilience building codes", 2),
    ("US", "Federal appeals court weighs landmark data-privacy case", 2),
    ("ASIA", "Tokyo unveils record robotics investment package", 2),
    ("ASIA", "Monsoon relief operations expand across the subcontinent", 2),
    ("ASIA", "Regional summit opens with trade and climate on agenda", 2),
    ("TECH", "Open-source model releases sharpen cost competition", 2),
    ("TECH", "Chipmakers report record demand for edge AI hardware", 2),
    ("TECH", "Regulators publish first draft rules for agent software", 2),
    ("BUSINESS", "Markets steady as central banks signal patient stance", 2),
    ("BUSINESS", "Shipping rates ease as new routes settle into place", 2),
    ("BUSINESS", "Retail groups report resilient holiday-season outlook", 2),
    ("SPORT", "Title race tightens after dramatic weekend of fixtures", 2),
    ("SPORT", "Underdogs stun champions in continental cup upsets", 2),
    ("SPORT", "Marathon season opens with record field sizes", 2),
    ("CULTURE", "Restored film classics return to festival screens", 2),
    ("CULTURE", "New literary prize celebrates translated fiction", 2),
    ("SCIENCE", "Deep-sea survey catalogs hundreds of new species", 2),
    ("SCIENCE", "Green hydrogen pilot plant hits production milestone", 2),
]
REGIONS = {}
for cat, headline, n in STORIES:
    REGIONS.setdefault(cat, []).append(headline)

COUNTERS = {"stories": len(STORIES), "regions": len(REGIONS), "sources": 14}

FONT = {
 'A':["01110","10001","10001","11111","10001","10001","10001"],
 'B':["11110","10001","10001","11110","10001","10001","11110"],
 'C':["01110","10001","10000","10000","10000","10001","01110"],
 'D':["11110","10001","10001","10001","10001","10001","11110"],
 'E':["11111","10000","10000","11110","10000","10000","11111"],
 'F':["11111","10000","10000","11110","10000","10000","10000"],
 'G':["01110","10001","10000","10111","10001","10001","01110"],
 'H':["10001","10001","10001","11111","10001","10001","10001"],
 'I':["11111","00100","00100","00100","00100","00100","11111"],
 'J':["00111","00010","00010","00010","00010","10010","01100"],
 'K':["10001","10010","10100","11000","10100","10010","10001"],
 'L':["10000","10000","10000","10000","10000","10000","11111"],
 'M':["10001","11011","10101","10101","10001","10001","10001"],
 'N':["10001","11001","10101","10011","10001","10001","10001"],
 'O':["01110","10001","10001","10001","10001","10001","01110"],
 'P':["11110","10001","10001","11110","10000","10000","10000"],
 'Q':["01110","10001","10001","10001","10101","10011","01101"],
 'R':["11110","10001","10001","11110","10100","10010","10001"],
 'S':["01111","10000","10000","01110","00001","00001","11110"],
 'T':["11111","00100","00100","00100","00100","00100","00100"],
 'U':["10001","10001","10001","10001","10001","10001","01110"],
 'V':["10001","10001","10001","10001","10001","01010","00100"],
 'W':["10001","10001","10001","10101","10101","11011","10001"],
 'X':["10001","10001","01010","00100","01010","10001","10001"],
 'Y':["10001","10001","01010","00100","00100","00100","00100"],
 'Z':["11111","00001","00010","00100","01000","10000","11111"],
 '0':["01110","10001","10011","10101","11001","10001","01110"],
 '1':["00100","01100","00100","00100","00100","00100","01110"],
 '2':["01110","10001","00001","00110","01000","10000","11111"],
 '3':["11110","00001","00001","01110","00001","00001","11110"],
 '4':["00010","00110","01010","10010","11111","00010","00010"],
 '5':["11111","10000","11110","00001","00001","10001","01110"],
 '6':["01110","10000","10000","11110","10001","10001","01110"],
 '7':["11111","00001","00010","00100","01000","01000","01000"],
 '8':["01110","10001","10001","01110","10001","10001","01110"],
 '9':["01110","10001","10001","01111","00001","00001","01110"],
 ' ':["00000"]*7, '.':["00000","00000","00000","00000","00000","00110","00110"],
 ',':["00000","00000","00000","00000","00110","00100","01000"],
 '-':["00000","00000","00000","01110","00000","00000","00000"],
 ':':["00000","00110","00110","00000","00110","00110","00000"],
 '/':["00001","00010","00010","00100","01000","01000","10000"],
 "'":["00100","00100","00000","00000","00000","00000","00000"],
 '(':["00010","00100","01000","01000","01000","00100","00010"],
 ')':["01000","00100","00010","00010","00010","00100","01000"],
 '&':["01100","10010","10100","01000","10101","10010","01101"],
 '%':["10001","00010","00100","01000","00100","01000","10001"],
 '•':["00000","00000","01100","01100","00000","00000","00000"],
}

buf = bytearray()
for _ in range(H * W * 3):
    buf.extend(b'\xf7\xf5\xf0')

def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i] = c[0]; buf[i+1] = c[1]; buf[i+2] = c[2]

def rect(x0, y0, x1, y1, c):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            px(x, y, c)

def hline(x0, x1, y, c, t=1):
    rect(x0, y, x1, y + t, c)

def text(x, y, s, c, scale=2):
    cx = x
    for ch in s.upper():
        g = FONT.get(ch, FONT[' '])
        for r, row in enumerate(g):
            for col, b in enumerate(row):
                if b == '1':
                    rect(cx + col*scale, y + r*scale, cx + col*scale + scale, y + r*scale + scale, c)
        cx += 6 * scale
    return cx

def center(s, y, c, scale):
    w = len(s) * 6 * scale
    text(max(0, (W - w)//2), y, s, c, scale)

today = datetime.date.today().strftime("%B %-d, %Y")

# masthead
hline(40, W-40, 40, ACCENT, 6)
center("THE FRONT PAGE", 90, INK, 9)
center(today, 260, GREY, 5)
center("%d STORIES  •  %d REGIONS  •  %d SOURCES" % (COUNTERS['stories'], COUNTERS['regions'], COUNTERS['sources']), 360, ACCENT, 3)
hline(40, W-40, 430, INK, 4)

# region sections: 2 columns of story cards
y = 470
pairs = list(REGIONS.items())
cards = []
ci = 0
for cat, heads in pairs:
    cards.append((cat, heads)); 
# 3 big story cards (first 3 regions' first headlines)
y0 = 470
rect(40, y0, W-40, y0+180, (240, 236, 228))
x = 60
for k in range(3):
    cat, heads = cards[k]
    rect(x, y0+20, x+480, y0+160, (255, 253, 248))
    text(x+20, y0+40, cat, ACCENT, 4)
    words = heads[0].split()
    lines, cur = [], ""
    for w_ in words:
        if len(cur)+len(w_)+1 <= 34: cur = (cur+" "+w_).strip()
        else: lines.append(cur); cur = w_
    lines.append(cur)
    yy = y0+95
    for ln in lines[:2]:
        text(x+20, yy, ln, INK, 2); yy += 26
    x += 500
y = y0 + 220

# remaining regions: 3x3 grid of small cards
rest = cards[3:12]
for gi, (cat, heads) in enumerate(rest):
    r_, c_ = divmod(gi, 3)
    gx = 40 + c_*520; gy = y + r_*170
    rect(gx, gy, gx+500, gy+150, (240, 236, 228))
    rect(gx, gy, gx+12, gy+150, SECT)
    text(gx+30, gy+18, cat, SECT, 3)
    words = heads[0].split()
    lines, cur = [], ""
    for w_ in words:
        if len(cur)+len(w_)+1 <= 36: cur = (cur+" "+w_).strip()
        else: lines.append(cur); cur = w_
    lines.append(cur)
    yy = gy+62
    for ln in lines[:3]:
        text(gx+30, yy, ln, INK, 2); yy += 24

rows_used = (len(rest) + 2) // 3
y = y + max(1, rows_used) * 170 + 40

# world map with dots (equirectangular-ish schematic)
map_y = y; map_h = 320
rect(40, map_y, W-40, map_y+map_h, (232, 236, 244))
text(60, map_y+16, "WORLD AT A GLANCE", SECT, 3)
import math
# simple continent blobs
for blob in [(150,60,420,200),(430,70,620,190),(640,150,760,260),(790,70,1010,190),(1040,90,1260,230),(1300,110,1560,280)]:
    rect(blob[0]+40, blob[1]+map_y+40, blob[2]+40, blob[3]+map_y+40, (214, 220, 232))
for cx_, cy_ in [(320,120),(520,100),(700,140),(980,110),(1200,160),(1380,130),(300,200),(760,220),(1100,210),(1420,240),(450,180),(880,180)]:
    cx_ += 40; cy_ += map_y+40
    rect(cx_-6, cy_-6, cx_+6, cy_+6, ACCENT)

y = map_y + map_h + 40

# ALSO-ON list
text(40, y, "ALSO ON THE FRONT PAGE", ACCENT, 4)
y += 60
extras = ["Weather bureau forecasts colder week across northern plains",
          "Transit agency adds late-night service on key metro lines",
          "University team publishes open dataset on urban air quality"]
for e in extras:
    rect(40, y, W-40, y+56, (240, 236, 228))
    rect(40, y, 52, y+56, ACCENT)
    text(70, y+16, e, INK, 2)
    y += 66

# footer
fy = H - 90
hline(40, W-40, fy, INK, 3)
center("DATE CHECK: %s  •  SOURCES: PUBLIC WIRE REPORTS (14)" % today, fy+30, GREY, 2)

# ---- PNG encode ----
def png_bytes():
    raw = bytearray()
    for row in range(H):
        raw.append(0)
        raw.extend(buf[row*W*3:(row+1)*W*3])
    comp = zlib.compress(bytes(raw), 6)
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', comp) + chunk(b'IEND', b'')

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "entry.png"), "wb") as f:
    f.write(png_bytes())
print("wrote entry.png", W, "x", H)

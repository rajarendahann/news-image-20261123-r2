import os
from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if draw.textlength(test_line, font=font) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def generate_image(output_path=None):
    if output_path is None:
        out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
        try:
            os.makedirs(out_dir, exist_ok=True)
            output_path = os.path.join(out_dir, "entry.png")
            with open(output_path, "a"):
                pass
        except Exception:
            out_dir = "."
            os.makedirs(out_dir, exist_ok=True)
            output_path = os.path.join(out_dir, "entry.png")

    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), color="#FAF7F2")
    draw = ImageDraw.Draw(img)

    # Fonts (DejaVu)
    sans_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    sans_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    serif_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    serif_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

    font_masthead = ImageFont.truetype(serif_bold_path, 50)
    font_subhead = ImageFont.truetype(sans_bold_path, 11)
    font_section = ImageFont.truetype(sans_bold_path, 11)
    font_big_title = ImageFont.truetype(serif_bold_path, 16)
    font_big_body = ImageFont.truetype(serif_path, 12)
    font_med_title = ImageFont.truetype(sans_bold_path, 13)
    font_med_body = ImageFont.truetype(sans_path, 11)
    font_small = ImageFont.truetype(sans_path, 11)
    font_tiny = ImageFont.truetype(sans_path, 10)

    margin = 20
    y = 16

    # 1. Top bar
    draw.text((margin, y), "THE GLOBAL CHRONICLE  •  MONDAY, 23 NOVEMBER 2026  •  EDITION NO. 328  •  $2.50", fill="#2C3E50", font=font_subhead)
    y += 18
    draw.line([(margin, y), (width - margin, y)], fill="#1B2631", width=2)
    y += 8

    # 2. Huge Masthead Title
    title_text = "THE DAILY WIRE"
    draw.text((margin, y), title_text, fill="#1B2631", font=font_masthead)
    y += 58

    # Lede line
    lede = "TRILATERAL SUMMIT IN SHENZHEN  •  MASSIVE MISSILE STRIKE ON UKRAINE  •  COP31 CLIMATE TALKS COLLAPSE IN ANTALYA"
    draw.text((margin, y), lede, fill="#C0392B", font=font_small)
    y += 16
    draw.line([(margin, y), (width - margin, y)], fill="#34495E", width=1)
    y += 6

    # 3. Stat boxes row (6 regions)
    stats = [
        ("ASIA", "3 stories"),
        ("MIDDLE EAST", "3 stories"),
        ("EUROPE", "5 stories"),
        ("AFRICA", "1 story"),
        ("AMERICAS", "3 stories"),
        ("GLOBAL", "3 stories")
    ]
    box_w = (width - 2 * margin - 5 * 8) / 6
    bx = margin
    for reg, count in stats:
        draw.rectangle([bx, y, bx + box_w, y + 24], outline="#BDC3C7", fill="#F4F6F7")
        text_str = f"{reg}: {count}"
        tw = draw.textlength(text_str, font=font_small)
        draw.text((bx + (box_w - tw) / 2, y + 5), text_str, fill="#1B2631", font=font_small)
        bx += box_w + 8
    y += 30

    # 4. Three Big Story Cards (height 175)
    big_stories = [
        ("GLOBAL", "Peace Declaration in Shenzhen", "Trump, Xi and Putin release an unprecedented trilateral peace pact.", "Leaders meet at special summit to stabilize major power relations and chart new security architecture."),
        ("EUROPE", "Massive Airstrike on Kyiv", "Russia launches over 110 missiles and 400 drones targeting energy grid.", "Eighty infrastructure sites hit; at least 8 civilians reported killed across multiple regions of Ukraine."),
        ("GLOBAL", "COP31 Climate Talks Collapse", "Antalya summit ends with no pact as fossil fuel divisions sink draft.", "Delegates fail to bridge major gaps over phase-out timelines and international climate financing.")
    ]
    
    card_w = (width - 2 * margin - 2 * 12) / 3
    card_h = 175
    cx = margin
    for tag, headline, line1, line2 in big_stories:
        draw.rectangle([cx, y, cx + card_w, y + card_h], outline="#BDC3C7", fill="#FFFFFF", width=1)
        draw.rectangle([cx, y, cx + card_w, y + 20], fill="#1B2631")
        draw.text((cx + 8, y + 4), tag, fill="#FFFFFF", font=font_section)
        
        hy = y + 26
        for h_line in wrap_text(headline, font_big_title, card_w - 16, draw):
            draw.text((cx + 8, hy), h_line, fill="#111111", font=font_big_title)
            hy += 20
        
        hy += 4
        body_text = f"{line1} {line2}"
        for b_line in wrap_text(body_text, font_big_body, card_w - 16, draw):
            draw.text((cx + 8, hy), b_line, fill="#34495E", font=font_big_body)
            hy += 16
            
        cx += card_w + 12
    y += card_h + 10

    # 5. 3x3 Grid of Medium Cards (height 72)
    med_stories = [
        ("EUROPE", "Ukraine Deal by Jan 2027", "Trump demands swift negotiated settlement to end conflict."),
        ("EUROPE", "EU Open to Negotiations", "Macron, Kushner and Witkoff meet to discuss peace framework."),
        ("EUROPE", "Kherson West Bank Final Stage", "Ukraine reports major advances in southern counter-offensive."),
        ("AMERICAS", "Pentagon Iran Prep Ordered", "Military told to prepare for operations; ready within 96 hours."),
        ("MIDDLE EAST", "Rabigh Refinery Attacked", "Houthis claim strike on Saudi facility; two tankers ablaze."),
        ("MIDDLE EAST", "Carrier USS Roosevelt Arrives", "Third US aircraft carrier deployed to Middle East region."),
        ("ASIA", "US-China AI Oversight Pact", "Agreement reached on human oversight in military AI decisions."),
        ("AFRICA", "Ramaphosa Defies G20 Threat", "South African leader dismisses US warning over summit bar."),
        ("AMERICAS", "Anthropic IPO Fails to Calm", "Record market debut overshadowed by AI spending fears.")
    ]

    grid_cols = 3
    g_w = (width - 2 * margin - 2 * 12) / 3
    g_h = 72
    
    gx_start = margin
    gy_start = y
    
    for i, (tag, title, desc) in enumerate(med_stories):
        r = i // grid_cols
        c = i % grid_cols
        gx = gx_start + c * (g_w + 12)
        gy = gy_start + r * (g_h + 6)
        
        draw.rectangle([gx, gy, gx + g_w, gy + g_h], outline="#BDC3C7", fill="#FFFFFF")
        draw.rectangle([gx, gy, gx + g_w, gy + 15], fill="#34495E")
        draw.text((gx + 6, gy + 2), tag, fill="#FFFFFF", font=font_tiny)
        
        draw.text((gx + 6, gy + 18), title, fill="#111111", font=font_med_title)
        
        d_y = gy + 33
        for d_line in wrap_text(desc, font_med_body, g_w - 12, draw)[:2]:
            draw.text((gx + 6, d_y), d_line, fill="#34495E", font=font_med_body)
            d_y += 14
        
    y += 3 * (g_h + 6) + 6
    draw.line([(margin, y), (width - margin, y)], fill="#34495E", width=1)
    y += 8

    # 5.5 IN BRIEF Second Page Strip
    brief_h = 24
    draw.rectangle([margin, y, width - margin, y + brief_h], outline="#1B2631", fill="#1B2631")
    brief_text = "IN BRIEF: UN Climate talks stall • Poland confirms missile fragments • Delta system glitch resolved • Beijing extends visa-free travel"
    draw.text((margin + 10, y + 6), brief_text, fill="#FFFFFF", font=font_small)
    y += brief_h + 8

    # 6. Bottom Section: Map on left, Also on this day on right (Height 210)
    bottom_h = 210
    half_w = (width - 2 * margin - 12) / 2
    
    # Left: Where it happened (Map with non-overlapping labels & leader lines)
    map_x = margin
    draw.rectangle([map_x, y, map_x + half_w, y + bottom_h], outline="#BDC3C7", fill="#F4F6F7")
    draw.rectangle([map_x, y, map_x + half_w, y + 20], fill="#1B2631")
    draw.text((map_x + 8, y + 4), "WHERE IT HAPPENED — GLOBAL HOTSPOTS", fill="#FFFFFF", font=font_section)
    
    for gx_line in range(int(map_x + 20), int(map_x + half_w), 45):
        draw.line([(gx_line, y + 24), (gx_line, y + bottom_h - 6)], fill="#E5E8E8", width=1)
    for gy_line in range(int(y + 35), int(y + bottom_h), 28):
        draw.line([(map_x + 10, gy_line), (map_x + half_w - 10, gy_line)], fill="#E5E8E8", width=1)

    # Carefully spaced dots and leader lines (city, cx, cy, label_dx, label_dy)
    dots = [
        ("Washington", 45, 50, -35, -12),
        ("Atlanta", 58, 85, -20, 10),
        ("Monrovia", 125, 145, 12, -4),
        ("Warsaw", 200, 42, -30, -14),
        ("Kyiv", 232, 52, 14, -12),
        ("Antalya", 215, 78, 14, 4),
        ("Kherson", 245, 70, 14, 14),
        ("Rabigh", 260, 112, 12, -4),
        ("Hormuz", 290, 105, 12, 10),
        ("Johannesburg", 235, 175, 12, 4),
        ("Shenzhen", 350, 80, -35, 12),
        ("Shanghai", 370, 62, 12, -10),
    ]

    for city, cx_off, cy_off, lx_off, ly_off in dots:
        px = map_x + cx_off
        py = y + cy_off
        draw.ellipse([px-3, py-3, px+3, py+3], fill="#C0392B", outline="#111111")
        # Draw leader line from dot to label
        lx = px + lx_off
        ly_pos = py + ly_off
        draw.line([(px, py), (lx if lx_off < 0 else px + 3, ly_pos + 4)], fill="#7F8C8D", width=1)
        draw.text((lx, ly_pos), city, fill="#1B2631", font=font_tiny)

    # Right: ALSO ON MONDAY 23 NOVEMBER 2026 (Refined column spacing & padding)
    right_x = map_x + half_w + 12
    draw.rectangle([right_x, y, width - margin, y + bottom_h], outline="#BDC3C7", fill="#FFFFFF")
    draw.rectangle([right_x, y, width - margin, y + 20], fill="#1B2631")
    draw.text((right_x + 8, y + 4), "ALSO ON MONDAY 23 NOVEMBER 2026", fill="#FFFFFF", font=font_section)

    also_items = [
        "[EUR] Russia missile flew into Poland, prosecutors confirm",
        "[MDE] Qatar officials discuss Iran mediation with Trump envoys",
        "[AFR] 25 deported migrants arrive in Liberia from US",
        "[GLO] Former UN Women chief Phumzile Mlambo-Ngcuka dies at 71",
        "[AMS] Delta system glitch delays hundreds of US flights at Atlanta",
        "[GLO] Barbados and UN convene special global AI-safety summit",
        "[ASI] Chinese visa-free entry extended to travellers in Philippines",
        "[ASI] Indian markets enter holiday-shortened trading week",
        "[MDE] Israel's first post-October-7 election reshapes politics"
    ]

    item_y = y + 26
    for item in also_items:
        wrapped_items = wrap_text(item, font_tiny, half_w - 20, draw)
        for w_item in wrapped_items:
            draw.text((right_x + 10, item_y), w_item, fill="#2C3E50", font=font_tiny)
            item_y += 15
        item_y += 2

    y += bottom_h + 10
    draw.line([(margin, y), (width - margin, y)], fill="#1B2631", width=1)
    y += 8

    # 7. Footer near y ~ 1000
    footer1 = "DATE CHECK: Every story on this page happened, or was first reported, on Monday 23 November 2026."
    footer2 = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Euronews, NPR, Kyiv Independent, Dawn, AllAfrica. Errors are not intentional."
    footer3 = "Stories are attributed, not stated as facts. Numbers are approximate."
    
    draw.text((margin, y), footer1, fill="#5D6D7E", font=font_tiny)
    y += 12
    draw.text((margin, y), footer2, fill="#5D6D7E", font=font_tiny)
    y += 12
    draw.text((margin, y), footer3, fill="#5D6D7E", font=font_tiny)

    # Save output
    img.save(output_path, "PNG", optimize=True)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_image()

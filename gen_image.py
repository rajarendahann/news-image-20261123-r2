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

def generate_image(output_path="entry.png"):
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), color="#FDFBF7")
    draw = ImageDraw.Draw(img)

    # Fonts (DejaVu)
    sans_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    sans_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    serif_bold_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    serif_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

    font_masthead = ImageFont.truetype(serif_bold_path, 52)
    font_subhead = ImageFont.truetype(sans_bold_path, 12)
    font_section = ImageFont.truetype(sans_bold_path, 12)
    font_big_title = ImageFont.truetype(sans_bold_path, 20)
    font_big_body = ImageFont.truetype(sans_path, 14)
    font_med_title = ImageFont.truetype(sans_bold_path, 14)
    font_med_body = ImageFont.truetype(sans_path, 12)
    font_small = ImageFont.truetype(sans_path, 12)
    font_tiny = ImageFont.truetype(sans_path, 11)

    margin = 20
    y = 16

    # 1. Top bar
    draw.text((margin, y), "THE WORLD IN ONE DAY  •  MONDAY, 23 NOVEMBER 2026  •  EDITION NO. 327", fill="#444444", font=font_subhead)
    y += 20
    draw.line([(margin, y), (width - margin, y)], fill="#222222", width=2)
    y += 10

    # 2. Huge Masthead Title
    title_text = "THE DAILY CHRONICLE"
    draw.text((margin, y), title_text, fill="#111111", font=font_masthead)
    y += 62

    # Lede line
    lede = "TRILATERAL SUMMIT IN SHENZHEN  •  MASSIVE MISSILE STRIKE ON UKRAINE  •  COP31 CLIMATE TALKS COLLAPSE IN ANTALYA"
    draw.text((margin, y), lede, fill="#555555", font=font_small)
    y += 18
    draw.line([(margin, y), (width - margin, y)], fill="#888888", width=1)
    y += 8

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
        draw.rectangle([bx, y, bx + box_w, y + 26], outline="#CCCCCC", fill="#F4F1EA")
        text_str = f"{reg}: {count}"
        tw = draw.textlength(text_str, font=font_small)
        draw.text((bx + (box_w - tw) / 2, y + 6), text_str, fill="#333333", font=font_small)
        bx += box_w + 8
    y += 34

    # 4. Three Big Story Cards (height 180)
    big_stories = [
        ("GLOBAL", "Peace Declaration in Shenzhen", "Trump, Xi and Putin release an unprecedented trilateral peace pact.", "Leaders meet at special summit to stabilize major power relations and chart new security architecture."),
        ("EUROPE", "Massive Airstrike on Kyiv", "Russia launches over 110 missiles and 400 drones targeting energy grid.", "Eighty infrastructure sites hit; at least 8 civilians reported killed across multiple regions of Ukraine."),
        ("GLOBAL", "COP31 Climate Talks Collapse", "Antalya summit ends with no pact as fossil fuel divisions sink draft.", "Delegates fail to bridge major gaps over phase-out timelines and international climate financing.")
    ]
    
    card_w = (width - 2 * margin - 2 * 12) / 3
    card_h = 180
    cx = margin
    for tag, headline, line1, line2 in big_stories:
        draw.rectangle([cx, y, cx + card_w, y + card_h], outline="#B0A899", fill="#FFFFFF", width=1)
        draw.rectangle([cx, y, cx + card_w, y + 22], fill="#2C3E50")
        draw.text((cx + 8, y + 4), tag, fill="#FFFFFF", font=font_section)
        
        hy = y + 28
        for h_line in wrap_text(headline, font_big_title, card_w - 16, draw):
            draw.text((cx + 8, hy), h_line, fill="#111111", font=font_big_title)
            hy += 22
        
        hy += 6
        body_text = f"{line1} {line2}"
        for b_line in wrap_text(body_text, font_big_body, card_w - 16, draw):
            draw.text((cx + 8, hy), b_line, fill="#333333", font=font_big_body)
            hy += 18
            
        cx += card_w + 12
    y += card_h + 12

    # 5. 3x3 Grid of Medium Cards (height 76)
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
    g_h = 76
    
    gx_start = margin
    gy_start = y
    
    for i, (tag, title, desc) in enumerate(med_stories):
        r = i // grid_cols
        c = i % grid_cols
        gx = gx_start + c * (g_w + 12)
        gy = gy_start + r * (g_h + 8)
        
        draw.rectangle([gx, gy, gx + g_w, gy + g_h], outline="#D0C8B8", fill="#FFFFFF")
        draw.rectangle([gx, gy, gx + g_w, gy + 16], fill="#555555")
        draw.text((gx + 6, gy + 2), tag, fill="#FFFFFF", font=font_tiny)
        
        draw.text((gx + 6, gy + 19), title, fill="#111111", font=font_med_title)
        
        d_y = gy + 36
        for d_line in wrap_text(desc, font_med_body, g_w - 12, draw)[:2]:
            draw.text((gx + 6, d_y), d_line, fill="#444444", font=font_med_body)
            d_y += 15
        
    y += 3 * (g_h + 8) + 8
    draw.line([(margin, y), (width - margin, y)], fill="#888888", width=1)
    y += 10

    # 6. Bottom Section: Map on left, Also on this day on right (Height stretched to 242)
    bottom_h = 242
    half_w = (width - 2 * margin - 12) / 2
    
    # Left: Where it happened
    map_x = margin
    draw.rectangle([map_x, y, map_x + half_w, y + bottom_h], outline="#CCCCCC", fill="#F4F1EA")
    draw.rectangle([map_x, y, map_x + half_w, y + 22], fill="#333333")
    draw.text((map_x + 8, y + 4), "WHERE IT HAPPENED", fill="#FFFFFF", font=font_section)
    
    for gx_line in range(int(map_x + 20), int(map_x + half_w), 40):
        draw.line([(gx_line, y + 26), (gx_line, y + bottom_h - 6)], fill="#E0DCD4", width=1)
    for gy_line in range(int(y + 35), int(y + bottom_h), 32):
        draw.line([(map_x + 10, gy_line), (map_x + half_w - 10, gy_line)], fill="#E0DCD4", width=1)

    # Kherson and Shenzhen moved further apart
    dots = [
        ("Washington", 50, 65, -10, -15),
        ("Atlanta", 65, 105, 8, 2),
        ("Monrovia", 130, 170, 10, -4),
        ("Warsaw", 205, 52, 8, -12),
        ("Kyiv", 235, 65, 10, 4),
        ("Antalya", 215, 90, -35, 8),
        ("Kherson", 240, 75, -38, -2),
        ("Rabigh", 260, 135, 8, 2),
        ("Hormuz", 295, 125, 8, -10),
        ("Johannesburg", 240, 200, 10, -4),
        ("Shenzhen", 355, 95, 10, 4),
        ("Shanghai", 375, 72, 10, -12),
    ]

    for city, cx_off, cy_off, lx_off, ly_off in dots:
        px = map_x + cx_off
        py = y + cy_off
        draw.ellipse([px-4, py-4, px+4, py+4], fill="#C0392B", outline="#000000")
        draw.text((px + lx_off, py + ly_off), city, fill="#222222", font=font_tiny)

    # Right: ALSO ON MONDAY 23 NOVEMBER 2026
    right_x = map_x + half_w + 12
    draw.rectangle([right_x, y, width - margin, y + bottom_h], outline="#CCCCCC", fill="#FFFFFF")
    draw.rectangle([right_x, y, width - margin, y + 22], fill="#333333")
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
        "[MDE] Israel's first post-October-7 election reshapes regional politics"
    ]

    item_y = y + 28
    for item in also_items:
        wrapped_items = wrap_text(item, font_tiny, half_w - 16, draw)
        for w_item in wrapped_items:
            draw.text((right_x + 8, item_y), w_item, fill="#333333", font=font_tiny)
            item_y += 16
        item_y += 3

    y += bottom_h + 12
    draw.line([(margin, y), (width - margin, y)], fill="#222222", width=1)
    y += 8

    # 7. Footer near y ~ 1000
    footer1 = "DATE CHECK: Every story on this page happened, or was first reported, on Monday 23 November 2026."
    footer2 = "Sources: Reuters, AP, AFP, BBC, Al Jazeera, Euronews, NPR, Kyiv Independent, Dawn, AllAfrica. Errors are not intentional."
    footer3 = "Stories are attributed, not stated as facts. Numbers are approximate."
    
    draw.text((margin, y), footer1, fill="#555555", font=font_tiny)
    y += 13
    draw.text((margin, y), footer2, fill="#555555", font=font_tiny)
    y += 13
    draw.text((margin, y), footer3, fill="#555555", font=font_tiny)

    # Save output
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    generate_image()

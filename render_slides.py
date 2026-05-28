#!/usr/bin/env python3
"""
Qalqan AI Roadmap — PNG slide renderer v2
Fixes: emoji→unicode, full-height layout, proper alignment
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = "/Users/eldoskydyrbek/qalqan-ai/slide_exports"
os.makedirs(OUT, exist_ok=True)

W, H = 1920, 1080

# ── Color palette ────────────────────────────────────────────────────────────
BG       = (2,   6,  23)
CARD     = (13,  22,  42)
CARD2    = (18,  30,  55)
BLUE     = (59,  130, 246)
RED      = (239,  68,  68)
AMBER    = (245, 158,  11)
GREEN    = (16,  185, 129)
PURPLE   = (139,  92, 246)
CYAN     = (34,  211, 238)
WHITE    = (255, 255, 255)
GRAY     = (148, 163, 184)
LGRAY    = (203, 213, 225)
DARKBLUE = (15,  23,  42)
HBORDER  = (30,  41,  59)
NAVY     = (30,  58, 138)

# ── Fonts ────────────────────────────────────────────────────────────────────
_FONT_PATH  = "/System/Library/Fonts/HelveticaNeue.ttc"
_FONT_BOLD  = "/System/Library/Fonts/HelveticaNeue.ttc"

def F(size, bold=False):
    idx = 1 if bold else 0
    try:
        return ImageFont.truetype(_FONT_PATH, size, index=idx)
    except:
        return ImageFont.load_default()

def FM(size):  # monospace
    try:
        return ImageFont.truetype("/System/Library/Fonts/Courier.ttc", size)
    except:
        return ImageFont.load_default()

# ── Drawing helpers ──────────────────────────────────────────────────────────
def new_slide():
    img = Image.new("RGB", (W, H), BG)
    d   = ImageDraw.Draw(img)
    return img, d

def rect(d, x, y, w, h, fill=None, outline=None, width=1):
    d.rectangle([(x, y), (x+w, y+h)], fill=fill, outline=outline, width=width)

def line_h(d, x, y, length, color, thickness=3):
    rect(d, x, y, length, thickness, fill=color)

def txt(d, x, y, text, fnt, color, anchor="la"):
    d.text((x, y), text, font=fnt, fill=color, anchor=anchor)

def txt_c(d, cx, y, text, fnt, color):
    d.text((cx, y), text, font=fnt, fill=color, anchor="mm")

def measure(text, fnt):
    bbox = ImageDraw.Draw(Image.new("RGB", (1,1))).textbbox((0,0), text, font=fnt)
    return bbox[2]-bbox[0], bbox[3]-bbox[1]

# ── Common chrome ─────────────────────────────────────────────────────────────
HDR_H  = 50
FTR_H  = 38
CONTENT_Y = HDR_H + 8          # content starts here
CONTENT_H = H - HDR_H - FTR_H - 16   # usable height

def header(d, label="QALQAN AI"):
    rect(d, 0, 0, W, HDR_H, fill=DARKBLUE)
    line_h(d, 0, HDR_H-2, W, BLUE, 2)
    # Left shield mark
    rect(d, 0, 0, 4, HDR_H, fill=BLUE)
    txt(d, 20, HDR_H//2, "[ Q ]", F(14, True), BLUE, anchor="lm")
    txt(d, 78, HDR_H//2, label, F(15, True), WHITE, anchor="lm")
    txt(d, W-20, HDR_H//2, "qalqan.kz  |  v5.1", F(13), GRAY, anchor="rm")

def footer(d):
    rect(d, 0, H-FTR_H, W, FTR_H, fill=DARKBLUE)
    line_h(d, 0, H-FTR_H, W, BLUE, 2)
    txt_c(d, W//2, H-FTR_H//2, "Qauipsis Qazaqstan  ·  Secure Kazakhstan  ·  Bezopasny Kazakhstan", F(12), GRAY)

def slide_title_bar(d, month_tag, month_color, title, subtitle, y=CONTENT_Y+4):
    # Month tag pill
    tw, _ = measure(month_tag, F(14, True))
    pad = 14
    pill_w = tw + pad*2
    rect(d, 40, y, pill_w, 38, fill=month_color)
    txt(d, 40+pad, y+19, month_tag, F(14, True), BG, anchor="lm")
    # Title
    txt(d, 40+pill_w+16, y, title, F(34, True), WHITE, anchor="lt")
    # Subtitle
    txt(d, 40+pill_w+16, y+40, subtitle, F(16), GRAY, anchor="lt")
    line_h(d, 40, y+68, 560, month_color, 3)
    return y + 80  # returns next y

def section_card(d, x, y, w, h, color, title_text):
    """Draw a section card with colored header bar."""
    rect(d, x, y, w, h, fill=CARD, outline=color, width=1)
    rect(d, x, y, w, 36, fill=(*[c//4 for c in color], 255) if False else
         tuple(min(255, c//3) for c in color))
    line_h(d, x, y, w, color, 2)
    txt(d, x+12, y+18, title_text, F(15, True), color, anchor="lm")
    return y + 44  # content start y

def bullet(d, x, y, text, color=BLUE, fsize=14):
    """Draw a bullet point line. Returns next y."""
    rect(d, x, y+7, 7, 7, fill=color)
    txt(d, x+16, y, text, F(fsize), LGRAY, anchor="lt")
    _, h = measure(text, F(fsize))
    return y + max(h, 9) + 10

def check_item(d, x, y, text, color=GREEN, fsize=14):
    """Green filled square + text."""
    sq = fsize - 4
    rect(d, x, y + 3, sq, sq, fill=color)
    txt(d, x + sq + 8, y, text, F(fsize), LGRAY, anchor="lt")
    _, h = measure(text, F(fsize))
    return y + max(h + 6, sq + 6) + 6

def cross_item(d, x, y, text, color=AMBER, fsize=14):
    """Amber outlined square + text."""
    sq = fsize - 4
    rect(d, x, y + 3, sq, sq, outline=color, width=2)
    txt(d, x + sq + 8, y, text, F(fsize), GRAY, anchor="lt")
    _, h = measure(text, F(fsize))
    return y + max(h + 6, sq + 6) + 6

def check_item2(d, x, y, title, detail, color=GREEN, fsize=15):
    """Two-line check item: bold title + gray detail. Returns next y."""
    sq = fsize - 2
    rect(d, x, y + 4, sq, sq, fill=color)
    txt(d, x + sq + 10, y,      title,  F(fsize, True), WHITE,  anchor="lt")
    txt(d, x + sq + 10, y + fsize + 4, detail, F(fsize - 2),   GRAY,   anchor="lt")
    return y + fsize*2 + 14

def cross_item2(d, x, y, title, detail, color=AMBER, fsize=15):
    """Two-line cross item. Returns next y."""
    sq = fsize - 2
    rect(d, x, y + 4, sq, sq, outline=color, width=2)
    txt(d, x + sq + 10, y,      title,  F(fsize, True), LGRAY,  anchor="lt")
    txt(d, x + sq + 10, y + fsize + 4, detail, F(fsize - 2),   GRAY,   anchor="lt")
    return y + fsize*2 + 14

def wow_banner(d, x, y, w, text, color):
    rect(d, x, y, w, 42, fill=tuple(c//4 for c in color), outline=color, width=1)
    txt_c(d, x+w//2, y+21, text, F(14, True), color)

def stat_block(d, cx, y, number, label, color=BLUE):
    txt_c(d, cx, y,    number, F(42, True), color)
    txt_c(d, cx, y+50, label,  F(13),       GRAY)

def spaced_rows(d, x, y_start, y_end, items, color, card_w=860):
    """Distribute (title, desc) items evenly from y_start to y_end. No empty gaps."""
    n = len(items)
    if n == 0: return
    row_h = (y_end - y_start) // n
    sq = 11
    for i, item in enumerate(items):
        title = item[0] if isinstance(item, tuple) else item
        desc  = item[1] if isinstance(item, tuple) and len(item) > 1 else ""
        ry = y_start + i * row_h
        mid = ry + row_h // 2
        # Colored left bar
        rect(d, x, ry + 2, 3, row_h - 4, fill=color)
        # Bullet square
        rect(d, x + 10, mid - sq//2, sq, sq, fill=color)
        # Text — vertically centered in row
        if desc:
            txt(d, x + 28, mid - 14, title, F(14, True), WHITE,  anchor="lt")
            txt(d, x + 28, mid +  4, desc,  F(12),        GRAY,   anchor="lt")
        else:
            txt(d, x + 28, mid - 10, title, F(14, True), WHITE, anchor="lt")
        # Row separator (except last)
        if i < n - 1:
            line_h(d, x + 3, ry + row_h - 1, card_w - 6, HBORDER, 1)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE
# ═══════════════════════════════════════════════════════════════════════════════
def slide1():
    img, d = new_slide()

    # Full-slide background gradient simulation with band
    rect(d, 0, 0, W, H, fill=BG)
    rect(d, 0, 0, W, 220, fill=(4, 10, 32))
    line_h(d, 0, 218, W, BLUE, 2)

    # Shield circle decoration
    cx, cy = W//2, 110
    d.ellipse([(cx-78, cy-78), (cx+78, cy+78)], outline=BLUE, width=2)
    d.ellipse([(cx-60, cy-60), (cx+60, cy+60)], outline=tuple(c//2 for c in BLUE), width=1)
    # Pentagon shield polygon
    shield_pts = [
        (cx,    cy-52),   # top center
        (cx+42, cy-32),   # top right
        (cx+42, cy+10),   # mid right
        (cx,    cy+52),   # bottom point
        (cx-42, cy+10),   # mid left
        (cx-42, cy-32),   # top left
    ]
    d.polygon(shield_pts, outline=BLUE, fill=tuple(c//5 for c in BLUE))
    # Q letter inside shield
    txt_c(d, cx, cy+4, "Q", F(36, True), BLUE)

    # Main title
    title = "QALQAN AI"
    txt_c(d, W//2, 310, title, F(108, True), WHITE)
    # Underline
    tw, _ = measure(title, F(108, True))
    ux = W//2 - tw//2
    line_h(d, ux, 372, tw, BLUE, 4)

    # Tagline
    txt_c(d, W//2, 420, "90-KUNDIK ZHOLZHASPAR  |  MAUSYM – TAMYZ 2026", F(26, True), BLUE)
    txt_c(d, W//2, 462, "Ulttyk kiberkorganysh platformasyna aparatyn zhol", F(18), GRAY)

    # ── 4 threat-type tags ───────────────────────────────────────────────────
    tags = [("PHISHING", RED), ("PYRAMID", AMBER), ("GAMBLING", PURPLE), ("GOSZAKUPKI", GREEN)]
    tag_w, tag_h = 190, 44
    gap = 20
    total = len(tags)*(tag_w+gap) - gap
    sx = (W - total)//2
    for i, (name, color) in enumerate(tags):
        tx = sx + i*(tag_w+gap)
        ty = 520
        rect(d, tx, ty, tag_w, tag_h, outline=color, width=2)
        # Subtle fill
        rect(d, tx+1, ty+1, tag_w-2, tag_h-2, fill=tuple(c//6 for c in color))
        txt_c(d, tx+tag_w//2, ty+tag_h//2, name, F(14, True), color)

    # ── 4 KPI stat boxes ─────────────────────────────────────────────────────
    stats = [("6", "Detection Layers", BLUE),
             ("30+", "ML Features",    CYAN),
             ("3",   "AI Models",      PURPLE),
             (">95%","Precision KZ",   GREEN)]
    box_w = 380
    bx_start = (W - 4*box_w - 3*20)//2
    for i, (num, lbl, color) in enumerate(stats):
        bx = bx_start + i*(box_w+20)
        by = 610
        rect(d, bx, by, box_w, 100, fill=CARD, outline=color, width=1)
        line_h(d, bx, by, box_w, color, 3)
        txt_c(d, bx+box_w//2, by+40, num, F(36, True), color)
        txt_c(d, bx+box_w//2, by+78, lbl, F(14),       GRAY)

    # ── Bottom two-line motto ─────────────────────────────────────────────────
    rect(d, 0, 750, W, 290, fill=(3, 8, 28))
    line_h(d, 0, 750, W, HBORDER, 1)

    txt_c(d, W//2, 800,
          "Kazakhstan's First AI-Powered Cybersecurity Platform",
          F(22, True), WHITE)
    txt_c(d, W//2, 840,
          "Phishing  |  Financial Pyramids  |  Gambling  |  Gov Procurement Fraud",
          F(16), GRAY)

    # Accent rectangles decorative
    rect(d, 40, 870, 280, 60, fill=CARD, outline=RED, width=1)
    txt_c(d, 180, 900, "Jeke adal", F(13), RED)
    txt_c(d, 180, 918, "Zero-trust, no bypass", F(12), GRAY)

    rect(d, 340, 870, 320, 60, fill=CARD, outline=GREEN, width=1)
    txt_c(d, 500, 900, "KazCERT Ready", F(13), GREEN)
    txt_c(d, 500, 918, "gov.kz integration", F(12), GRAY)

    rect(d, 680, 870, 300, 60, fill=CARD, outline=BLUE, width=1)
    txt_c(d, 830, 900, "Open Source", F(13), BLUE)
    txt_c(d, 830, 918, "Vercel + FastAPI", F(12), GRAY)

    rect(d, 1600, 870, 280, 60, fill=CARD, outline=AMBER, width=1)
    txt_c(d, 1740, 900, "Republican 2026", F(13), AMBER)
    txt_c(d, 1740, 918, "Competition Entry", F(12), GRAY)

    footer(d)
    img.save(f"{OUT}/slide_01_title.png")
    print("Slide 1 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — CURRENT STATUS
# ═══════════════════════════════════════════════════════════════════════════════
def slide2():
    img, d = new_slide()
    header(d)

    # Page title
    txt(d, 40, 62, "CURRENT STATUS — v5.1", F(36, True), WHITE, anchor="lt")
    txt(d, 40, 108, "What we have built  vs  What remains to win the competition", F(17), GRAY, anchor="lt")
    line_h(d, 40, 132, 600, BLUE, 3)

    CY   = 148
    # Two-line items — calculate height: 10 done × 46px + header 40 + pad 16 = 512
    # 8 gaps × 46px + header 40 + pad 16 = 424  → use 512 for both
    ROW  = 46   # px per two-line item
    LW   = 920  # left card width
    RW   = W - 80 - LW - 20  # right card width

    done_items = [
        ("6-tier detection pipeline",            "whitelist > cache > pyramid > DBs > domain intel > AI + XAI"),
        ("Chrome Extension MV3",                 "real-time KZ phishing / gambling / pyramid blocking"),
        ("Groq LLaMA 70B + Gemini Vision AI",    "dual AI with auto-fallback, vision screenshot analysis"),
        ("30+ ML URL features",                  "lexical, structural, entropy, brand-match features + XAI"),
        ("Offline DB — Service Worker",           "works without internet, instant block on page load"),
        ("Domain Intel — RDAP + SSL",            "domain age + certificate validity check"),
        ("KZ Brand Protection",                  "Kaspi / eGov / Halyk / TeleBank impersonation detection"),
        ("Telegram Bot integration",             "appeal + fraud report notifications to admin"),
        ("Phase 1 auto-block",                   "blocks on 'loading' event, before DOM fully loads"),
        ("Stats + history + cache",              "full analytics pipeline, persistent across sessions"),
    ]
    gap_items = [
        ("Goszakupki fraud detection",           "government tender fraud — 10 red-flag rules"),
        ("Mobile PWA + QR scanner",              "Android/iOS no-install, Kaspi QR phishing check"),
        ("Custom KZ ML model",                   "XLM-RoBERTa fine-tune on 50K KZ URL dataset"),
        ("Public REST API v1",                   "GET /check?url= for egov / banks / third-party apps"),
        ("KazGPT integration",                   "KZ data sovereignty — no US/RU cloud processing"),
        ("KazCERT official partnership",         "state-level endorsement and gov.kz monitoring"),
        ("KZ Threat Report 2026",                "published research paper + PDF + live dashboard"),
        ("Benchmark vs VirusTotal",              "prove Qalqan beats global tools on KZ-specific data"),
        ("Competition demo package",             "live demo + pitch deck + research summary"),
        ("Performance & stress testing",         "load test, accuracy validation, final QA pass"),
    ]

    # Equal row count — both 10 items, same card height
    LH = len(done_items) * ROW + 40 + 20
    CH  = LH  # both cards same height

    # ── LEFT card: Done ───────────────────────────────────────────────────────
    section_card(d, 40, CY, LW, CH, GREEN, f"  DONE — Production Ready   ({len(done_items)} items)")
    cy = CY + 44
    for title, detail in done_items:
        cy = check_item2(d, 52, cy, title, detail, GREEN, 15)

    # ── RIGHT card: Gaps ──────────────────────────────────────────────────────
    section_card(d, 40+LW+20, CY, RW, CH, AMBER,
                 f"  TO BUILD — June/July/August 2026   ({len(gap_items)} items)")
    ry = CY + 44
    for title, detail in gap_items:
        ry = cross_item2(d, 40+LW+32, ry, title, detail, AMBER, 15)

    # ── Stats bar — fixed height 120px, flush below cards ─────────────────────
    bar_y = CY + CH + 10
    bar_h = 120
    rect(d, 40, bar_y, W-80, bar_h, fill=(8, 16, 36), outline=BLUE, width=1)
    line_h(d, 40, bar_y, W-80, BLUE, 3)

    stats = [("6",     "Detection Layers",  BLUE,   200),
             ("30+",   "ML Features",       CYAN,   580),
             ("3",     "AI Models",         PURPLE, 960),
             ("100K+", "Threats Blocked",   GREEN,  1340),
             ("0 tg",  "Monthly Cost",      AMBER,  1720)]
    mid = bar_y + 18
    for num, lbl, color, cx in stats:
        stat_block(d, cx, mid, num, lbl, color)

    # ── Remaining space: two callout boxes ─────────────────────────────────────
    call_y = bar_y + bar_h + 10
    call_h = H - FTR_H - call_y - 6
    if call_h > 40:
        cw = (W - 80 - 20) // 2
        rect(d, 40, call_y, cw, call_h, fill=(5,20,10), outline=GREEN, width=1)
        txt(d, 40+cw//2, call_y + call_h//2 - 12,
            "Production status: LIVE on Vercel", F(14, True), GREEN, anchor="mm")
        txt(d, 40+cw//2, call_y + call_h//2 + 10,
            "qalqan-ai.vercel.app", F(13), GRAY, anchor="mm")
        rect(d, 40+cw+20, call_y, cw, call_h, fill=(25,18,0), outline=AMBER, width=1)
        txt(d, 40+cw+20+cw//2, call_y + call_h//2 - 12,
            "Competition: Republican IT Contest 2026", F(14, True), AMBER, anchor="mm")
        txt(d, 40+cw+20+cw//2, call_y + call_h//2 + 10,
            "Deadline: August 2026  —  90 days remaining", F(13), GRAY, anchor="mm")

    footer(d)
    img.save(f"{OUT}/slide_02_status.png")
    print("Slide 2 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — JUNE
# ═══════════════════════════════════════════════════════════════════════════════
def slide3():
    img, d = new_slide()
    header(d)

    ny = slide_title_bar(d, "JUNE", RED,
                         "Economic Intelligence",
                         "Goszakupki fraud + Telegram Bot — exclusive to us worldwide")

    CW = (W - 80 - 20) // 2
    CH = H - ny - FTR_H - 14
    wow_y = ny + CH - 50   # wow_banner starts here

    # ── LEFT: Goszakupki ─────────────────────────────────────────────────────
    cy = section_card(d, 40, ny, CW, CH, GREEN,
                      "  GOSZAKUPKI FRAUD DETECTION  [ worlds first ]")

    txt(d, 52, cy + 2, "10 RED-FLAG RULES:", F(13, True), AMBER, anchor="lt")
    cy += 26

    rules = [
        ("Company wins >70% tenders in region",    "Regional monopoly — collusion signal"),
        ("Supplier registered <30 days",            "Newly formed entity — shell risk"),
        ("Price >40% above market estimate",        "Inflated pricing — overvalued bid"),
        ("Only 1-2 participants in tender",         "No competition — rigged process"),
        ("Same-day announcement + deadline",        "No time to compete fairly"),
        ("Spec written for one supplier",           "Artificially restricted bidding"),
        ("Shell company: 0-1 employees",            "Company-of-the-day pattern"),
        ("Single-source procurement",               "No bidding process at all"),
    ]

    info_h = 52
    spaced_rows(d, 52, cy, wow_y - info_h - 8, rules, GREEN, card_w=CW - 20)

    iy = wow_y - info_h + 4
    txt(d, 52, iy,    "->  Data: goszakup.gov.kz Open API — free, no auth", F(13), CYAN, anchor="lt")
    txt(d, 52, iy+24, "->  Almaty region pilot — real fraud case examples", F(13), CYAN, anchor="lt")

    wow_banner(d, 40, wow_y, CW,
               "[ WOW ]  World's first KZ government procurement AI fraud detector",
               GREEN)

    # ── RIGHT: Telegram Bot ───────────────────────────────────────────────────
    rx = 40 + CW + 20
    ry = section_card(d, rx, ny, CW, CH, BLUE,
                      "  TELEGRAM BOT  [ 0 install ]")

    commands = [
        ("/check <url>",       "Full 6-tier Qalqan pipeline in seconds"),
        ("/tender <number>",   "Goszakupki fraud scan — real tender data"),
        ("/report <url>",      "Submit fraud report, notify admin"),
        ("/stats",             "Today's protection stats and blocked count"),
        ("@bot <url>",         "Inline mode — works in any group chat"),
        ("(bare URL message)", "Auto-detected and scanned, no command needed"),
    ]

    info_h2 = 80
    spaced_rows(d, rx+12, ry, wow_y - info_h2 - 8, commands, BLUE, card_w=CW - 20)

    iy2 = wow_y - info_h2 + 4
    txt(d, rx+12, iy2,    "Platform: Vercel webhook + httpx — no extra deps",  F(13), GRAY,  anchor="lt")
    txt(d, rx+12, iy2+24, "Cost:     0 tg / month — serverless, always free",  F(13), GRAY,  anchor="lt")
    txt(d, rx+12, iy2+48, "Audience: 100K+ KZ Telegram users, zero install",   F(14, True), GREEN, anchor="lt")

    wow_banner(d, rx, wow_y, CW,
               "[ WOW ]  Zero install — open Telegram, type /check, done",
               BLUE)

    footer(d)
    img.save(f"{OUT}/slide_03_june.png")
    print("Slide 3 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — JULY
# ═══════════════════════════════════════════════════════════════════════════════
def slide4():
    img, d = new_slide()
    header(d)

    ny = slide_title_bar(d, "JULY", AMBER,
                         "Mobile + Custom ML Model",
                         "70% of KZ users are mobile + academic depth for jury credibility")

    CW = (W - 80 - 20) // 2
    CH = H - ny - FTR_H - 14
    wow_y = ny + CH - 50

    # ── LEFT: PWA + QR ────────────────────────────────────────────────────────
    cy = section_card(d, 40, ny, CW, CH, PURPLE, "  PWA + QR SCANNER  [ no install ]")

    feats = [
        ("Android & iOS — no app store required",    "Runs entirely in mobile browser"),
        ("Camera QR code scanner",                   "Scan -> Qalqan check in < 1 second"),
        ("Kaspi QR phishing detection",              "Most common KZ mobile scam vector"),
        ("Offline mode — Service Worker cache",      "Protection without internet access"),
        ("Push notifications",                       "Real-time new threat alerts"),
        ("Web Share Target API",                     "Share any URL from any app to Qalqan"),
    ]

    stat_h = 52
    spaced_rows(d, 52, cy, wow_y - stat_h - 8, feats, PURPLE, card_w=CW - 20)

    sy = wow_y - stat_h + 4
    txt(d, 52, sy,    "->  70% Kazakhstan users = mobile devices", F(14, True), AMBER, anchor="lt")
    txt(d, 52, sy+24, "->  Target reach: 10 million KZ users", F(13), GRAY, anchor="lt")

    wow_banner(d, 40, wow_y, CW,
               "[ WOW ]  QR scanner — #1 mobile cybersecurity tool in Central Asia",
               PURPLE)

    # ── RIGHT: ML Model ───────────────────────────────────────────────────────
    rx = 40 + CW + 20
    ry = section_card(d, rx, ny, CW, CH, CYAN, "  XLM-RoBERTa FINE-TUNE  [ own model ]")

    ml_items = [
        ("KZ / RU / EN trilingual detector",           "Native language phishing understanding"),
        ("Google Colab A100 — free GPU training",      "Zero hardware cost"),
        ("Dataset: 50K KZ URLs collected",             "Unique KZ-specific training data"),
        ("Target precision: >95% on KZ phishing",      "Beats all generic global models"),
        ("ONNX export -> Vercel Edge Functions",        "Fast inference, no Python runtime"),
        ("arxiv preprint publication",                 "Academic credibility for competition jury"),
    ]

    api_h = 92
    spaced_rows(d, rx+12, ry, wow_y - api_h - 8, ml_items, CYAN, card_w=CW - 20)

    ay = wow_y - api_h + 4
    rect(d, rx+12, ay, CW-24, api_h - 4, fill=CARD2, outline=BLUE, width=1)
    line_h(d, rx+12, ay, CW-24, BLUE, 2)
    txt(d, rx+24, ay+12, "PUBLIC API  v1", F(14, True), BLUE, anchor="lt")
    txt(d, rx+24, ay+34, "GET /api/check?url=...  ->  {verdict, score, reason_kk}", FM(12), LGRAY, anchor="lt")
    txt(d, rx+24, ay+56, "egov.kz / Halyk Bank / CON integration ready", F(12), GREEN, anchor="lt")

    wow_banner(d, rx, wow_y, CW,
               "[ WOW ]  Own model + academic paper = unique research depth",
               CYAN)

    footer(d)
    img.save(f"{OUT}/slide_04_july.png")
    print("Slide 4 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — AUGUST
# ═══════════════════════════════════════════════════════════════════════════════
def slide5():
    img, d = new_slide()
    header(d)

    ny = slide_title_bar(d, "AUGUST", GREEN,
                         "Scientific Proof + Sovereignty",
                         "Jury believes data + state partnership = unbeatable credibility")

    gap = 15
    CW = (W - 80 - gap*2) // 3
    CH = H - ny - FTR_H - 14

    cols = [
        (40,          CW, AMBER,  "  KZ THREAT REPORT 2026",
         [("'KZ Cyber Threat Landscape 2026'",    "Named PDF research publication"),
          ("Top-20 active phishing domains",       "Real KZ threat intelligence"),
          ("Threat type statistics",               "Gambling 45%, Phishing 30%"),
          ("Monthly trend graphs",                 "Visualised attack patterns"),
          ("PDF + live web dashboard",             "Always up-to-date"),
          ("Submitted to KazCERT",                 "Official threat sharing"),],
         "[ WOW ]  Data credibility — jury trusts numbers"),

        (40+CW+gap,   CW, RED,    "  BENCHMARK vs GLOBALS",
         [("vs VirusTotal (91 engines, global)",   "Our advantage: KZ specificity"),
          ("vs Kaspersky (RU-focused)",             "We detect KZ brands, they don't"),
          ("vs PhishTank (crowdsourced)",           "We have local KZ intel"),
          ("KZ-specific test dataset",              "50K real URLs, not synthetic"),
          ("Metrics: Precision / Recall / F1",      "Rigorous scientific comparison"),
          ("Result: Qalqan wins on KZ phishing",   "Clear competitive advantage"),],
         "[ WOW ]  We beat global tools on KZ-specific data"),

        (40+2*(CW+gap), CW, BLUE, "  KazGPT + KazCERT",
         [("KazGPT AI integration",                "KZ data stays in Kazakhstan"),
          ("Sovereign AI — no US/RU dependency",   "Data privacy guaranteed"),
          ("Kazakh + Russian native language",      "Better context understanding"),
          ("KazCERT official partnership",          "State-level endorsement"),
          ("gov.kz domains auto-monitoring",        "Protect all government sites"),
          ("KZ cybersecurity ecosystem",            "Competitive moat — no copy"),],
         "[ WOW ]  Gov endorsement = competition win"),
    ]

    wow_y = ny + CH - 50

    for cx, cw, color, title, items, wow in cols:
        cy = section_card(d, cx, ny, cw, CH, color, title)
        spaced_rows(d, cx+12, cy, wow_y - 8, items, color, card_w=cw - 20)
        wow_banner(d, cx, wow_y, cw, wow, color)

    footer(d)
    img.save(f"{OUT}/slide_05_august.png")
    print("Slide 5 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — GANTT
# ═══════════════════════════════════════════════════════════════════════════════
def slide6():
    img, d = new_slide()
    header(d)

    txt(d, 40, 62,  "90-DAY ROADMAP — All Features", F(36, True), WHITE, anchor="lt")
    txt(d, 40, 108, "June + July + August 2026  |  Sorted by impact", F(17), GRAY, anchor="lt")
    line_h(d, 40, 132, 600, BLUE, 3)

    rows = [
        ("Goszakupki fraud detection",     "JUN", RED,    "Worlds first KZ gov procurement fraud AI detector"),
        ("Telegram Bot /check /tender",    "JUN", RED,    "Zero install — 100K+ KZ Telegram users instantly"),
        ("PWA + QR Scanner",               "JUL", AMBER,  "Mobile-first — 70% KZ users = 10M people"),
        ("XLM-RoBERTa KZ fine-tune",       "JUL", AMBER,  "Own AI model + arxiv paper = academic credibility"),
        ("Public REST API v1",             "JUL", AMBER,  "egov / Halyk Bank / CON integration pathway"),
        ("KZ Threat Report PDF",           "AUG", GREEN,  "Data-driven credibility — jury trusts numbers"),
        ("Benchmark vs VirusTotal",        "AUG", GREEN,  "Proof: we beat global tools on KZ-specific data"),
        ("KazGPT Integration",             "AUG", GREEN,  "Data sovereignty — KZ data stays in Kazakhstan"),
        ("KazCERT Partnership",            "AUG", GREEN,  "State endorsement — impossible to copy"),
        ("Competition Demo Package",       "AUG", GREEN,  "Full live demo + pitch deck + research paper"),
    ]

    # Table header
    hy = 148
    rect(d, 40, hy, W-80, 36, fill=NAVY)
    line_h(d, 40, hy, W-80, BLUE, 2)
    headers = [("FEATURE / TASK", 56, 480), ("MONTH", 540, 80),
               ("COMPETITIVE EDGE", 640, 1240)]
    for label, hx, _ in headers:
        txt(d, hx, hy+18, label, F(12, True), CYAN, anchor="lm")
    line_h(d, 40, hy+36, W-80, HBORDER, 1)

    ROW_H = 78
    for i, (task, month, color, edge) in enumerate(rows):
        ry = hy + 36 + i*ROW_H
        bg = CARD if i%2==0 else (10, 18, 38)
        rect(d, 40, ry, W-80, ROW_H, fill=bg)
        # Left color strip
        rect(d, 40, ry, 4, ROW_H, fill=color)
        # Row number
        txt(d, 60, ry+ROW_H//2, f"{i+1:02d}", F(13), GRAY, anchor="lm")
        # Task name
        txt(d, 86, ry+ROW_H//2-10, task, F(15, True), WHITE, anchor="lm")
        # Month badge
        mc = RED if month=="JUN" else AMBER if month=="JUL" else GREEN
        bw = 68
        rect(d, 540, ry+18, bw, 28, fill=mc)
        txt_c(d, 540+bw//2, ry+32, month, F(13, True), BG)
        # Edge description
        txt(d, 640, ry+ROW_H//2-8, edge, F(13), LGRAY, anchor="lm")
        # Separator
        line_h(d, 40, ry+ROW_H-1, W-80, HBORDER, 1)

    footer(d)
    img.save(f"{OUT}/slide_06_gantt.png")
    print("Slide 6 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — WHY WE WIN
# ═══════════════════════════════════════════════════════════════════════════════
def slide7():
    img, d = new_slide()
    header(d)

    txt_c(d, W//2, 82, "WHY WE WIN", F(52, True), WHITE)
    line_h(d, W//2-260, 112, 520, BLUE, 4)
    txt_c(d, W//2, 132, "Three unbeatable arguments for the jury", F(18), GRAY)

    gap = 20
    CW = (W - 80 - gap*2) // 3
    CY = 152
    # Leave 52px at bottom for the global statement + margin
    CH = H - CY - FTR_H - 56
    wow_y = CY + CH - 50   # wow_banner top inside each card

    cards = [
        (BLUE,   "01  UNIQUENESS",
         [("Kaspi + eGov + Halyk impersonation",        "KZ-specific brand protection"),
          ("Financial pyramid detection",                "MLM / investment fraud KZ-style"),
          ("Gambling — banned in KZ",                   "1xBet, Mostbet, 60+ blocked"),
          ("Goszakupki fraud detection",                "Gov procurement, unique worldwide"),
          ("All in ONE tool, 6-tier pipeline",          "No competitor covers all these"),],
         [("VirusTotal",   "global — zero KZ focus"),
          ("Kaspersky",    "RU-focused — no KZ brands"),
          ("PhishTank",    "crowdsource — no KZ intel"),],
         "No comparable solution exists for Central Asia — FIRST MOVER"),

        (GREEN,  "02  SOCIAL IMPACT",
         [("180K+ Kazakhstanis defrauded in 2024",      "Real documented problem scale"),
          ("Average loss per victim: 150,000 tg",       "Significant financial harm"),
          ("Target: 100K blocked attacks by Aug",       "Measurable KPI for the jury"),
          ("Telegram bot: 100K+ users, zero install",   "Mass adoption instantly"),
          ("QR scanner: mobile-first protection",       "Reaches most vulnerable users"),],
         [("Pyramid schemes",  "~45% of online fraud in KZ"),
          ("Phishing",         "~30%, banking focused"),
          ("Gambling",         "~25%, youth targeted"),],
         "Protecting people who cannot protect themselves"),

        (AMBER,  "03  SOVEREIGNTY",
         [("KazGPT: KZ data stays in Kazakhstan",       "No foreign AI cloud processing"),
          ("Not dependent on US or RU services",        "True digital sovereignty"),
          ("KazCERT partnership pathway",               "Official state endorsement"),
          ("gov.kz domains auto-monitoring",            "Protects all government sites"),
          ("Kazakh + Russian native NLP",               "Better than generic global models"),],
         [("DigitalKZ 2025",   "state program alignment"),
          ("NCSC partnership", "national cyber strategy"),
          ("Data privacy",     "GDPR-equivalent KZ law"),],
         "State partnership = competitive moat nobody can copy"),
    ]

    for i, card_data in enumerate(cards):
        color, title, items, comps, tagline = card_data
        cx = 40 + i*(CW+gap)

        # Card background
        rect(d, cx, CY, CW, CH, fill=CARD, outline=color, width=1)

        # Header
        hdr_bg = tuple(min(c//3, 80) for c in color)
        rect(d, cx, CY, CW, 48, fill=hdr_bg)
        line_h(d, cx, CY, CW, color, 3)
        txt(d, cx+16, CY+24, title, F(18, True), color, anchor="lm")
        line_h(d, cx+12, CY+50, CW-24, HBORDER, 1)

        # Competitor section sits just above wow_banner
        # comp_h = label(22) + 3 entries × 22px = 22+66 = 88
        comp_h = 90
        comp_top = wow_y - comp_h - 6

        # Main items use spaced_rows — fills space from header to competitor section
        spaced_rows(d, cx+12, CY+58, comp_top - 6, items, color, card_w=CW-24)

        # Competitor comparison
        line_h(d, cx+12, comp_top, CW-24, HBORDER, 1)
        comp_top += 4
        rect(d, cx+12, comp_top, CW-24, 22, fill=(20,28,50))
        txt(d, cx+20, comp_top+11, "vs COMPETITORS:", F(12, True), GRAY, anchor="lm")
        comp_top += 24
        for cname, cdesc in comps:
            rect(d, cx+12, comp_top, 4, 18, fill=RED)
            txt(d, cx+22, comp_top+9, cname, F(12, True), LGRAY, anchor="lm")
            nw, _ = measure(cname, F(12, True))
            txt(d, cx+22+nw+8, comp_top+9, f"— {cdesc}", F(12), GRAY, anchor="lm")
            comp_top += 22

        # Tagline
        wow_banner(d, cx, wow_y, CW, tagline, color)

    # Global statement banner — safe below cards, above footer
    gs_y = CY + CH + 6
    gs_h = H - FTR_H - 4 - gs_y
    rect(d, 40, gs_y, W-80, gs_h, fill=(5,15,50), outline=BLUE, width=1)
    txt_c(d, W//2, gs_y + gs_h//2,
          "Qalqan AI — Kazakhstan's first local AI cyber-immunity system.  "
          "No comparable solution exists for Central Asia.",
          F(15, True), WHITE)

    footer(d)
    img.save(f"{OUT}/slide_07_whywin.png")
    print("Slide 7 done")

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — PRIORITY MVP
# ═══════════════════════════════════════════════════════════════════════════════
def slide8():
    img, d = new_slide()
    header(d)

    txt_c(d, W//2, 82,  "PRIORITIES — IF TIME IS LIMITED", F(44, True), WHITE)
    txt_c(d, W//2, 126, "Pick 3 features — these are the ones:", F(18), GRAY)
    line_h(d, W//2-280, 148, 560, AMBER, 3)

    gap = 20
    CW = (W - 80 - gap*2) // 3
    CY = 162
    # Reserve 52px at bottom for deadline banner
    CH = H - CY - FTR_H - 56
    # rating bar is last 46px of each card
    rating_h = 46
    rating_y = CY + CH - rating_h   # absolute y of rating bar

    mvps = [
        (BLUE,  "#1  TELEGRAM BOT",
         "Build time: 2 weeks",
         "Vercel webhook + httpx — zero library deps",
         [("Mass audience instantly",         "100K+ KZ Telegram users, zero install"),
          ("Easiest to build of all features", "2 weeks, minimal dependencies"),
          ("0 tg / month cost",               "Runs free on existing Vercel account"),
          ("/check /tender /report /stats",   "Full feature set from day one"),
          ("Inline mode @bot",                "Works in any group chat instantly"),],
         "IMPACT: HIGH  |  EFFORT: LOW  |  TIME: 2 weeks"),

        (GREEN, "#2  GOSZAKUPKI FRAUD",
         "Build time: 3 weeks",
         "goszakup.gov.kz Open API + 8 red-flag rules",
         [("World's first — no competitor has it",  "Unique worldwide, KZ exclusive"),
          ("Real economic damage addressed",         "Billions tg stolen via fraud tenders"),
          ("Open data — free API, no auth",          "Zero cost, zero barriers"),
          ("8 red-flag rules + scoring system",      "Single-source, monopoly, overpriced"),
          ("Jury WOW factor — they remember this",   "Nothing like it exists anywhere"),],
         "IMPACT: MAX  |  EFFORT: MED  |  TIME: 3 weeks"),

        (AMBER, "#3  KZ THREAT REPORT",
         "Build time: 2 weeks",
         "Auto-generated PDF + live web dashboard",
         [("Data-driven credibility",         "Jury trusts hard numbers over claims"),
          ("Academic tone and structure",     "Looks like a real research publication"),
          ("Real KZ threat statistics",       "Top-20 phishing domains, trend graphs"),
          ("Shareable with KazCERT",          "Opens official partnership pathway"),
          ("Auto-generated monthly",          "Always current, zero manual work"),],
         "IMPACT: HIGH  |  EFFORT: LOW  |  TIME: 2 weeks"),
    ]

    for i, (color, title, build_time, tech, items, rating) in enumerate(mvps):
        cx = 40 + i*(CW+gap)

        # Card
        rect(d, cx, CY, CW, CH, fill=CARD, outline=color, width=1)

        # Colored header
        rect(d, cx, CY, CW, 52, fill=color)
        txt_c(d, cx+CW//2, CY+26, title, F(20, True), BG)

        # Build info box
        cy = CY + 60
        rect(d, cx+12, cy, CW-24, 54, fill=CARD2, outline=HBORDER, width=1)
        txt(d, cx+22, cy+10, build_time, F(13, True), color, anchor="lt")
        txt(d, cx+22, cy+30, tech,       F(12),       GRAY,  anchor="lt")
        cy += 62

        line_h(d, cx+12, cy, CW-24, HBORDER, 1)
        cy += 8

        # Items — spaced_rows fills to just above rating bar
        spaced_rows(d, cx+12, cy, rating_y - 8, items, color, card_w=CW-24)

        # Rating bar at bottom of card
        rect(d, cx+12, rating_y, CW-24, rating_h-2, fill=tuple(c//4 for c in color))
        line_h(d, cx+12, rating_y, CW-24, color, 2)
        txt_c(d, cx+CW//2, rating_y + rating_h//2, rating, F(13, True), color)

    # Competition deadline banner — safe between cards and footer
    by = CY + CH + 6
    bh = H - FTR_H - 4 - by
    rect(d, 40, by, W-80, bh, fill=(25, 15, 0), outline=AMBER, width=2)
    txt_c(d, W//2, by + bh//2,
          "COMPETITION DEADLINE: AUGUST 2026  —  90 DAYS LEFT.  START NOW.",
          F(18, True), AMBER)

    footer(d)
    img.save(f"{OUT}/slide_08_mvp.png")
    print("Slide 8 done")

# ── Run ──────────────────────────────────────────────────────────────────────
slide1()
slide2()
slide3()
slide4()
slide5()
slide6()
slide7()
slide8()
print(f"\nAll 8 slides saved -> {OUT}/")

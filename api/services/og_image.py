# Qalqan AI — social share card (OpenGraph image).
# Renders a 1200x630 branded PNG so links shared in Telegram/WhatsApp/Slack get a
# real card instead of a tiny favicon. Drawn once, cached in memory for the life
# of the warm serverless instance. Pillow's scalable default font — no font files
# needed on the runtime.

import io

_CACHE: bytes | None = None

_BG = (10, 14, 22)          # --bg
_PANEL = (17, 24, 39)
_CYAN = (122, 162, 247)     # --cyan
_TX = (231, 235, 243)
_MUT = (125, 138, 160)
_GREEN = (158, 206, 106)

_SHIELD = [  # normalized lucide shield path sampled to a polygon (0..1 space)
    (0.50, 0.04), (0.78, 0.16), (0.95, 0.20), (0.95, 0.52),
    (0.78, 0.82), (0.50, 0.96), (0.22, 0.82), (0.05, 0.52),
    (0.05, 0.20), (0.22, 0.16),
]


def render_og_card() -> bytes:
    """1200x630 PNG share card. Cached after first render."""
    global _CACHE
    if _CACHE is not None:
        return _CACHE
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1200, 630
    img = Image.new("RGB", (W, H), _BG)
    d = ImageDraw.Draw(img)

    # subtle top glow band
    for y in range(0, 220):
        t = 1 - y / 220
        d.line([(0, y), (W, y)], fill=(
            int(_BG[0] + (16 - _BG[0]) * t * 0.5),
            int(_BG[1] + (23 - _BG[1]) * t * 0.5),
            int(_BG[2] + (37 - _BG[2]) * t * 0.5)))

    # shield mark (top-left of the text block)
    sx, sy, ss = 96, 150, 150
    poly = [(sx + px * ss, sy + py * ss) for px, py in _SHIELD]
    d.polygon(poly, outline=_CYAN, width=6)
    # check inside the shield
    cx, cy = sx + 0.5 * ss, sy + 0.5 * ss
    d.line([(cx - 0.16 * ss, cy), (cx - 0.03 * ss, cy + 0.13 * ss),
            (cx + 0.20 * ss, cy - 0.16 * ss)], fill=_GREEN, width=8, joint="curve")

    font_xl = ImageFont.load_default(size=96)
    font_lg = ImageFont.load_default(size=42)
    font_md = ImageFont.load_default(size=34)
    font_sm = ImageFont.load_default(size=28)

    # Latin-only text so the card renders identically on the Vercel Linux runtime
    # without bundling a Cyrillic font (Pillow's default font is Latin).
    tx = 300
    d.text((tx, 150), "Qalqan AI", font=font_xl, fill=_TX)
    d.text((tx, 268), "AI protection for Kazakhstan", font=font_lg, fill=_CYAN)
    d.text((tx, 336), "Phishing · Fraud · Pyramids · Gambling",
           font=font_md, fill=_MUT)

    # stat chips
    chips = ["97% accuracy", "F1 0.98", "0 false positives", "3 languages"]
    x = tx
    y = 430
    for c in chips:
        bb = d.textbbox((0, 0), c, font=font_sm)
        w = bb[2] - bb[0] + 44
        d.rounded_rectangle([x, y, x + w, y + 56], radius=28,
                            fill=_PANEL, outline=(30, 41, 59), width=2)
        d.text((x + 22, y + 12), c, font=font_sm, fill=_TX)
        x += w + 16

    d.text((tx, 528), "qalqan-ai-nu.vercel.app", font=font_md, fill=_MUT)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    _CACHE = buf.getvalue()
    return _CACHE


_ICON_CACHE: bytes | None = None


def render_touch_icon() -> bytes:
    """180x180 apple-touch-icon (iOS home screen): shield on the brand panel."""
    global _ICON_CACHE
    if _ICON_CACHE is not None:
        return _ICON_CACHE
    from PIL import Image, ImageDraw

    S = 180
    img = Image.new("RGB", (S, S), _PANEL)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=40, fill=_BG)
    ss, ox, oy = 120, 30, 26
    poly = [(ox + px * ss, oy + py * ss) for px, py in _SHIELD]
    d.polygon(poly, outline=_CYAN, width=7)
    cx, cy = ox + 0.5 * ss, oy + 0.5 * ss
    d.line([(cx - 0.18 * ss, cy), (cx - 0.03 * ss, cy + 0.15 * ss),
            (cx + 0.22 * ss, cy - 0.18 * ss)], fill=_GREEN, width=10, joint="curve")
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    _ICON_CACHE = buf.getvalue()
    return _ICON_CACHE

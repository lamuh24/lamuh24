"""Generate the pixel-art fighting-game SVGs used by README.md.

Everything is drawn on a low-res logical grid (viewBox) and scaled up with
crispEdges so each logical unit renders as a hard-edged pixel.
Run: python3 scripts/build_pixel_ui.py
"""
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"

# 5x7 bitmap font
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10011", "10101", "10101", "10101", "11001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "01110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    "!": ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    "?": ["01110", "10001", "00001", "00010", "00100", "00000", "00100"],
    ".": ["00000", "00000", "00000", "00000", "00000", "00000", "00100"],
    ":": ["00000", "00100", "00000", "00000", "00000", "00100", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    "+": ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    "'": ["00100", "00100", "00000", "00000", "00000", "00000", "00000"],
    " ": ["00000"] * 7,
}

def text_width(s, scale=1):
    return (len(s) * 6 - 1) * scale

def text(s, x, y, fill, scale=1):
    """Pixel text as merged horizontal runs."""
    out = []
    for i, ch in enumerate(s.upper()):
        glyph = FONT[ch]
        gx = x + i * 6 * scale
        for row, bits in enumerate(glyph):
            col = 0
            while col < 5:
                if bits[col] == "1":
                    start = col
                    while col < 5 and bits[col] == "1":
                        col += 1
                    out.append(
                        f'<rect x="{gx + start * scale}" y="{y + row * scale}" '
                        f'width="{(col - start) * scale}" height="{scale}" fill="{fill}"/>'
                    )
                else:
                    col += 1
    return "".join(out)

def outlined(s, x, y, fill, outline, scale=1, shadow=None):
    """Text with a 1-unit outline and optional drop shadow, fighting-game title style."""
    parts = []
    ring = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    if shadow:
        # solid offset silhouette behind the outlined text
        for dx, dy in ring + [(0, 0)]:
            parts.append(text(s, x + dx + scale, y + dy + scale, shadow, scale))
    for dx, dy in ring:
        parts.append(text(s, x + dx, y + dy, outline, scale))
    parts.append(text(s, x, y, fill, scale))
    return "".join(parts)

def centered(s, cx, scale=1):
    return cx - text_width(s, scale) // 2

def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"{extra}/>'

def svg(w, h, scale, body, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w * scale}" height="{h * scale}" shape-rendering="crispEdges">'
        f"<style>{style}</style>{body}</svg>\n"
    )

# Fighter sprite (16x24). Palette keys: k outline, s skin, h hair, g gi, b belt, p pants, w wrap
FIGHTER = [
    "....kkkkkk......",
    "...khhhhhhk.....",
    "..khhhhhhhhk....",
    "..khhssssshk....",
    "..khsskskssk....",
    "...kssssssk.....",
    "...kksssskk.....",
    "..kgggkkgggk....",
    ".kgggggggggggk..",
    "kggkgggggggkggk.",
    "kwwkgggggggkwwkk",
    "kwwkgggggggk.kwwk",
    ".kk.kbbbbbbk..kk",
    "....kgggggggk...",
    "....kpppppppk...",
    "...kpppkkpppk...",
    "...kpppk.kpppk..",
    "..kpppk...kpppk.",
    "..kpppk...kpppk.",
    "..kpppk....kppk.",
    ".kwwwk.....kwwwk",
    ".kssssk....kssssk",
    "kkkkkkk...kkkkkkk",
    "................",
]

def sprite(rows, x, y, palette, mirror=False):
    out = []
    width = max(len(r) for r in rows)
    for ry, row in enumerate(rows):
        row = row.ljust(width, ".")
        if mirror:
            row = row[::-1]
        for rx, c in enumerate(row):
            if c != ".":
                out.append(rect(x + rx, y + ry, 1, 1, palette[c]))
    return "".join(out)

P1 = {"k": "#14051f", "s": "#f2b78a", "h": "#2a1a12", "g": "#f4f1e8", "b": "#111111", "p": "#f4f1e8", "w": "#d63a3a"}
P2 = {"k": "#14051f", "s": "#7fd6c2", "h": "#ff2e88", "g": "#3b2d8f", "b": "#ffcc00", "p": "#241a5e", "w": "#ffcc00"}

def health_bar(x, y, w, fill_id, mirror=False):
    parts = [
        rect(x - 1, y - 1, w + 2, 8, "#14051f"),
        rect(x, y, w, 6, "#5a0e1e"),
    ]
    # yellow life with highlight stripe, drains on the P2 side
    anim = ' class="drain"' if fill_id == "p2" else ""
    origin = f' style="transform-origin:{x + w}px {y}px"' if fill_id == "p2" else ""
    parts.append(f"<g{anim}{origin}>")
    parts.append(rect(x, y, w, 6, "#ffcc00"))
    parts.append(rect(x, y, w, 2, "#fff27a"))
    parts.append(rect(x, y + 5, w, 1, "#d98a00"))
    parts.append("</g>")
    # segment ticks
    for t in range(x + 8, x + w, 8):
        parts.append(rect(t, y, 1, 6, "#14051f", ' opacity="0.25"'))
    return "".join(parts)

def build_header():
    W, H = 240, 120
    rnd = random.Random(24)
    b = []
    # banded sunset sky (no gradients: hard pixel bands)
    bands = ["#1a0b3d", "#24104f", "#33125e", "#4a1569", "#6b1a6e", "#91206b", "#bb2f5e", "#e04a4f", "#f2743f", "#ff9e3d"]
    bh = 7
    for i, c in enumerate(bands):
        b.append(rect(0, i * bh, W, bh, c))
        # dither row between bands
        if i + 1 < len(bands):
            for dx in range(i % 2, W, 2):
                b.append(rect(dx, i * bh + bh - 1, 1, 1, bands[i + 1]))
    # stars
    for _ in range(40):
        sx, sy = rnd.randrange(W), rnd.randrange(28)
        b.append(rect(sx, sy, 1, 1, "#fff6d0", ' class="twinkle"' if rnd.random() < 0.3 else ""))
    # pixel sun
    cx, cy, r = 186, 66, 14
    for yy in range(cy - r, cy + 1):
        half = int((r * r - (yy - cy) ** 2) ** 0.5)
        if (yy - cy) % 3 != 0 or yy < cy - 6:
            b.append(rect(cx - half, yy, half * 2, 1, "#ffd23f"))
    # far skyline
    x = 0
    while x < W:
        bw, bht = rnd.randint(6, 14), rnd.randint(10, 26)
        b.append(rect(x, 74 - bht, bw, bht, "#2b0f45"))
        x += bw
    # near skyline with lit windows
    x = 0
    while x < W:
        bw, bht = rnd.randint(8, 18), rnd.randint(6, 18)
        b.append(rect(x, 78 - bht, bw, bht, "#160830"))
        for wy in range(78 - bht + 2, 76, 3):
            for wx in range(x + 2, x + bw - 1, 3):
                if rnd.random() < 0.35:
                    b.append(rect(wx, wy, 1, 1, "#ffcf5c"))
        x += bw
    # palm trees (Tampa stage)
    for px in (22, 214):
        for ty in range(52, 82):
            b.append(rect(px + (ty - 52) // 10, ty, 2, 1, "#0d0420"))
        for dx, dy in [(-8, 0), (-6, -1), (-4, -2), (-2, -2), (0, -2), (2, -2), (4, -2), (6, -1), (8, 0),
                       (-9, 1), (9, 1), (-10, 2), (10, 2), (-5, -1), (5, -1)]:
            b.append(rect(px + dx, 52 + dy, 2, 1, "#0d0420"))
    # stage floor: perspective-ish checker
    b.append(rect(0, 82, W, H - 82, "#3a1f4f"))
    for row, (yy, hh) in enumerate([(82, 3), (85, 4), (89, 5), (94, 6), (100, 8), (108, 12)]):
        tile = 8 + row * 3
        off = (row % 2) * tile // 2
        for xx in range(-tile + off, W, tile * 2):
            b.append(rect(xx, yy, tile, hh, "#4f2a66"))
    b.append(rect(0, 82, W, 1, "#ff6fb5"))
    # fighters
    b.append('<g class="bob">' + sprite(FIGHTER, 52, 70, P1) + "</g>")
    b.append('<g class="bob2">' + sprite(FIGHTER, 172, 70, P2, mirror=True) + "</g>")
    # shadows
    b.append(rect(52, 93, 16, 2, "#1a0b2a", ' opacity="0.6"'))
    b.append(rect(172, 93, 16, 2, "#1a0b2a", ' opacity="0.6"'))

    # HUD
    b.append(health_bar(8, 6, 96, "p1"))
    b.append(health_bar(136, 6, 96, "p2", mirror=True))
    b.append(outlined("QUINTIN", 8, 15, "#ffffff", "#14051f"))
    b.append(outlined("THE BACKLOG", 232 - text_width("THE BACKLOG"), 15, "#ffffff", "#14051f"))
    # win pips
    for i, px in enumerate((96, 101)):
        b.append(rect(px, 15, 4, 4, "#14051f"))
        b.append(rect(px + 1, 16, 2, 2, "#ff3b3b" if i == 0 else "#55405f"))
    # timer
    b.append(rect(110, 3, 20, 14, "#14051f"))
    b.append(rect(111, 4, 18, 12, "#2a0f45"))
    b.append(outlined("99", centered("99", 120), 6, "#ffcc00", "#14051f"))

    # title
    title = "LAMUH"
    b.append(outlined(title, centered(title, 120, 3), 23, "#ffe14d", "#14051f", 3, shadow="#c2185b"))
    sub = "DEVELOPMENT SERVICES"
    b.append(outlined(sub, centered(sub, 120), 48, "#ffffff", "#14051f"))

    # ROUND 1 / FIGHT! flash
    r1 = "ROUND 1"
    b.append(f'<g class="round">{outlined(r1, centered(r1, 120, 2), 60, "#ffffff", "#14051f", 2, shadow="#14051f")}</g>')
    ft = "FIGHT!"
    b.append(f'<g class="fight">{outlined(ft, centered(ft, 120, 2), 60, "#ff3b3b", "#14051f", 2, shadow="#ffcc00")}</g>')

    # bottom ticker
    b.append(rect(0, H - 9, W, 9, "#14051f"))
    tick = "TAMPA FL - SOLO DEV - AI SYSTEMS"
    b.append(text(tick, centered(tick, 120), H - 7, "#7fd6c2"))

    style = """
    .bob{animation:bob 0.8s steps(1) infinite}
    .bob2{animation:bob 0.8s steps(1) infinite 0.4s}
    @keyframes bob{0%,49%{transform:translateY(0)}50%,100%{transform:translateY(1px)}}
    .round{animation:round 4s steps(1) infinite}
    .fight{animation:fight 4s steps(1) infinite}
    @keyframes round{0%{opacity:1}40%{opacity:0}100%{opacity:0}}
    @keyframes fight{0%{opacity:0}40%{opacity:1}48%{opacity:0}52%{opacity:1}75%{opacity:0}100%{opacity:0}}
    .drain{animation:drain 8s steps(24) infinite}
    @keyframes drain{0%{transform:scaleX(1)}80%{transform:scaleX(0.3)}100%{transform:scaleX(0.3)}}
    .twinkle{animation:tw 1.6s steps(1) infinite}
    @keyframes tw{0%{opacity:1}50%{opacity:0.2}}
    """
    return svg(W, H, 4, "".join(b), style)

def build_banner(label, accent):
    W, H = 240, 16
    b = [rect(0, 0, W, H, "#14051f")]
    # slanted plate
    for yy in range(2, 14):
        off = (14 - yy) // 2
        b.append(rect(6 + off, yy, W - 12 - 6, 1, "#2a0f45"))
    b.append(rect(6, 2, W - 12, 1, accent))
    b.append(rect(6, 13, W - 12, 1, accent))
    # chevrons
    for i in range(3):
        cx = 12 + i * 5
        for d in range(4):
            b.append(rect(cx + d, 4 + d, 2, 1, accent))
            b.append(rect(cx + d, 11 - d, 2, 1, accent))
        cx = W - 16 - i * 5
        for d in range(4):
            b.append(rect(cx + 3 - d, 4 + d, 2, 1, accent))
            b.append(rect(cx + 3 - d, 11 - d, 2, 1, accent))
    b.append(outlined(label, centered(label, 120), 5, "#ffffff", "#14051f"))
    return svg(W, H, 4, "".join(b))

def build_stats():
    stats = [("AGENTS", 10, "#ff3b3b"), ("ROUTING", 9, "#ffcc00"), ("SHIPPING", 10, "#7fd6c2"),
             ("QA", 9, "#ff6fb5"), ("SOLO", 10, "#9b7bff")]
    W, H = 240, 12 + len(stats) * 10
    b = [rect(0, 0, W, H, "#14051f"), rect(1, 1, W - 2, H - 2, "#2a0f45"), rect(2, 2, W - 4, H - 4, "#1a0b3d")]
    for i, (name, val, c) in enumerate(stats):
        y = 6 + i * 10
        b.append(text(name, 8, y, "#ffffff"))
        for s in range(10):
            on = s < val
            b.append(rect(64 + s * 13, y - 1, 12, 9, "#14051f"))
            b.append(rect(65 + s * 13, y, 10, 7, c if on else "#3a2a50"))
            if on:
                b.append(rect(65 + s * 13, y, 10, 2, "#ffffff", ' opacity="0.35"'))
        label = "MAX" if val == 10 else f"{val}/10"
        b.append(text(label, 232 - text_width(label), y, "#ffcc00" if val == 10 else "#ffffff"))
    return svg(W, H, 4, "".join(b))

def build_footer():
    W, H = 240, 40
    b = [rect(0, 0, W, H, "#14051f")]
    for yy in range(0, H, 2):
        b.append(rect(0, yy, W, 1, "#1d0a33"))
    ko = "K.O."
    b.append(f'<g class="ko">{outlined(ko, centered(ko, 120, 3), 4, "#ff3b3b", "#ffffff", 3, shadow="#ffcc00")}</g>')
    msg = "PRESS START TO COLLABORATE"
    b.append(f'<g class="blink">{text(msg, centered(msg, 120), 30, "#ffcc00")}</g>')
    style = """
    .blink{animation:bl 1s steps(1) infinite}
    @keyframes bl{0%{opacity:1}50%{opacity:0}}
    .ko{animation:ko 2.4s steps(1) infinite}
    @keyframes ko{0%{transform:translate(0,0)}5%{transform:translate(1px,0)}10%{transform:translate(-1px,1px)}15%{transform:translate(0,0)}}
    """
    return svg(W, H, 4, "".join(b), style)

def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "header.svg").write_text(build_header())
    (OUT / "stats.svg").write_text(build_stats())
    (OUT / "footer.svg").write_text(build_footer())
    banners = {
        "select-fighter": ("SELECT YOUR FIGHTER", "#ff3b3b"),
        "move-list": ("MOVE LIST", "#ffcc00"),
        "stages-cleared": ("STAGES CLEARED", "#7fd6c2"),
        "final-boss": ("FINAL BOSS", "#ff6fb5"),
    }
    for name, (label, accent) in banners.items():
        (OUT / f"banner-{name}.svg").write_text(build_banner(label, accent))

if __name__ == "__main__":
    main()

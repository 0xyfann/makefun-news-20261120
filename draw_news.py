#!/usr/bin/env python3
"""Draw a deterministic, self-contained 1024x1024 news front page."""
import struct
import zlib

W = H = 1024
PIXELS = bytearray(W * H * 3)

# The complete bitmap alphabet is hand-defined here; each glyph is 5 by 7.
GLYPHS = {
    'A': ('01110','10001','10001','11111','10001','10001','10001'),
    'B': ('11110','10001','10001','11110','10001','10001','11110'),
    'C': ('01111','10000','10000','10000','10000','10000','01111'),
    'D': ('11110','10001','10001','10001','10001','10001','11110'),
    'E': ('11111','10000','10000','11110','10000','10000','11111'),
    'F': ('11111','10000','10000','11110','10000','10000','10000'),
    'G': ('01111','10000','10000','10111','10001','10001','01111'),
    'H': ('10001','10001','10001','11111','10001','10001','10001'),
    'I': ('11111','00100','00100','00100','00100','00100','11111'),
    'J': ('00111','00010','00010','00010','10010','10010','01100'),
    'K': ('10001','10010','10100','11000','10100','10010','10001'),
    'L': ('10000','10000','10000','10000','10000','10000','11111'),
    'M': ('10001','11011','10101','10101','10001','10001','10001'),
    'N': ('10001','11001','10101','10011','10001','10001','10001'),
    'O': ('01110','10001','10001','10001','10001','10001','01110'),
    'P': ('11110','10001','10001','11110','10000','10000','10000'),
    'Q': ('01110','10001','10001','10001','10101','10010','01101'),
    'R': ('11110','10001','10001','11110','10100','10010','10001'),
    'S': ('01111','10000','10000','01110','00001','00001','11110'),
    'T': ('11111','00100','00100','00100','00100','00100','00100'),
    'U': ('10001','10001','10001','10001','10001','10001','01110'),
    'V': ('10001','10001','10001','10001','10001','01010','00100'),
    'W': ('10001','10001','10001','10101','10101','10101','01010'),
    'X': ('10001','10001','01010','00100','01010','10001','10001'),
    'Y': ('10001','10001','01010','00100','00100','00100','00100'),
    'Z': ('11111','00001','00010','00100','01000','10000','11111'),
    '0': ('01110','10001','10011','10101','11001','10001','01110'),
    '1': ('00100','01100','00100','00100','00100','00100','01110'),
    '2': ('01110','10001','00001','00010','00100','01000','11111'),
    '3': ('11110','00001','00001','01110','00001','00001','11110'),
    '4': ('00010','00110','01010','10010','11111','00010','00010'),
    '5': ('11111','10000','10000','11110','00001','00001','11110'),
    '6': ('01110','10000','10000','11110','10001','10001','01110'),
    '7': ('11111','00001','00010','00100','01000','01000','01000'),
    '8': ('01110','10001','10001','01110','10001','10001','01110'),
    '9': ('01110','10001','10001','01111','00001','00001','01110'),
    ' ': ('00000',)*7,
    '.': ('00000','00000','00000','00000','00000','00110','00110'),
    ',': ('00000','00000','00000','00000','00110','00100','01000'),
    ':': ('00000','00110','00110','00000','00110','00110','00000'),
    ';': ('00000','00110','00110','00000','00110','00100','01000'),
    '!': ('00100','00100','00100','00100','00100','00000','00100'),
    '?': ('01110','10001','00001','00010','00100','00000','00100'),
    "'": ('00100','00100','00010','00000','00000','00000','00000'),
    '"': ('01010','01010','00100','00000','00000','00000','00000'),
    '-': ('00000','00000','00000','11111','00000','00000','00000'),
    '/': ('00001','00010','00010','00100','01000','01000','10000'),
    '(': ('00010','00100','01000','01000','01000','00100','00010'),
    ')': ('01000','00100','00010','00010','00010','00100','01000'),
    '+': ('00000','00100','00100','11111','00100','00100','00000'),
    '=': ('00000','11111','00000','11111','00000','00000','00000'),
    '&': ('01100','10010','10100','01000','10101','10010','01101'),
    '%': ('11001','11010','00100','01000','10110','00110','00000'),
    '$': ('00100','01111','10100','01110','00101','11110','00100'),
    '#': ('01010','11111','01010','01010','11111','01010','00000'),
    '*': ('00000','10101','01110','11111','01110','10101','00000'),
}
# Lowercase forms are separate hand-drawn glyphs so the dateline keeps its case.
GLYPHS.update({
    'a': ('00000','01110','00001','01111','10001','10011','01101'),
    'b': ('10000','10000','10110','11001','10001','10001','11110'),
    'c': ('00000','01110','10001','10000','10000','10001','01110'),
    'd': ('00001','00001','01101','10011','10001','10001','01111'),
    'e': ('00000','01110','10001','11111','10000','10001','01110'),
    'f': ('00110','01001','01000','11100','01000','01000','01000'),
    'g': ('00000','01111','10001','10001','01111','00001','01110'),
    'h': ('10000','10000','10110','11001','10001','10001','10001'),
    'i': ('00100','00000','01100','00100','00100','00100','01110'),
    'j': ('00010','00000','00110','00010','00010','10010','01100'),
    'k': ('10000','10000','10010','10100','11000','10100','10010'),
    'l': ('01100','00100','00100','00100','00100','00100','01110'),
    'm': ('00000','11010','10101','10101','10101','10101','10101'),
    'n': ('00000','10110','11001','10001','10001','10001','10001'),
    'o': ('00000','01110','10001','10001','10001','10001','01110'),
    'p': ('00000','11110','10001','10001','11110','10000','10000'),
    'q': ('00000','01111','10001','10001','01111','00001','00001'),
    'r': ('00000','10110','11001','10000','10000','10000','10000'),
    's': ('00000','01111','10000','01110','00001','00001','11110'),
    't': ('01000','01000','11100','01000','01000','01001','00110'),
    'u': ('00000','10001','10001','10001','10001','10011','01101'),
    'v': ('00000','10001','10001','10001','10001','01010','00100'),
    'w': ('00000','10001','10001','10101','10101','10101','01010'),
    'x': ('00000','10001','01010','00100','01010','10001','10001'),
    'y': ('00000','10001','10001','10001','01111','00001','01110'),
    'z': ('00000','11111','00010','00100','01000','10000','11111'),
})

PAPER = (247, 243, 231)
INK = (25, 35, 43)
MUTED = (88, 99, 104)
RED = (168, 47, 40)
GOLD = (204, 150, 56)
BLUE = (38, 91, 119)
TEAL = (43, 112, 105)
WHITE = (255, 253, 247)


def rect(x, y, w, h, color):
    x0, y0 = max(0, int(x)), max(0, int(y))
    x1, y1 = min(W, int(x + w)), min(H, int(y + h))
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        start = (yy * W + x0) * 3
        PIXELS[start:start + len(row)] = row


def line(x0, y0, x1, y1, color, thickness=1):
    x0, y0, x1, y1 = map(int, (x0, y0, x1, y1))
    dx, dy = abs(x1 - x0), abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx - dy
    while True:
        rect(x0 - thickness // 2, y0 - thickness // 2, thickness, thickness, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy


def circle(cx, cy, radius, color, filled=True, thickness=2):
    cx, cy, radius = int(cx), int(cy), int(radius)
    r2 = radius * radius
    inner = max(0, radius - thickness) ** 2
    for yy in range(max(0, cy-radius), min(H, cy+radius+1)):
        for xx in range(max(0, cx-radius), min(W, cx+radius+1)):
            d = (xx-cx)**2 + (yy-cy)**2
            if d <= r2 and (filled or d >= inner):
                rect(xx, yy, 1, 1, color)


def text_width(s, scale, spacing=1):
    return max(0, len(s.upper()) * 5 * scale + max(0, len(s)-1) * spacing * scale)


def text(x, y, s, scale, color=INK, spacing=1):
    x, y = int(x), int(y)
    for char in s:
        glyph = GLYPHS.get(char, GLYPHS[' '])
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == '1':
                    rect(x + gx*scale, y + gy*scale, scale, scale, color)
        x += 5*scale + spacing*scale


def centered(y, s, scale, color=INK, spacing=1):
    text((W - text_width(s, scale, spacing)) // 2, y, s, scale, color, spacing)


def icon(kind, x, y, color):
    """Small hand-drawn pictograms for the eight briefs below the lead."""
    x, y = int(x), int(y)
    dark = INK
    if kind == 'court':
        # Classical court facade and columns.
        line(x+4,y+22,x+54,y+22,color,4)
        line(x+7,y+20,x+29,y+7,color,3); line(x+29,y+7,x+52,y+20,color,3)
        for xx in (12,22,32,42):
            rect(x+xx,y+23,4,26,color)
        line(x+5,y+51,x+53,y+51,dark,4); line(x+1,y+56,x+57,y+56,dark,3)
    elif kind == 'voyager':
        circle(x+26,y+29,20,(99,153,177),False,3)
        circle(x+26,y+29,7,GOLD,True)
        line(x+27,y+29,x+51,y+11,color,3); line(x+48,y+9,x+55,y+12,color,3)
        line(x+50,y+9,x+49,y+17,color,3); circle(x+52,y+11,3,RED,True)
        for dx,dy in ((4,8),(48,43),(7,48)):
            circle(x+dx,y+dy,1,dark,True)
    elif kind == 'hayabusa':
        # Asteroid, probe, and a broken contact line.
        circle(x+17,y+31,16,(177,139,88),True)
        circle(x+12,y+25,3,(214,183,129),True); circle(x+23,y+36,4,(214,183,129),True)
        line(x+35,y+28,x+49,y+18,color,3); line(x+49,y+18,x+54,y+20,color,3)
        rect(x+41,y+25,12,10,BLUE); line(x+45,y+25,x+45,y+35,WHITE,1)
        line(x+38,y+41,x+44,y+46,RED,3); line(x+48,y+46,x+54,y+41,RED,3)
    elif kind == 'game':
        # Controller with buttons and a small value tag.
        line(x+9,y+22,x+47,y+22,BLUE,3); line(x+7,y+24,x+5,y+43,BLUE,3)
        line(x+5,y+43,x+16,y+48,BLUE,3); line(x+16,y+48,x+23,y+40,BLUE,3)
        line(x+23,y+40,x+38,y+40,BLUE,3); line(x+38,y+40,x+46,y+48,BLUE,3)
        line(x+46,y+48,x+55,y+42,BLUE,3); line(x+55,y+42,x+52,y+24,BLUE,3)
        line(x+12,y+31,x+20,y+31,WHITE,3); line(x+16,y+27,x+16,y+35,WHITE,3)
        circle(x+40,y+29,2,GOLD,True); circle(x+47,y+34,2,RED,True)
    elif kind == 'storm':
        circle(x+28,y+30,22,(157,194,192),False,4)
        line(x+28,y+11,x+20,y+26,TEAL,4); line(x+20,y+26,x+32,y+26,TEAL,4)
        line(x+32,y+26,x+24,y+43,TEAL,4)
        line(x+2,y+53,x+14,y+53,color,3); line(x+42,y+53,x+57,y+53,color,3)
        line(x+9,y+48,x+15,y+42,color,3); line(x+50,y+48,x+44,y+42,color,3)
    elif kind == 'europe':
        # Two speech bubbles for negotiations.
        rect(x+3,y+9,32,24,(223,235,231)); line(x+9,y+32,x+6,y+40,color,3)
        line(x+6,y+40,x+18,y+32,color,3); rect(x+22,y+24,34,24,(229,219,190))
        line(x+46,y+47,x+52,y+55,color,3); line(x+52,y+55,x+36,y+47,color,3)
        line(x+10,y+19,x+27,y+19,TEAL,2); line(x+29,y+34,x+49,y+34,GOLD,2)
    elif kind == 'tower':
        # Riyadh tower with impact marks.
        rect(x+17,y+11,27,42,(218,226,222)); line(x+17,y+11,x+30,y+3,color,3)
        line(x+30,y+3,x+44,y+11,color,3); line(x+44,y+11,x+44,y+53,color,3)
        for yy in (20,29,38,47):
            line(x+19,y+yy,x+42,y+yy,BLUE,2)
        line(x+5,y+11,x+12,y+18,RED,3); line(x+12,y+18,x+5,y+24,RED,3)
        line(x+53,y+10,x+47,y+17,RED,3); line(x+47,y+17,x+55,y+22,RED,3)
    elif kind == 'cricket':
        # Bat, ball, and three stumps.
        line(x+14,y+48,x+39,y+11,GOLD,7); line(x+10,y+53,x+17,y+43,dark,3)
        circle(x+47,y+14,6,RED,True)
        for xx in (35,43,51):
            line(x+xx,y+31,x+xx,y+53,BLUE,3)
        line(x+32,y+53,x+54,y+53,dark,3)


def card(x, y, w, h, accent, kind, headline, summary):
    rect(x, y, w, h, WHITE)
    rect(x, y, 6, h, accent)
    rect(x+14, y+13, 52, 52, (239, 235, 222))
    icon(kind, x+11, y+10, accent)
    tx = x + 73
    ty = y + 8
    for i, row in enumerate(headline):
        text(tx, ty + i*24, row, 3, accent, 1)
    body_y = ty + len(headline)*24 + 2
    for i, row in enumerate(summary):
        text(tx, body_y + i*22, row, 3, INK, 1)


def png_chunk(kind, data):
    body = kind + data
    return struct.pack('!I', len(data)) + body + struct.pack('!I', zlib.crc32(body) & 0xffffffff)


def write_png(path):
    raw = bytearray()
    stride = W * 3
    for y in range(H):
        raw.append(0)
        raw.extend(PIXELS[y*stride:(y+1)*stride])
    data = (b'\x89PNG\r\n\x1a\n'
            + png_chunk(b'IHDR', struct.pack('!2I5B', W, H, 8, 2, 0, 0, 0))
            + png_chunk(b'IDAT', zlib.compress(bytes(raw), 9))
            + png_chunk(b'IEND', b''))
    with open(path, 'wb') as f:
        f.write(data)


def build():
    rect(0, 0, W, H, PAPER)
    # Masthead and exact, brief-required publication date.
    centered(16, 'THE WORLD', 10, INK, 1)
    centered(98, 'Friday, 20 November 2026', 3, RED, 1)
    rect(32, 132, 960, 3, INK)

    # Lead: restrained two-column headline with a hand-drawn Capitol vignette.
    text(38, 149, 'WORLD / LEAD', 2, RED, 1)
    text(38, 173, 'TRUMP: IRAN DECISION', 5, INK, 1)
    text(38, 229, 'PUT OFF TO 2027', 5, RED, 1)
    text(39, 294, "TRUMP: 'NO RUSH' ON IRAN; WILL", 3, MUTED, 1)
    text(39, 318, "'SEE WHAT HAPPENS' AFTER JAN. 1.", 3, MUTED, 1)
    # Capitol building over a flag-inspired striped ground.
    rect(733, 165, 253, 196, (238, 234, 220))
    rect(747, 319, 226, 8, BLUE)
    rect(747, 334, 226, 8, WHITE)
    rect(747, 349, 226, 8, RED)
    # Dome and cupola.
    rect(838, 232, 64, 69, (223, 216, 195))
    circle(870, 232, 32, (223, 216, 195), True)
    rect(861, 211, 18, 20, GOLD)
    circle(870, 208, 6, GOLD, True)
    # Building wings, columns, steps.
    rect(759, 277, 222, 42, WHITE)
    for xx in (770, 802, 834, 866, 898, 930, 962):
        rect(xx, 282, 8, 36, BLUE)
    line(754, 275, 986, 275, INK, 4)
    line(751, 322, 982, 322, INK, 4)
    line(764, 329, 969, 329, INK, 4)
    text(770, 173, 'WASHINGTON', 2, BLUE, 1)
    rect(32, 386, 960, 2, INK)

    # Eight compact dispatches; all captions remain inside their cards.
    cw, ch = 472, 145
    xs = (32, 520)
    ys = (400, 550, 700, 850)
    card(xs[0], ys[0], cw, ch, BLUE, 'court',
         ('ICJ: MYANMAR', 'ROHINGYA GENOCIDE'),
         ('COURT RULES GENOCIDE', 'AGAINST ROHINGYA'))
    card(xs[1], ys[0], cw, ch, TEAL, 'voyager',
         ('VOYAGER 1', 'ONE LIGHT-DAY'),
         ('NASA: 24-HOUR SIGNAL', 'TO REACH THE CRAFT'))
    card(xs[0], ys[1], cw, ch, GOLD, 'hayabusa',
         ('HAYABUSA2', 'NO ASTEROID LANDING'),
         ('ENGINE DAMAGE FORCES', 'PLAN CHANGE IN JAPAN'))
    card(xs[1], ys[1], cw, ch, RED, 'game',
         ('GTA VI SALES TOP', 'THE ODYSSEY'),
         ('GTA VI TOPS FILM\'S', 'GLOBAL $1.80B GROSS'))
    card(xs[0], ys[2], cw, ch, TEAL, 'storm',
         ('CYCLONE AKVAN', 'ODISHA EVACUATES'),
         ('300,000 EVACUATED;', '423 RESCUE TEAMS', 'LANDFALL FORECAST', 'TODAY'))
    card(xs[1], ys[2], cw, ch, BLUE, 'europe',
         ('EUROPE READY TO', 'TALK WITH RUSSIA'),
         ('LEADERS SEEK TALKS', 'TO END UKRAINE WAR'))
    card(xs[0], ys[3], cw, ch, RED, 'tower',
         ('HOUTHI STRIKE', 'DAMAGES PIF TOWER'),
         ('PIF TOWER IN RIYADH', 'DAMAGED IN HOUTHI', 'ATTACK'))
    card(xs[1], ys[3], cw, ch, GOLD, 'cricket',
         ('HENRY NICHOLLS', '100 NOT OUT', 'NZ 243/5'),
         ('WELLINGTON: DAY ONE', 'INDIA VS NEW ZEALAND'))
    write_png('entry.png')


if __name__ == '__main__':
    build()

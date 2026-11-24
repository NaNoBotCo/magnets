"""Share card, 1200x630: a carnival at night under a horseshoe magnet, field lines for an aurora, and the title."""
import math, pathlib, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

out = pathlib.Path(__file__).resolve().parent.parent / "docs" / "card.jpg"
W, H, S = 1200, 630, 2
RED, BLUE, GREEN, PURPLE, GOLD, INK, STEEL = (255, 42, 60), (31, 178, 255), (88, 255, 107), (182, 103, 255), (255, 210, 60), (255, 245, 230), (201, 211, 230)
img = Image.new("RGB", (W * S, H * S))
d = ImageDraw.Draw(img)
stops = [(0, (4, 2, 10)), (.5, (23, 10, 48)), (.86, (59, 16, 70)), (1, (90, 18, 56))]
for y in range(H * S):
    u = y / (H * S)
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if a <= u <= b:
            k = (u - a) / (b - a)
            d.line([(0, y), (W * S, y)], fill=tuple(int(ca[i] + (cb[i] - ca[i]) * k) for i in range(3)))
mx, my, R = 960, 170, 92
pN, pS = (mx - R, my + R * 1.2), (mx + R, my + R * 1.2)

def B(x, y):
    bx = by = 0
    for (px, py), q in ((pN, 1), (pS, -1)):
        dx, dy = x - px, y - py
        r2 = dx * dx + dy * dy + 80
        r3 = r2 * math.sqrt(r2)
        bx += q * dx / r3
        by += q * dy / r3
    return bx, by

r = random.Random(11)
for _ in range(520):
    x, y = r.random() * W, r.random() * H * .9
    bx, by = B(x, y)
    m, a = math.hypot(bx, by), math.atan2(by, bx)
    ln = .6 + min(1, m * R * R * 9) * 6
    d.line([((x - math.cos(a) * ln) * S, (y - math.sin(a) * ln) * S), ((x + math.cos(a) * ln) * S, (y + math.sin(a) * ln) * S)], fill=tuple(int(c * (.35 + .6 * r.random())) for c in INK), width=3)
glow = Image.new("RGB", img.size)
g = ImageDraw.Draw(glow)
for k in range(9):
    a0 = -.35 * math.pi + k * 1.5 * math.pi / 8
    x, y = pN[0] + math.cos(a0) * 10, pN[1] + math.sin(a0) * 10
    pts = [(x * S, y * S)]
    for _ in range(700):
        bx, by = B(x, y)
        m = math.hypot(bx, by) or 1
        x += bx / m * 5
        y += by / m * 5
        pts.append((x * S, y * S))
        if math.hypot(x - pS[0], y - pS[1]) < 9 or not (-200 < x < W + 200 and -200 < y < H + 200):
            break
    for layer in (g, d):
        layer.line(pts, fill=PURPLE, width=5)
bb = [(mx - R) * S, (my - R) * S, (mx + R) * S, (my + R) * S]
t = int(R * .6 * S)
for layer in (g, d):
    layer.arc([bb[0] - t // 2, bb[1] - t // 2, bb[2] + t // 2, bb[3] + t // 2], 180, 271, fill=RED, width=t)
    layer.arc([bb[0] - t // 2, bb[1] - t // 2, bb[2] + t // 2, bb[3] + t // 2], 270, 360, fill=BLUE, width=t)
    layer.rectangle([(mx - R) * S - t // 2, my * S, (mx - R) * S + t // 2, (my + R * .85) * S], fill=RED)
    layer.rectangle([(mx + R) * S - t // 2, my * S, (mx + R) * S + t // 2, (my + R * .85) * S], fill=BLUE)
img = Image.blend(img, Image.composite(glow.filter(ImageFilter.GaussianBlur(26)), img, glow.filter(ImageFilter.GaussianBlur(26)).convert("L").point(lambda v: min(255, v * 2))), .55)
d = ImageDraw.Draw(img)
for sx in (-1, 1):
    d.rectangle([(mx + sx * R) * S - t // 2, (my + R * .85) * S, (mx + sx * R) * S + t // 2, (my + R * 1.2) * S], fill=STEEL)
gy = H * .93
d.rectangle([0, gy * S, W * S, H * S], fill=(13, 5, 24))

def tent(cx, tw, th, n):
    ey, top, sw, x0 = gy - th * .42, gy - th, tw * 1.16 / n, cx - tw * .58
    d.rectangle([(cx - tw / 2) * S, ey * S, (cx + tw / 2) * S, gy * S], fill=(28, 11, 46))
    for i in range(n):
        d.polygon([(cx * S, top * S), ((x0 + i * sw) * S, ey * S), ((x0 + (i + 1) * sw) * S, ey * S)], fill=(217, 205, 230) if i % 2 else (163, 22, 42))
        d.pieslice([(x0 + i * sw) * S, (ey - sw / 2) * S, (x0 + (i + 1) * sw) * S, (ey + sw / 2) * S], 0, 180, fill=(163, 22, 42) if i % 2 else (217, 205, 230))
    d.polygon([((cx - tw * .1) * S, gy * S), (cx * S, (ey + th * .1) * S), ((cx + tw * .1) * S, gy * S)], fill=(5, 2, 12))
    d.line([(cx * S, top * S), (cx * S, (top - th * .14) * S)], fill=(217, 205, 230), width=4)
    d.polygon([(cx * S, (top - th * .14) * S), ((cx + th * .11) * S, (top - th * .11) * S), (cx * S, (top - th * .08) * S)], fill=GOLD)

tent(1010, 250, 190, 10)
tent(838, 150, 120, 8)
img = img.resize((W, H), Image.LANCZOS)
d = ImageDraw.Draw(img)
F = "/System/Library/Fonts/Supplemental/"
big = ImageFont.truetype(F + "Impact.ttf", 150)
sub = ImageFont.truetype(F + "Chalkduster.ttf", 50)
small = ImageFont.truetype(F + "Impact.ttf", 34)
th = ImageFont.truetype(F + "Tahoma Bold.ttf", 40)
d.text((64, 44), "FOR THE JUGGALO FAMILY", font=small, fill=(255, 79, 216))
for word, y, fill in (("FUCKING", 90, INK), ("MAGNETS", 232, None)):
    for off, col in ((12, BLUE), (8, PURPLE), (4, RED)):
        d.text((60 + off, y + off), word, font=big, fill=col)
    if fill:
        d.text((60, y), word, font=big, fill=fill)
    else:
        w = int(d.textlength(word, font=big))
        mask = Image.new("L", (W, H), 0)
        ImageDraw.Draw(mask).text((60, y), word, font=big, fill=255)
        bar = Image.new("RGB", (W, H), BLUE)
        ImageDraw.Draw(bar).rectangle([0, 0, 60 + w // 2, H], fill=RED)
        img.paste(bar, (0, 0), mask)
        d = ImageDraw.Draw(img)
d.text((64, 408), "Here's how they work", font=sub, fill=GREEN)
d.text((64, 486), "แม่เหล็กแม่งเจ๋ง  มาดูว่ามันทำงานยังไง", font=th, fill=INK)
d.text((64, 560), "WHOOP WHOOP  ·  8 TOYS  ·  EN + TH", font=small, fill=GOLD)
img.save(out, quality=88)
print(out)

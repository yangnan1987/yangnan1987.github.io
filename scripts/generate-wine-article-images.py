"""Generate infographic images for wine brand strategy article."""
from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "images"
W, H = 1200, 675

NAVY = "#1a2a3a"
TEAL = "#1a6b8a"
BURGUNDY = "#6b1e2d"
GOLD = "#c9a227"
CREAM = "#f7f4ef"
WHITE = "#ffffff"
MUTED = "#5a6470"
LIGHT = "#e8e4dc"
WINE_RED = "#8b2332"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        r"C:\Windows\Fonts\YuGothB.ttc" if bold else r"C:\Windows\Fonts\YuGothM.ttc",
        r"C:\Windows\Fonts\meiryo.ttc",
        r"C:\Windows\Fonts\msgothic.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def new_canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, 8), fill=NAVY)
    draw.rectangle((0, H - 8, W, H), fill=NAVY)
    return img, draw


def draw_title(draw: ImageDraw.ImageDraw, title: str, subtitle: str = "") -> None:
    draw.text((48, 36), title, fill=NAVY, font=load_font(34, bold=True))
    if subtitle:
        draw.text((48, 82), subtitle, fill=TEAL, font=load_font(20))


def draw_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], fill: str = WHITE) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=16, fill=fill, outline=LIGHT, width=2)
    draw.line((x1 + 16, y1 + 8, x1 + 96, y1 + 8), fill=GOLD, width=4)


def save(img: Image.Image, name: str) -> Path:
    path = OUT / name
    img.save(path, "PNG", optimize=True)
    print(f"Saved {path}")
    return path


def draw_glass(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0, color: str = WINE_RED) -> None:
    s = scale
    bowl = [
        (cx - 55 * s, cy - 70 * s),
        (cx + 55 * s, cy - 70 * s),
        (cx + 42 * s, cy + 35 * s),
        (cx - 42 * s, cy + 35 * s),
    ]
    draw.polygon(bowl, fill=color, outline=NAVY)
    draw.rectangle((cx - 8 * s, cy + 35 * s, cx + 8 * s, cy + 95 * s), fill=WHITE, outline=NAVY)
    draw.ellipse((cx - 34 * s, cy + 90 * s, cx + 34 * s, cy + 108 * s), fill=WHITE, outline=NAVY)
    draw.polygon(
        [
            (cx - 38 * s, cy - 20 * s),
            (cx + 10 * s, cy - 55 * s),
            (cx + 30 * s, cy - 10 * s),
        ],
        fill="#ffffff55",
    )


def gen_evaluation() -> None:
    img, draw = new_canvas()
    draw_title(draw, "テイスティングは「計測」", "外観・香り・味わい・総合の4軸で価値を読み解く")
    cx, cy = W // 2, H // 2 + 20
    draw_glass(draw, cx, cy, 1.35)
    labels = [
        ("外観", "輝き・深み", cx, cy - 170),
        ("香り", "複雑性・熟成度", cx + 220, cy - 20),
        ("味わい", "骨格・バランス", cx, cy + 170),
        ("総合", "評価・価値", cx - 220, cy - 20),
    ]
    for title, sub, x, y in labels:
        draw.rounded_rectangle((x - 95, y - 38, x + 95, y + 38), radius=12, fill=WHITE, outline=TEAL, width=2)
        draw.text((x - 80, y - 24), title, fill=NAVY, font=load_font(24, bold=True))
        draw.text((x - 80, y + 2), sub, fill=MUTED, font=load_font(16))
        draw.line((x, y + 38 if y > cy else y - 38, cx, cy - 70 if y < cy else cy + 35), fill=GOLD, width=2)
    save(img, "wine-article-evaluation-20260624.png")


def gen_metrics() -> None:
    img, draw = new_canvas()
    draw_title(draw, "4つの定量的チェックポイント", "感覚をデータとして比較・鑑定する")
    items = [
        ("1", "香りの数", "5種類以上の複雑性"),
        ("2", "滑らかさ", "絹のような口当たり"),
        ("3", "密度", "果実の凝縮感"),
        ("4", "余韻", "20秒以上の持続性"),
    ]
    positions = [(70, 150), (630, 150), (70, 390), (630, 390)]
    for (num, title, sub), (x, y) in zip(items, positions):
        box = (x, y, x + 500, y + 210)
        draw_card(draw, box)
        draw.ellipse((x + 24, y + 24, x + 84, y + 84), fill=BURGUNDY)
        draw.text((x + 42, y + 36), num, fill=WHITE, font=load_font(28, bold=True))
        draw.text((x + 110, y + 36), title, fill=NAVY, font=load_font(28, bold=True))
        draw.text((x + 110, y + 78), sub, fill=MUTED, font=load_font(18))
        accent_y = y + 130
        draw.rounded_rectangle((x + 32, accent_y, x + 468, accent_y + 52), radius=10, fill="#f0ebe3")
        draw.text((x + 48, accent_y + 14), "A と B をデータとして比較", fill=TEAL, font=load_font(18))
    save(img, "wine-article-metrics-20260624.png")


def gen_aroma() -> None:
    img, draw = new_canvas()
    draw_title(draw, "香りの複雑性", "1〜2要素か、5要素以上か——時間とともに進化する")
    draw_card(draw, (60, 140, 560, 600))
    draw_card(draw, (640, 140, 1140, 600))
    draw.text((90, 170), "デイリーワイン", fill=MUTED, font=load_font(22, bold=True))
    draw.text((670, 170), "高級ワイン", fill=BURGUNDY, font=load_font(22, bold=True))
    draw.text((90, 220), "シンプル：イチゴジャムのみ", fill=NAVY, font=load_font(20))
    draw.text((670, 220), "複雑：イチゴ＋バラ＋腐葉土", fill=NAVY, font=load_font(20))
    draw.text((670, 252), "＋スパイス＋なめし皮", fill=NAVY, font=load_font(20))
    draw.rounded_rectangle((90, 290, 530, 360), radius=10, fill="#efe8e0")
    draw.text((110, 312), "時間で変化しない", fill=MUTED, font=load_font(20))
    for i, label in enumerate(["15分後", "30分後"]):
        y = 400 + i * 80
        draw.rounded_rectangle((670, y, 1110, y + 56), radius=10, fill="#efe8e0" if i else "#e3d2d6")
        draw.text((690, y + 16), f"グラス注いで{label}に香りが進化", fill=NAVY, font=load_font(18))
    draw.text((90, 420), "1〜2要素", fill=TEAL, font=load_font(42, bold=True))
    draw.text((670, 520), "5要素以上", fill=BURGUNDY, font=load_font(42, bold=True))
    save(img, "wine-article-aroma-20260624.png")


def gen_finish() -> None:
    img, draw = new_canvas()
    draw_title(draw, "余韻（コーダリー）", "1コーダリー＝1秒｜価格と比例する最大の指標")
    draw_card(draw, (60, 150, 1140, 560))

    def wave(y_base: int, length: int, amp: int, color: str) -> None:
        points = []
        for x in range(120, 120 + length * 18, 8):
            t = (x - 120) / (length * 18)
            decay = max(0, 1 - t)
            y = y_base + int(math.sin(t * 14) * amp * decay)
            points.append((x, y))
        if len(points) > 1:
            draw.line(points, fill=color, width=4)

    draw.text((120, 190), "デイリーワイン：3〜5秒で消える", fill=MUTED, font=load_font(20, bold=True))
    wave(260, 5, 18, MUTED)
    draw.text((120, 330), "高級ワイン：10〜20秒以上続く", fill=BURGUNDY, font=load_font(20, bold=True))
    wave(400, 20, 16, BURGUNDY)
    for sec, x in [(3, 180), (5, 260), (10, 520), (20, 860)]:
        draw.line((x, 470, x, 490), fill=NAVY, width=2)
        draw.text((x - 12, 498), f"{sec}s", fill=NAVY, font=load_font(16))
    draw.text((760, 190), "飲み込んだ後の香りが", fill=TEAL, font=load_font(22, bold=True))
    draw.text((760, 224), "何秒続くか？", fill=TEAL, font=load_font(22, bold=True))
    save(img, "wine-article-finish-20260624.png")


def gen_vintage() -> None:
    img, draw = new_canvas()
    draw_title(draw, "ヴィンテージ＝作品", "その年（土地）を表現する一本の物語")
    boxes = [
        ("テロワール", "その土地", 80, 180, "#d9e8ef"),
        ("気候・季節", "一年一度の物語", 340, 180, "#e8dfd3"),
        ("収穫", "最適なタイミング", 600, 180, "#ead9de"),
        ("作品", "瓶に封印", 900, 180, "#f2ead8"),
    ]
    for title, sub, x, y, fill in boxes:
        draw.rounded_rectangle((x, y, x + 200, y + 180), radius=14, fill=fill, outline=TEAL, width=2)
        draw.text((x + 20, y + 36), title, fill=NAVY, font=load_font(22, bold=True))
        draw.text((x + 20, y + 78), sub, fill=MUTED, font=load_font(16))
    for x in (280, 540, 800):
        draw.text((x + 8, 255), "×", fill=GOLD, font=load_font(34, bold=True))
    draw.text((500, 400), "→", fill=GOLD, font=load_font(48, bold=True))
    draw.rounded_rectangle((760, 390, 1100, 590), radius=18, fill=WHITE, outline=BURGUNDY, width=3)
    draw_glass(draw, 930, 470, 0.9)
    draw.text((790, 540), "Vintage = Signature of the Year", fill=NAVY, font=load_font(18, bold=True))
    save(img, "wine-article-vintage-20260624.png")


def gen_sensory() -> None:
    img, draw = new_canvas()
    draw_title(draw, "五感で見分ける実践チェック", "色合い・香り・味わい——違いを楽しむ一歩")
    sections = [
        ("1", "色合い", "濃淡・色相・透明度", "#e7eef3"),
        ("2", "香り", "果実→花→スパイス→熟成", "#efe8e0"),
        ("3", "味わい", "舌全体で広げ、余韻まで追う", "#ead9de"),
    ]
    for i, (num, title, sub, fill) in enumerate(sections):
        x = 70 + i * 370
        draw_card(draw, (x, 170, x + 330, 590), fill=fill)
        draw.ellipse((x + 28, 205, x + 88, 265), fill=TEAL)
        draw.text((x + 46, 217), num, fill=WHITE, font=load_font(28, bold=True))
        draw.text((x + 110, 215), title, fill=NAVY, font=load_font(30, bold=True))
        draw.text((x + 36, 300), sub, fill=MUTED, font=load_font(20))
        if i == 0:
            for j, c in enumerate(["#8b2332", "#a83246", "#c45c2d"]):
                draw.ellipse((x + 50 + j * 70, 390, x + 100 + j * 70, 440), fill=c, outline=NAVY)
        elif i == 1:
            draw_glass(draw, x + 165, 430, 0.75, "#d4b06a")
        else:
            draw.arc((x + 90, 380, x + 250, 520), 200, 340, fill=BURGUNDY, width=8)
            draw.text((x + 120, 500), "余韻", fill=BURGUNDY, font=load_font(20, bold=True))
    draw.text((48, 620), "Enjoy Wine, Enjoy Life", fill=TEAL, font=load_font(18))
    save(img, "wine-article-sensory-20260624.png")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gen_evaluation()
    gen_metrics()
    gen_aroma()
    gen_finish()
    gen_vintage()
    gen_sensory()


if __name__ == "__main__":
    main()

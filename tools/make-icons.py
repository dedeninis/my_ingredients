"""產生 PWA 圖示。

改動造型或配色後重跑即可：python tools/make-icons.py

圖形為 180 度翻轉後的雙門冰箱：容量較大的冷藏在上、冷凍在下，把手在左側。
內容落在中央 80% 的安全區內，因此同一張圖可同時作為 maskable 圖示使用。
"""

from PIL import Image, ImageDraw

LEAF = (46, 107, 78, 255)
WHITE = (255, 255, 255, 255)
SIZES = (192, 512)


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def make(size):
    # 以 4 倍解析度繪製再縮小，邊緣才不會有鋸齒。
    scale = 4
    s = size * scale
    image = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    rounded(draw, (0, 0, s - 1, s - 1), s * 0.22, LEAF)

    # 冰箱本體
    body = (s * 0.28, s * 0.19, s * 0.72, s * 0.81)
    rounded(draw, body, s * 0.06, WHITE)

    # 冷藏與冷凍的分隔線，翻轉後落在下三分之一
    draw.rectangle((s * 0.28, s * 0.55, s * 0.72, s * 0.575), fill=LEAF)

    # 把手（翻轉後位於左側）
    rounded(draw, (s * 0.327, s * 0.37, s * 0.365, s * 0.505), s * 0.019, LEAF)
    rounded(draw, (s * 0.327, s * 0.615, s * 0.365, s * 0.705), s * 0.019, LEAF)

    return image.resize((size, size), Image.LANCZOS)


for size in SIZES:
    path = f"icon-{size}.png"
    make(size).save(path)
    print(f"wrote {path}")

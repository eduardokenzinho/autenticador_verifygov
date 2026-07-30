from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "screenshots"
OUT.mkdir(exist_ok=True)

WIDTH = 1920
HEIGHT = 1080

GREEN = "#009440"
YELLOW = "#ffcb00"
BLUE = "#302681"
WHITE = "#ffffff"
MINT = "#eaf7ef"
MINT_STRONG = "#dff3e7"
INK = "#102519"
MUTED = "#5d7064"


def font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]

    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size=size)

    return ImageFont.load_default(size=size)


def center_text(draw, text, y, fill, size, bold=False, max_width=None, line_gap=12):
    selected = font(size, bold)
    words = text.split()
    lines = []

    if max_width:
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if draw.textlength(test, font=selected) <= max_width or not current:
                current = test
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    else:
        lines = [text]

    line_height = selected.getbbox("Hg")[3] - selected.getbbox("Hg")[1]
    for index, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=selected)
        x = (WIDTH - (bbox[2] - bbox[0])) / 2
        draw.text((x, y + index * (line_height + line_gap)), line, font=selected, fill=fill)

    return y + len(lines) * line_height + max(0, len(lines) - 1) * line_gap


def draw_background():
    image = Image.new("RGB", (WIDTH, HEIGHT), "#edf9f2")
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw.ellipse((-220, -120, 620, 720), fill=(255, 203, 0, 25))
    draw.ellipse((1260, 440, 2140, 1320), fill=(48, 38, 129, 22))
    overlay = overlay.filter(ImageFilter.GaussianBlur(90))
    return Image.alpha_composite(image.convert("RGBA"), overlay)


def draw_panel(image, panel_h):
    panel_w = 672
    x = (WIDTH - panel_w) // 2
    y = (HEIGHT - panel_h) // 2

    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((x, y + 22, x + panel_w, y + panel_h + 22), radius=38, fill=(0, 148, 64, 30))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(34)))

    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((x, y, x + panel_w, y + panel_h), radius=38, fill=WHITE)


def draw_footer(draw, base_y):
    lock_x = WIDTH // 2 - 128
    lock_y = base_y
    draw.rounded_rectangle((lock_x, lock_y + 11, lock_x + 20, lock_y + 31), radius=3, outline=MUTED, width=2)
    draw.arc((lock_x + 3, lock_y, lock_x + 17, lock_y + 19), start=180, end=360, fill=MUTED, width=2)
    draw.text((lock_x + 34, lock_y + 1), "Ambiente 100% seguro", font=font(22), fill=MUTED)

    links = "Política de Privacidade  ·  Termos de Uso"
    selected = font(21)
    text_w = draw.textlength(links, font=selected)
    draw.text(((WIDTH - text_w) / 2, lock_y + 54), links, font=selected, fill=MUTED)


def draw_accent(draw, y):
    x = (WIDTH - 112) // 2
    draw.rounded_rectangle((x, y, x + 48, y + 7), radius=4, fill=GREEN)
    draw.rectangle((x + 44, y, x + 76, y + 7), fill=YELLOW)
    draw.rounded_rectangle((x + 72, y, x + 112, y + 7), radius=4, fill=BLUE)


def draw_loading():
    image = draw_background()
    draw_panel(image, 650)
    draw = ImageDraw.Draw(image)

    ring_box = (855, 338, 1065, 548)
    draw.ellipse(ring_box, fill=MINT)
    draw.pieslice(ring_box, start=-90, end=270, fill=GREEN)
    draw.ellipse((873, 356, 1047, 530), fill=WHITE)

    selected = font(36, bold=True)
    text = "100%"
    bbox = draw.textbbox((0, 0), text, font=selected)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) / 2, 419), text, font=selected, fill=GREEN)

    draw_accent(draw, 582)
    center_text(draw, "Analisando sua conexão", 620, INK, 38, bold=True)
    center_text(draw, "Verificando integridade do acesso...", 680, GREEN, 25)
    draw_footer(draw, 760)
    image.convert("RGB").save(OUT / "parte-1-analise.png", quality=95)


def draw_shield(draw, cx, cy, scale, fill, outline=None):
    points = [
        (cx, cy - 44 * scale),
        (cx - 35 * scale, cy - 25 * scale),
        (cx - 35 * scale, cy + 14 * scale),
        (cx - 24 * scale, cy + 42 * scale),
        (cx, cy + 58 * scale),
        (cx + 24 * scale, cy + 42 * scale),
        (cx + 35 * scale, cy + 14 * scale),
        (cx + 35 * scale, cy - 25 * scale),
    ]
    draw.polygon(points, fill=fill, outline=outline)


def draw_success():
    image = draw_background()
    draw_panel(image, 830)
    draw = ImageDraw.Draw(image)

    draw.ellipse((888, 230, 1032, 374), fill=MINT_STRONG)
    draw_shield(draw, 960, 302, 0.64, "#35b86c")

    center_text(draw, "Atendimento disponível", 420, INK, 38, bold=True)
    center_text(
        draw,
        "Seu acesso está pronto. Você já pode falar com o atendimento.",
        486,
        MUTED,
        24,
        max_width=650,
        line_gap=10,
    )

    draw.rounded_rectangle((777, 591, 1143, 645), radius=27, fill="#edf8f1")
    draw_shield(draw, 811, 616, 0.18, None, GREEN)
    selected = font(20, bold=True)
    draw.text((842, 606), "Conexão protegida", font=selected, fill="#34b76c")

    draw.rounded_rectangle((792, 662, 1128, 716), radius=27, fill="#edf8f1")
    draw.line((821, 688, 831, 698, 850, 675), fill="#34b76c", width=3)
    draw.text((874, 677), "Atendimento online", font=selected, fill="#34b76c")

    button = (634, 758, 1286, 850)
    shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((button[0], button[1] + 14, button[2], button[3] + 14), radius=30, fill=(0, 148, 64, 60))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))
    draw.rounded_rectangle(button, radius=30, fill=GREEN)

    text = "Ir para atendimento"
    selected = font(28, bold=True)
    text_w = draw.textlength(text, font=selected)
    draw.text((WIDTH / 2 - text_w / 2 - 22, 790), text, font=selected, fill=WHITE)
    draw.line((1098, 804, 1130, 804), fill=WHITE, width=4)
    draw.line((1117, 790, 1131, 804, 1117, 818), fill=WHITE, width=4, joint="curve")

    draw_footer(draw, 872)
    image.convert("RGB").save(OUT / "parte-2-atendimento.png", quality=95)


if __name__ == "__main__":
    draw_loading()
    draw_success()
    print(OUT / "parte-1-analise.png")
    print(OUT / "parte-2-atendimento.png")

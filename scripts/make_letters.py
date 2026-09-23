from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
LETTERS = ROOT / "fixtures" / "letters"
WATERMARK = "SAMPLE — NOT A REAL FEMA LETTER"


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def wrap(
    draw: ImageDraw.ImageDraw, text: str, face: ImageFont.ImageFont, width: int
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and draw.textlength(candidate, font=face) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def render(text_path: Path, angle: float) -> None:
    width, height = 900, 1240
    page = Image.new("RGBA", (width, height), (250, 249, 245, 255))
    watermark = Image.new("RGBA", page.size, (0, 0, 0, 0))
    mark_draw = ImageDraw.Draw(watermark)
    mark_face = font(43)
    mark_width = mark_draw.textlength(WATERMARK, font=mark_face)
    mark_draw.text(
        ((width - mark_width) / 2, height / 2 - 24),
        WATERMARK,
        font=mark_face,
        fill=(170, 38, 38, 52),
    )
    watermark = watermark.rotate(-27, resample=Image.Resampling.BICUBIC)
    page = Image.alpha_composite(page, watermark)

    draw = ImageDraw.Draw(page)
    regular, bold = font(23), font(25)
    y = 60
    line_height = 31
    for index, source_line in enumerate(
        text_path.read_text(encoding="utf-8").splitlines()
    ):
        if not source_line:
            y += 15
            continue
        face = (
            bold
            if index < 3 or (source_line.isupper() and len(source_line) < 60)
            else regular
        )
        color = (150, 20, 20, 255) if WATERMARK in source_line else (35, 37, 39, 255)
        for line in wrap(draw, source_line, face, width - 120):
            if y + line_height > height - 55:
                raise ValueError(
                    f"Letter text does not fit on one page: {text_path.name}"
                )
            draw.text((60, y), line, font=face, fill=color)
            y += line_height

    page = page.convert("RGB")
    grain = Image.effect_noise(page.size, 5).convert("L").convert("RGB")
    page = Image.blend(page, grain, 0.018)
    page = page.rotate(
        angle, resample=Image.Resampling.BICUBIC, expand=True, fillcolor=(223, 222, 218)
    )

    photo = Image.new("RGB", (1080, 1400))
    photo_draw = ImageDraw.Draw(photo)
    for y in range(photo.height):
        shade = 235 - y * 17 // photo.height
        photo_draw.line((0, y, photo.width, y), fill=(shade, shade, shade - 2))

    position = ((photo.width - page.width) // 2, (photo.height - page.height) // 2)
    shadow = Image.new("RGBA", photo.size, (0, 0, 0, 0))
    mask = Image.new("L", page.size, 110).filter(ImageFilter.GaussianBlur(18))
    shadow.paste((25, 25, 25, 80), position, mask)
    photo = Image.alpha_composite(photo.convert("RGBA"), shadow).convert("RGB")
    photo.paste(page, position)

    grain = Image.effect_noise(photo.size, 6).convert("L").convert("RGB")
    photo = Image.blend(photo, grain, 0.02)
    photo.save(text_path.with_suffix(".png"), format="PNG", optimize=True)


def main() -> None:
    for index, text_path in enumerate(sorted(LETTERS.glob("L*.txt"))):
        render(text_path, (1.4, -2.1, 2.7)[index % 3])
    print(f"Rendered {len(list(LETTERS.glob('L*.txt')))} sample letters in {LETTERS}")


if __name__ == "__main__":
    main()

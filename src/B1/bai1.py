from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from common.grayscale import clamp_u8, rgb_to_gray


GRAY_LEVELS = 256
SHRINK_MIN = 30
SHRINK_MAX = 120


#Tính histogram H1 của ảnh xám, H1[i] là số pixel có giá trị xám i (0 <= i <= 255)
def calculate_histogram(gray_image: Image.Image) -> list[int]:
    width, height = gray_image.size
    histogram = [0 for _ in range(GRAY_LEVELS)]

    for y in range(height):
        for x in range(width):
            gray_value = gray_image.getpixel((x, y))
            histogram[gray_value] += 1

    return histogram

#Hàm này dùng để tạo bảng ánh xạ cho cân bằng histogram.
def build_equalization_table(histogram: list[int], total_pixels: int) -> list[int]:
    table = [0 for _ in range(GRAY_LEVELS)]
    cumulative_count = 0

    for gray_value in range(GRAY_LEVELS):
        cumulative_count += histogram[gray_value]
        cdf = cumulative_count / total_pixels
        table[gray_value] = clamp_u8(255 * cdf)

    return table

#áp dụng bảng ánh xạ vào ảnh xám.
def apply_lookup_table(gray_image: Image.Image, table: list[int]) -> Image.Image:
    width, height = gray_image.size
    output_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            old_value = gray_image.getpixel((x, y))
            output_image.putpixel((x, y), table[old_value])

    return output_image

#tìm mức xám nhỏ nhất và lớn nhất trong ảnh.
def min_max_gray(gray_image: Image.Image) -> tuple[int, int]:
    width, height = gray_image.size
    min_value = 255
    max_value = 0

    for y in range(height):
        for x in range(width):
            value = gray_image.getpixel((x, y))
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value

    return min_value, max_value

#lấy ảnh sau cân bằng histogram rồi co mức xám về khoảng
def shrink_histogram_range(
    gray_image: Image.Image,
    target_min: int = SHRINK_MIN,
    target_max: int = SHRINK_MAX,
) -> Image.Image:
    width, height = gray_image.size
    output_image = Image.new("L", (width, height))
    source_min, source_max = min_max_gray(gray_image)

    if source_min == source_max:
        fill_value = clamp_u8((target_min + target_max) / 2)
        for y in range(height):
            for x in range(width):
                output_image.putpixel((x, y), fill_value)
        return output_image

    scale = (target_max - target_min) / (source_max - source_min)
    for y in range(height):
        for x in range(width):
            old_value = gray_image.getpixel((x, y))
            new_value = scale * (old_value - source_min) + target_min
            output_image.putpixel((x, y), clamp_u8(new_value))

    return output_image

#Vẽ biểu đồ histogram và lưu vào output_path
def draw_histogram(
    histogram: list[int],
    output_path: Path,
    title: str,
    width: int = 768,
    height: int = 420,
) -> None:
    margin_left = 48
    margin_right = 16
    margin_top = 36
    margin_bottom = 44
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    max_count = max(histogram)

    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    axis_color = (40, 40, 40)
    bar_color = (50, 115, 190)
    text_color = (20, 20, 20)
    grid_color = (225, 225, 225)

    x0 = margin_left
    y0 = margin_top + plot_height
    x1 = margin_left + plot_width
    y1 = margin_top

    for i in range(5):
        y = y0 - round(i * plot_height / 4)
        draw.line((x0, y, x1, y), fill=grid_color)

    draw.line((x0, y0, x1, y0), fill=axis_color, width=2)
    draw.line((x0, y0, x0, y1), fill=axis_color, width=2)
    draw.text((margin_left, 10), title, fill=text_color)
    draw.text((margin_left, height - 28), "0", fill=text_color)
    draw.text((x1 - 20, height - 28), "255", fill=text_color)
    draw.text((8, margin_top - 5), str(max_count), fill=text_color)

    if max_count > 0:
        for gray_value, count in enumerate(histogram):
            bar_x = x0 + round(gray_value * plot_width / (GRAY_LEVELS - 1))
            bar_height = round(count * plot_height / max_count)
            draw.line((bar_x, y0, bar_x, y0 - bar_height), fill=bar_color)

    canvas.save(output_path)


def save_text_histogram(histogram: list[int], output_path: Path) -> None:
    lines = ["gray_value,count\n"]
    for gray_value, count in enumerate(histogram):
        lines.append(f"{gray_value},{count}\n")
    output_path.write_text("".join(lines), encoding="utf-8")


def input_images(input_dir: Path) -> Iterable[Path]:
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def process_image(image_path: Path, output_root: Path) -> None:
    image_name = image_path.stem
    output_dir = output_root / image_name / "B1"
    output_dir.mkdir(parents=True, exist_ok=True)

    original_image = Image.open(image_path)

    gray_image = rgb_to_gray(original_image)
    h1 = calculate_histogram(gray_image)

    total_pixels = gray_image.size[0] * gray_image.size[1]
    equalization_table = build_equalization_table(h1, total_pixels)
    equalized_image = apply_lookup_table(gray_image, equalization_table)
    h2 = calculate_histogram(equalized_image)

    shrink_image = shrink_histogram_range(equalized_image)
    h_shrink = calculate_histogram(shrink_image)

    gray_image.save(output_dir / "01_gray.png")
    draw_histogram(h1, output_dir / "02_H1_histogram.png", "H1 - original gray histogram")
    save_text_histogram(h1, output_dir / "02_H1_histogram.csv")

    equalized_image.save(output_dir / "03_equalized.png")
    draw_histogram(h2, output_dir / "04_H2_equalized_histogram.png", "H2 - equalized histogram")
    save_text_histogram(h2, output_dir / "04_H2_equalized_histogram.csv")

    shrink_image.save(output_dir / "05_shrink_30_120.png")
    draw_histogram(
        h_shrink,
        output_dir / "06_H_shrink_30_120_histogram.png",
        "Histogram after shrinking to 30..120",
    )
    save_text_histogram(h_shrink, output_dir / "06_H_shrink_30_120_histogram.csv")

    print(f"Done {image_path.name} -> {output_dir}")


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Bai 1: grayscale, histogram, equalization, shrink range.")
    parser.add_argument("--input-dir", type=Path, default=project_root / "input")
    parser.add_argument("--output-dir", type=Path, default=project_root / "output")
    parser.add_argument("--image", type=Path, help="Optional path to process only one image.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.image:
        image_paths = [args.image]
    else:
        image_paths = list(input_images(args.input_dir))

    if not image_paths:
        raise FileNotFoundError(f"No input images found in {args.input_dir}")

    for image_path in image_paths:
        process_image(image_path, args.output_dir)


if __name__ == "__main__":
    main()

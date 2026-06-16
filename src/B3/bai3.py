from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from common.grayscale import Matrix, clamp_u8, rgb_to_gray_matrix


GRAY_LEVELS = 256


def clamp_index(value: int, lower: int, upper: int) -> int:
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value


def matrix_height(matrix: Matrix) -> int:
    return len(matrix)


def matrix_width(matrix: Matrix) -> int:
    if not matrix:
        return 0
    return len(matrix[0])


def matrix_to_image(matrix: Matrix) -> Image.Image:
    height = matrix_height(matrix)
    width = matrix_width(matrix)
    image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            image.putpixel((x, y), clamp_u8(matrix[y][x]))

    return image


def get_replicate(matrix: Matrix, x: int, y: int) -> int:
    height = matrix_height(matrix)
    width = matrix_width(matrix)
    safe_x = clamp_index(x, 0, width - 1)
    safe_y = clamp_index(y, 0, height - 1)
    return matrix[safe_y][safe_x]


def bilinear_interpolate(matrix: Matrix, x: float, y: float) -> float:
    x1 = math.floor(x)
    y1 = math.floor(y)
    x2 = x1 + 1
    y2 = y1 + 1

    a = x - x1
    b = y - y1

    top_left = get_replicate(matrix, x1, y1)
    top_right = get_replicate(matrix, x2, y1)
    bottom_left = get_replicate(matrix, x1, y2)
    bottom_right = get_replicate(matrix, x2, y2)

    return (
        (1 - a) * (1 - b) * top_left
        + a * (1 - b) * top_right
        + (1 - a) * b * bottom_left
        + a * b * bottom_right
    )


def bits_to_decimal(bits: list[int], start: int) -> int:
    value = 0
    weight = 1

    for offset in range(8):
        value += bits[start + offset] * weight
        weight *= 2

    return value


def largest_group_value(bits: list[int]) -> int:
    group_count = len(bits) // 8
    largest = 0

    for group_index in range(group_count):
        value = bits_to_decimal(bits, group_index * 8)
        if value > largest:
            largest = value

    return largest


def lbp_pixel_value(matrix: Matrix, center_x: int, center_y: int, neighbors: int, radius: int) -> int:
    center_value = matrix[center_y][center_x]
    bits: list[int] = []

    for p in range(neighbors):
        angle = 2 * math.pi * p / neighbors
        sample_x = center_x + radius * math.cos(angle)
        sample_y = center_y - radius * math.sin(angle)
        sample_value = bilinear_interpolate(matrix, sample_x, sample_y)

        if sample_value >= center_value:
            bits.append(1)
        else:
            bits.append(0)

    return largest_group_value(bits)


def lbp_image(matrix: Matrix, neighbors: int, radius: int) -> Matrix:
    height = matrix_height(matrix)
    width = matrix_width(matrix)
    output: Matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            output[y][x] = lbp_pixel_value(matrix, x, y, neighbors, radius)

    return output


def calculate_histogram(matrix: Matrix) -> list[int]:
    histogram = [0 for _ in range(GRAY_LEVELS)]
    height = matrix_height(matrix)
    width = matrix_width(matrix)

    for y in range(height):
        for x in range(width):
            histogram[matrix[y][x]] += 1

    return histogram


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


def save_matrix(matrix: Matrix, path: Path) -> None:
    matrix_to_image(matrix).save(path)


def process_image(image_path: Path, output_root: Path) -> None:
    output_dir = output_root / image_path.stem / "B3"
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(image_path)
    gray = rgb_to_gray_matrix(image)
    save_matrix(gray, output_dir / "00_gray.png")

    configs = [
        (8, 1, "01_lbp_p8_r1"),
        (8, 2, "02_lbp_p8_r2"),
        (16, 2, "03_lbp_p16_r2"),
        (16, 3, "04_lbp_p16_r3"),
        (24, 3, "05_lbp_p24_r3"),
    ]

    for neighbors, radius, name in configs:
        lbp = lbp_image(gray, neighbors, radius)
        save_matrix(lbp, output_dir / f"{name}.png")
        save_text_histogram(calculate_histogram(lbp), output_dir / f"{name}_histogram.csv")

    print(f"Done {image_path.name} -> {output_dir}")


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Bai 3: Local Binary Patterns.")
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

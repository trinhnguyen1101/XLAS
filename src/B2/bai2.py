from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from common.grayscale import Matrix, clamp_u8, rgb_to_gray_matrix


Kernel = list[list[float]]


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


def pad_matrix(matrix: Matrix, padding: int, value: int = 0) -> Matrix:
    if padding <= 0:
        return [row[:] for row in matrix]

    old_height = matrix_height(matrix)
    old_width = matrix_width(matrix)
    new_height = old_height + 2 * padding
    new_width = old_width + 2 * padding
    padded: Matrix = [[value for _ in range(new_width)] for _ in range(new_height)]

    for y in range(old_height):
        for x in range(old_width):
            padded[y + padding][x + padding] = matrix[y][x]

    return padded


def average_kernel(size: int) -> Kernel:
    weight = 1.0 / (size * size)
    return [[weight for _ in range(size)] for _ in range(size)]


def rotate_kernel_180(kernel: Kernel) -> Kernel:
    height = len(kernel)
    width = len(kernel[0])
    rotated: Kernel = [[0.0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            rotated[y][x] = kernel[height - 1 - y][width - 1 - x]

    return rotated


def convolution2d(matrix: Matrix, kernel: Kernel, padding: int = 0, stride: int = 1) -> Matrix:
    input_height = matrix_height(matrix)
    input_width = matrix_width(matrix)
    kernel_height = len(kernel)
    kernel_width = len(kernel[0])

    output_height = ((input_height + 2 * padding - kernel_height) // stride) + 1
    output_width = ((input_width + 2 * padding - kernel_width) // stride) + 1

    padded = pad_matrix(matrix, padding, 0)
    conv_kernel = rotate_kernel_180(kernel)
    output: Matrix = [[0 for _ in range(output_width)] for _ in range(output_height)]

    for out_y in range(output_height):
        for out_x in range(output_width):
            total = 0.0
            start_y = out_y * stride
            start_x = out_x * stride

            for ky in range(kernel_height):
                for kx in range(kernel_width):
                    pixel_value = padded[start_y + ky][start_x + kx]
                    kernel_value = conv_kernel[ky][kx]
                    total += pixel_value * kernel_value

            output[out_y][out_x] = clamp_u8(total)

    return output


def insertion_sort(values: list[int]) -> list[int]:
    sorted_values = values[:]

    for i in range(1, len(sorted_values)):
        current = sorted_values[i]
        j = i - 1
        while j >= 0 and sorted_values[j] > current:
            sorted_values[j + 1] = sorted_values[j]
            j -= 1
        sorted_values[j + 1] = current

    return sorted_values


def median_filter(matrix: Matrix, size: int = 3, padding: int = 1) -> Matrix:
    input_height = matrix_height(matrix)
    input_width = matrix_width(matrix)
    padded = pad_matrix(matrix, padding, 0)
    output: Matrix = [[0 for _ in range(input_width)] for _ in range(input_height)]

    for y in range(input_height):
        for x in range(input_width):
            neighbors: list[int] = []

            for ky in range(size):
                for kx in range(size):
                    neighbors.append(padded[y + ky][x + kx])

            sorted_neighbors = insertion_sort(neighbors)
            output[y][x] = sorted_neighbors[len(sorted_neighbors) // 2]

    return output


def mean_filter(matrix: Matrix, size: int = 5, padding: int = 2) -> Matrix:
    return convolution2d(matrix, average_kernel(size), padding=padding, stride=1)


def pad_to_size(matrix: Matrix, target_height: int, target_width: int, value: int = 0) -> Matrix:
    old_height = matrix_height(matrix)
    old_width = matrix_width(matrix)

    if old_height > target_height or old_width > target_width:
        raise ValueError("Target size must be greater than or equal to matrix size.")

    pad_top = (target_height - old_height) // 2
    pad_left = (target_width - old_width) // 2
    padded: Matrix = [[value for _ in range(target_width)] for _ in range(target_height)]

    for y in range(old_height):
        for x in range(old_width):
            padded[y + pad_top][x + pad_left] = matrix[y][x]

    return padded


def pad_to_same_size(matrix_a: Matrix, matrix_b: Matrix) -> tuple[Matrix, Matrix]:
    target_height = max(matrix_height(matrix_a), matrix_height(matrix_b))
    target_width = max(matrix_width(matrix_a), matrix_width(matrix_b))
    return (
        pad_to_size(matrix_a, target_height, target_width, 0),
        pad_to_size(matrix_b, target_height, target_width, 0),
    )


def create_i6(i4: Matrix, i5: Matrix) -> Matrix:
    same_i4, same_i5 = pad_to_same_size(i4, i5)
    height = matrix_height(same_i5)
    width = matrix_width(same_i5)
    output: Matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if same_i4[y][x] > same_i5[y][x]:
                output[y][x] = 0
            else:
                output[y][x] = same_i5[y][x]

    return output


def input_images(input_dir: Path) -> Iterable[Path]:
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def save_matrix(matrix: Matrix, path: Path) -> None:
    matrix_to_image(matrix).save(path)


def process_image(image_path: Path, output_root: Path) -> None:
    output_dir = output_root / image_path.stem / "B2"
    output_dir.mkdir(parents=True, exist_ok=True)

    image = Image.open(image_path)
    gray = rgb_to_gray_matrix(image)

    i1 = convolution2d(gray, average_kernel(3), padding=1, stride=1)
    i2 = convolution2d(gray, average_kernel(5), padding=2, stride=1)
    i3 = convolution2d(gray, average_kernel(7), padding=3, stride=2)
    i4 = median_filter(i3, size=3, padding=1)
    i5 = mean_filter(i1, size=5, padding=2)
    i6 = create_i6(i4, i5)

    save_matrix(gray, output_dir / "00_gray.png")
    save_matrix(i1, output_dir / "01_I1_conv_3x3_p1_s1.png")
    save_matrix(i2, output_dir / "02_I2_conv_5x5_p2_s1.png")
    save_matrix(i3, output_dir / "03_I3_conv_7x7_p3_s2.png")
    save_matrix(i4, output_dir / "04_I4_median_3x3_from_I3.png")
    save_matrix(i5, output_dir / "05_I5_mean_5x5_from_I1.png")
    save_matrix(i6, output_dir / "06_I6_threshold_I4_I5.png")

    print(f"Done {image_path.name} -> {output_dir}")


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description="Bai 2: convolution, median filter, mean filter, threshold.")
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

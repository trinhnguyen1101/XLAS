from __future__ import annotations

from PIL import Image


Matrix = list[list[int]]


def clamp_u8(value: float) -> int:
    rounded = int(value + 0.5)
    if rounded < 0:
        return 0
    if rounded > 255:
        return 255
    return rounded


def get_rgb_pixel(image: Image.Image, x: int, y: int) -> tuple[int, int, int]:
    pixel = image.getpixel((x, y))

    if isinstance(pixel, int):
        return pixel, pixel, pixel

    if len(pixel) < 3:
        value = int(pixel[0])
        return value, value, value

    red = int(pixel[0])
    green = int(pixel[1])
    blue = int(pixel[2])
    return red, green, blue


def rgb_to_gray(image: Image.Image) -> Image.Image:
    width, height = image.size
    gray_image = Image.new("L", (width, height))

    for y in range(height):
        for x in range(width):
            red, green, blue = get_rgb_pixel(image, x, y)
            gray_value = 0.299 * red + 0.587 * green + 0.114 * blue
            gray_image.putpixel((x, y), clamp_u8(gray_value))

    return gray_image


def rgb_to_gray_matrix(image: Image.Image) -> Matrix:
    width, height = image.size
    gray: Matrix = [[0 for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            red, green, blue = get_rgb_pixel(image, x, y)
            gray_value = 0.299 * red + 0.587 * green + 0.114 * blue
            gray[y][x] = clamp_u8(gray_value)

    return gray

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from B1.bai1 import process_image as process_bai1
from B2.bai2 import process_image as process_bai2
from B3.bai3 import process_image as process_bai3


def input_images(input_dir: Path) -> Iterable[Path]:
    extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in extensions:
            yield path


def process_all_lessons(image_path: Path, output_dir: Path) -> None:
    print(f"\nProcessing {image_path.name}")
    process_bai1(image_path, output_dir)
    process_bai2(image_path, output_dir)
    process_bai3(image_path, output_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bai 4: run Bai 1, Bai 2, Bai 3 for input images.")
    parser.add_argument("--input-dir", type=Path, default=PROJECT_ROOT / "input")
    parser.add_argument("--output-dir", type=Path, default=PROJECT_ROOT / "output")
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
        process_all_lessons(image_path, args.output_dir)

    print("\nDone all requested lessons.")


if __name__ == "__main__":
    main()

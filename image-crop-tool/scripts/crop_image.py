#!/usr/bin/env python3
"""Crop an image using normalized coordinates."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from PIL import Image, UnidentifiedImageError
except ImportError as exc:
    raise SystemExit(
        "Error: Pillow is required. Install it with `uv add pillow 2>/dev/null || (uv venv && uv pip install pillow)`."
    ) from exc


@dataclass(frozen=True)
class CropResult:
    source: str
    output: str
    box_normalized: list[float]
    box_pixels: list[int]
    source_size: list[int]
    crop_size: list[int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crop an image with normalized 0-1 coordinates.")
    parser.add_argument("image", help="Path to the source image.")
    parser.add_argument(
        "--box",
        nargs=4,
        type=float,
        metavar=("X1", "Y1", "X2", "Y2"),
        required=True,
        help="Normalized crop box. Example: --box 0.1 0.2 0.8 0.9",
    )
    parser.add_argument("--output", required=True, help="Path for the cropped image.")
    parser.add_argument(
        "--metadata-output",
        help="Optional path for JSON metadata. If omitted, metadata is printed to stdout.",
    )
    return parser.parse_args()


def validate_box(box: list[float]) -> None:
    if len(box) != 4:
        raise ValueError("Box must contain exactly four values: x1 y1 x2 y2.")
    if not all(0 <= value <= 1 for value in box):
        raise ValueError("Coordinates must be between 0 and 1.")
    x1, y1, x2, y2 = box
    if x1 >= x2 or y1 >= y2:
        raise ValueError("Invalid bounding box: require x1 < x2 and y1 < y2.")


def crop_image(image_path: Path, box: list[float], output_path: Path) -> CropResult:
    validate_box(box)
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    if not image_path.is_file():
        raise ValueError(f"Image path is not a file: {image_path}")

    try:
        image = Image.open(image_path)
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unsupported or corrupt image file: {image_path}") from exc

    with image:
        image = image.convert("RGB")
        width, height = image.size
        x1, y1, x2, y2 = box
        pixel_box = [
            int(x1 * width),
            int(y1 * height),
            int(x2 * width),
            int(y2 * height),
        ]
        cropped = image.crop(tuple(pixel_box))
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(output_path)
        return CropResult(
            source=str(image_path),
            output=str(output_path),
            box_normalized=box,
            box_pixels=pixel_box,
            source_size=[width, height],
            crop_size=[cropped.width, cropped.height],
        )


def main() -> None:
    args = parse_args()
    try:
        result = crop_image(Path(args.image), args.box, Path(args.output))
        metadata = json.dumps(asdict(result), indent=2) + "\n"
        if args.metadata_output:
            metadata_path = Path(args.metadata_output)
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata_path.write_text(metadata, encoding="utf-8")
        else:
            print(metadata, end="")
    except (FileNotFoundError, ValueError, OSError) as exc:
        raise SystemExit(f"Error: {exc}") from exc


if __name__ == "__main__":
    main()

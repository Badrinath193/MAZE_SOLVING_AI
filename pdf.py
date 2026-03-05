from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from maze_solver.solver import SUPPORTED_IMAGE_FORMATS


def convert_images_to_pdf(folder_path: Path, output_pdf: Path) -> None:
    image_files = sorted([p for p in folder_path.iterdir() if p.suffix.lower() in SUPPORTED_IMAGE_FORMATS])
    if not image_files:
        raise ValueError(f"No supported image files found in: {folder_path}")

    images = [Image.open(img).convert("RGB") for img in image_files]
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    images[0].save(output_pdf, save_all=True, append_images=images[1:])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert solved maze images into one PDF")
    parser.add_argument("--input", default="input/solved_mazes", help="Folder containing solved images")
    parser.add_argument("--output", default="outputs/output.pdf", help="Output PDF path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    in_dir = Path(args.input).expanduser().resolve()
    out_pdf = Path(args.output).expanduser().resolve()

    if not in_dir.exists():
        raise SystemExit(f"Input folder does not exist: {in_dir}")

    convert_images_to_pdf(in_dir, out_pdf)
    print(f"Saved PDF: {out_pdf}")

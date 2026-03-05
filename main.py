from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from maze_solver.solver import SUPPORTED_IMAGE_FORMATS, solve_maze_image


def process_folder(input_dir: Path, output_dir: Path) -> int:
    image_files = sorted([p for p in input_dir.iterdir() if p.suffix.lower() in SUPPORTED_IMAGE_FORMATS])
    if not image_files:
        print(f"No supported image files found in {input_dir}")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    solved_count = 0
    for image_file in image_files:
        print(f"Processing: {image_file.name}")
        try:
            solved, path = solve_maze_image(image_file)
        except ValueError as exc:
            print(f"Skipped {image_file.name}: {exc}")
            continue

        out_file = output_dir / f"solved_{image_file.name}"
        Image.fromarray(solved).save(out_file)
        print(f"Saved {out_file} (path length: {len(path)})")
        solved_count += 1

    print(f"Completed. Solved {solved_count}/{len(image_files)} maze(s).")
    return 0 if solved_count else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch maze solver for image files.")
    parser.add_argument("--input", default="input", help="Folder containing maze images.")
    parser.add_argument("--output", default=None, help="Output folder for solved images (default: <input>/solved_mazes)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    input_dir = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve() if args.output else input_dir / "solved_mazes"

    if not input_dir.exists():
        raise SystemExit(f"Input folder does not exist: {input_dir}")

    raise SystemExit(process_folder(input_dir, output_dir))

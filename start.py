from __future__ import annotations

import argparse
import subprocess
import sys


def run(cmd: list[str]) -> None:
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.stdout:
        print(completed.stdout.strip())
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr.strip(), file=sys.stderr)
        raise SystemExit(completed.returncode)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Solve mazes and build a combined PDF report")
    parser.add_argument("--input", default="input", help="Folder containing maze images")
    parser.add_argument("--solved", default=None, help="Folder for solved images")
    parser.add_argument("--output", default="outputs/output.pdf", help="Output PDF path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    solved_dir = args.solved or f"{args.input}/solved_mazes"

    run([sys.executable, "main.py", "--input", args.input, "--output", solved_dir])
    run([sys.executable, "pdf.py", "--input", solved_dir, "--output", args.output])

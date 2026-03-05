from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class SolverConfig:
    input_dir: str = "input"
    output_dir: str = "input/solved_mazes"
    output_pdf: str = "outputs/output.pdf"
    threshold: int = 128
    path_thickness: int = 3

    @classmethod
    def from_yaml(cls, path: str | Path) -> "SolverConfig":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        image_processing = data.get("image_processing", {})
        visualization = data.get("visualization", {})
        return cls(
            threshold=128 if image_processing.get("auto_threshold", True) else 128,
            path_thickness=max(1, int(visualization.get("animation_speed", 50) // 25)),
        )

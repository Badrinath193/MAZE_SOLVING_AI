"""Maze solver package."""

from .config import SolverConfig
from .solver import (
    MazeEndpoints,
    bfs_parents,
    find_start_end,
    preprocess_image,
    reconstruct_path,
    solve_maze_image,
    visualize_solution,
)

__version__ = "2.1.0"

__all__ = [
    "SolverConfig",
    "MazeEndpoints",
    "preprocess_image",
    "find_start_end",
    "bfs_parents",
    "reconstruct_path",
    "visualize_solution",
    "solve_maze_image",
]

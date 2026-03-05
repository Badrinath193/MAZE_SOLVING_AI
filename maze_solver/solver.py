from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np
from PIL import Image


SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}


@dataclass(frozen=True)
class MazeEndpoints:
    start: tuple[int, int]
    end: tuple[int, int]


def preprocess_image(img_path: str | Path, threshold: int = 128) -> np.ndarray:
    """Load an image and convert it into a binary maze mask."""
    img = np.asarray(Image.open(img_path).convert("L"))
    return (img > threshold).astype(np.uint8) * 255


def _border_openings(binary_img: np.ndarray) -> list[tuple[int, int]]:
    rows, cols = binary_img.shape
    openings: set[tuple[int, int]] = set()

    for col in range(cols):
        if binary_img[0, col] == 255:
            openings.add((0, col))
        if binary_img[rows - 1, col] == 255:
            openings.add((rows - 1, col))

    for row in range(rows):
        if binary_img[row, 0] == 255:
            openings.add((row, 0))
        if binary_img[row, cols - 1] == 255:
            openings.add((row, cols - 1))

    return sorted(openings)


def find_start_end(binary_img: np.ndarray) -> MazeEndpoints:
    """Find two maze openings on the border to use as start/end points."""
    openings = _border_openings(binary_img)
    if len(openings) < 2:
        raise ValueError("Could not find at least two border openings in the maze image.")
    return MazeEndpoints(start=openings[0], end=openings[-1])


def bfs_parents(binary_img: np.ndarray, start: tuple[int, int], end: tuple[int, int]) -> dict[tuple[int, int], tuple[int, int]]:
    """Run BFS and return a parent map for shortest-path reconstruction."""
    rows, cols = binary_img.shape
    queue = deque([start])
    visited = np.zeros(binary_img.shape, dtype=bool)
    visited[start] = True
    parents: dict[tuple[int, int], tuple[int, int]] = {}

    for_current_neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0))

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for dx, dy in for_current_neighbors:
            nxt = (current[0] + dx, current[1] + dy)
            if 0 <= nxt[0] < rows and 0 <= nxt[1] < cols and not visited[nxt] and binary_img[nxt] == 255:
                visited[nxt] = True
                parents[nxt] = current
                queue.append(nxt)

    return parents


def reconstruct_path(parents: dict[tuple[int, int], tuple[int, int]], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    if start == end:
        return [start]
    if end not in parents:
        return []

    path = [end]
    current = end
    while current != start:
        current = parents[current]
        path.append(current)
    path.reverse()
    return path


def visualize_solution(binary_img: np.ndarray, path: Iterable[tuple[int, int]], explored: Iterable[tuple[int, int]], path_thickness: int = 3) -> np.ndarray:
    color_img = np.zeros((*binary_img.shape, 3), dtype=np.uint8)
    color_img[binary_img == 255] = [255, 255, 255]

    explored_points = list(explored)
    if explored_points:
        pts = np.asarray(explored_points)
        color_img[pts[:, 0], pts[:, 1]] = [255, 0, 0]

    path_img = np.zeros(binary_img.shape, dtype=np.uint8)
    for row, col in path:
        path_img[row, col] = 255

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (path_thickness, path_thickness))
    thick_path = cv2.dilate(path_img, kernel)
    color_img[thick_path > 0] = [0, 255, 0]
    return color_img


def solve_maze_image(img_path: str | Path, path_thickness: int = 3) -> tuple[np.ndarray, list[tuple[int, int]]]:
    binary_img = preprocess_image(img_path)
    endpoints = find_start_end(binary_img)
    parents = bfs_parents(binary_img, endpoints.start, endpoints.end)
    path = reconstruct_path(parents, endpoints.start, endpoints.end)
    if not path:
        raise ValueError("No path found between detected maze openings.")
    solved = visualize_solution(binary_img, path=path, explored=parents.keys(), path_thickness=path_thickness)
    return solved, path

import numpy as np

from maze_solver.solver import bfs_parents, find_start_end, reconstruct_path


def test_find_start_end_and_path():
    maze = np.array(
        [
            [0, 255, 0, 0],
            [0, 255, 255, 0],
            [0, 0, 255, 0],
            [0, 0, 255, 0],
        ],
        dtype=np.uint8,
    )

    endpoints = find_start_end(maze)
    assert endpoints.start == (0, 1)
    assert endpoints.end == (3, 2)

    parents = bfs_parents(maze, endpoints.start, endpoints.end)
    path = reconstruct_path(parents, endpoints.start, endpoints.end)
    assert path[0] == endpoints.start
    assert path[-1] == endpoints.end
    assert len(path) >= 2

# Maze Solver Package
__version__ = "2.0.0"
__author__ = "Badrinath193"

from .config import Config
from .image_processing.preprocessing import ImagePreprocessor
from .algorithms.pathfinding import PathFinder

__all__ = ['Config', 'ImagePreprocessor', 'PathFinder']
# MAZE_SOLVING_AI

Reliable maze solving pipeline for image mazes.

## Features
- Batch solve maze images from a folder.
- Detect maze openings from image borders.
- Compute shortest path with BFS.
- Export solved images and combine them into a PDF.
- Optional drag-and-drop desktop interface.

## Quick start
```bash
pip install -r requirements.txt
python start.py --input input --output outputs/output.pdf
```

This will:
1. Solve all supported images in `input/`.
2. Save solved images to `input/solved_mazes/`.
3. Create `outputs/output.pdf`.

## Run modules independently
```bash
python main.py --input input --output input/solved_mazes
python pdf.py --input input/solved_mazes --output outputs/output.pdf
```

## GUI mode
```bash
python interface.py
```

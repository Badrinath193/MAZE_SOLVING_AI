from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "input"
OUTPUT_PDF = ROOT / "outputs" / "output.pdf"
SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}


def open_file(path: Path) -> None:
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.run(["open", str(path)], check=False)
    else:
        subprocess.run(["xdg-open", str(path)], check=False)


def run_solver() -> None:
    try:
        INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cmd = [sys.executable, "start.py", "--input", str(INPUT_DIR), "--output", str(OUTPUT_PDF)]
        result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Unknown execution error")

        status_var.set("✅ Mazes solved successfully.")
        if OUTPUT_PDF.exists():
            open_file(OUTPUT_PDF)
        else:
            messagebox.showerror("Error", f"Output PDF not found at:\n{OUTPUT_PDF}")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to execute solver:\n{exc}")


def clear_input_folder() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        for item in INPUT_DIR.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        status_var.set("🗑 Input folder cleared.")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to clear input folder:\n{exc}")


def handle_drop(event) -> None:  # type: ignore[no-untyped-def]
    for raw_file_path in root.tk.splitlist(event.data.strip()):
        file_path = Path(raw_file_path.strip())
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_IMAGE_FORMATS:
            INPUT_DIR.mkdir(parents=True, exist_ok=True)
            shutil.copy(file_path, INPUT_DIR / file_path.name)
            status_var.set(f"📁 File copied: {file_path.name}")
        elif file_path.is_file():
            messagebox.showwarning("Warning", f"Unsupported file type: {file_path.suffix.lower()}")
        else:
            messagebox.showwarning("Warning", f"Invalid file path: {file_path}")


root = TkinterDnD.Tk()
root.title("Maze Solver File Manager")
root.geometry("520x350")
root.configure(bg="#1E1E1E")

title_label = tk.Label(root, text="📂 Maze Solver", font=("Arial", 16, "bold"), fg="white", bg="#1E1E1E")
title_label.pack(pady=10)

button_style = {"font": ("Arial", 12), "width": 20, "borderwidth": 0, "relief": "flat"}

run_button = tk.Button(root, text="▶ Solve the Maze", **button_style, bg="#007BFF", fg="white", command=run_solver)
run_button.pack(pady=5)

clear_button = tk.Button(root, text="🗑 Clear Input", **button_style, bg="#DC3545", fg="white", command=clear_input_folder)
clear_button.pack(pady=5)

drop_label = tk.Label(root, text="📂 Drag & Drop Images Here", font=("Arial", 12), bg="#444", fg="white", padx=10, pady=5, relief="ridge")
drop_label.pack(pady=15, fill="x", padx=20)
drop_label.drop_target_register(DND_FILES)
drop_label.dnd_bind("<<Drop>>", handle_drop)

status_var = tk.StringVar(value=f"Input folder: {INPUT_DIR}")
status_label = tk.Label(root, textvariable=status_var, font=("Arial", 10), fg="lightgray", bg="#1E1E1E", wraplength=500)
status_label.pack(pady=10)

root.mainloop()

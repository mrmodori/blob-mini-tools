"""Manual test for the MovementManager.

Run this script to open a small window that can be dragged by its body.
Verify that dragging with the mouse moves the window smoothly.
"""

import sys
from pathlib import Path
import tkinter as tk

# Ensure the repo root is on sys.path so `app` can be imported when this
# script is run from within the tests directory.
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.core.window_mover import MovementManager


def main() -> None:
    root = tk.Tk()
    root.geometry("200x150")

    mover = MovementManager(root)
    root.bind("<ButtonPress-1>", mover.start_move)
    root.bind("<B1-Motion>", mover.do_move)

    tk.Label(root, text="Drag me!").pack(expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()


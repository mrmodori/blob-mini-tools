"""Color picker tab widget.

This module defines the :class:`ColorTab` class which mirrors the
object‑oriented structure used by the other widgets in the application.  The
previous implementation exposed a ``create_color_tab`` function that mutated a
passed ``app`` object.  For better encapsulation, the state is now contained
within this class and all widget references live on the instance.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

from utils.tooltip import ToolTip


class ColorTab:
    """Encapsulates the color picker tab and its behaviour."""

    def __init__(self, root: tk.Misc) -> None:
        self.root = root

        # Widgets initialised during :meth:`build`.
        self.outer_frame: ttk.Frame | None = None
        self.hex_var = tk.StringVar()
        self.color_entry: ttk.Entry | None = None
        self.swatch: tk.Frame | None = None

    # ------------------------------------------------------------------
    def build(self, parent_notebook: ttk.Notebook) -> ttk.Frame:
        """Build the color picker UI and return the top-level frame."""

        self.outer_frame = ttk.Frame(parent_notebook)

        # --- Color Picker Button ---
        pick_btn = ttk.Button(
            self.outer_frame, text="Pick Color", command=self._pick_color
        )
        pick_btn.pack(pady=5, padx=10, fill="x")
        ToolTip(pick_btn, "Open a color chooser dialog")

        # --- Screen Color Picker Button ---
        pick_screen_btn = ttk.Button(
            self.outer_frame, text="Pick Screen Pixel", command=self._pick_screen_color
        )
        if not sys.platform.startswith("linux") or shutil.which("xcolor") is None:
            pick_screen_btn.configure(state="disabled")
        pick_screen_btn.pack(pady=5, padx=10, fill="x")
        ToolTip(pick_screen_btn, "Pick color from screen (Linux only with xcolor)")

        # --- Color Hex Entry (readonly) ---
        self.color_entry = ttk.Entry(
            self.outer_frame,
            textvariable=self.hex_var,
            state="readonly",
            justify="center",
        )
        self.color_entry.pack(pady=5, padx=10, fill="x")
        ToolTip(self.color_entry, "Hex color value (auto copied to clipboard)")

        # --- Color Swatch Panel ---
        self.swatch = tk.Frame(
            self.outer_frame, height=30, bg="#ffffff", relief="sunken", borderwidth=1
        )
        self.swatch.pack(pady=5, padx=10, fill="x")

        # Trace changes to update swatch colour
        self.hex_var.trace_add("write", lambda *_: self._update_swatch())

        # --- Label ---
        ttk.Label(self.outer_frame, text="Hex copied to clipboard").pack(pady=5)

        return self.outer_frame

    # ------------------------------------------------------------------
    def _pick_color(self) -> None:
        color = colorchooser.askcolor(parent=self.root, title="Choose a color")
        if color and color[1]:
            self._update_color(color[1])

    # ------------------------------------------------------------------
    def _pick_screen_color(self) -> None:
        # Hide window before picking
        self.root.withdraw()
        self.root.after(300, self._run_xcolor)

    # ------------------------------------------------------------------
    def _run_xcolor(self) -> None:
        try:
            result = subprocess.run(
                ["xcolor"], capture_output=True, text=True, timeout=10
            )
            hex_color = result.stdout.strip()
            if hex_color.startswith("#") and len(hex_color) == 7:
                self._update_color(hex_color)
        except Exception as e:  # pragma: no cover - GUI path
            messagebox.showerror("Error", f"xcolor failed: {e}")
        finally:
            self.root.deiconify()

    # ------------------------------------------------------------------
    def _update_swatch(self) -> None:
        if self.swatch is None:
            return
        value = self.hex_var.get().strip()
        if value.startswith("#") and len(value) == 7:
            try:
                self.swatch.configure(bg=value)
            except tk.TclError:
                self.swatch.configure(bg="#ffffff")
        else:
            self.swatch.configure(bg="#ffffff")

    # ------------------------------------------------------------------
    def _update_color(self, value: str) -> None:
        self.hex_var.set(value)
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(value)
        except Exception:
            pass


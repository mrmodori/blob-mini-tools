import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
import subprocess
import sys
import shutil
from utils.tooltip import ToolTip

def create_color_tab(app):
    color_tab = ttk.Frame(app.notebook)
    app.notebook.add(color_tab, text="Color")

    # --- Color Picker Button ---
    pick_btn = ttk.Button(color_tab, text="Pick Color", command=lambda: _pick_color(app))
    pick_btn.pack(pady=5, padx=10, fill='x')
    ToolTip(pick_btn, "Open a color chooser dialog")

    # --- Screen Color Picker Button ---
    pick_screen_btn = ttk.Button(color_tab, text="Pick Screen Pixel", command=lambda: _pick_screen_color(app))
    if not sys.platform.startswith('linux') or shutil.which('xcolor') is None:
        pick_screen_btn.configure(state='disabled')
    pick_screen_btn.pack(pady=5, padx=10, fill='x')
    ToolTip(pick_screen_btn, "Pick color from screen (Linux only with xcolor)")

    # --- Color Hex Entry (readonly) ---
    hex_var = tk.StringVar()
    color_entry = ttk.Entry(color_tab, textvariable=hex_var, state='readonly', justify='center')
    color_entry.pack(pady=5, padx=10, fill='x')
    ToolTip(color_entry, "Hex color value (auto copied to clipboard)")

    # --- Color Swatch Panel ---
    swatch = tk.Frame(color_tab, height=30, bg="#ffffff", relief='sunken', borderwidth=1)
    swatch.pack(pady=5, padx=10, fill='x')
    
    def update_swatch(*_):
        value = hex_var.get().strip()
        if value.startswith("#") and len(value) == 7:
            try:
                swatch.configure(bg=value)
            except tk.TclError:
                swatch.configure(bg="#ffffff")  # fallback if invalid
        else:
            swatch.configure(bg="#ffffff")

    # Trace changes to the hex value
    hex_var.trace_add('write', update_swatch)

    # --- Label ---
    ttk.Label(color_tab, text="Hex copied to clipboard").pack(pady=5)

    # Save reference for theming or updates
    app.color_hex_var = hex_var
    app.color_entry = color_entry
    app.color_swatch = swatch



def _pick_color(app):
    color = colorchooser.askcolor(parent=app.root, title="Choose a color")
    if color and color[1]:
        _update_color(app, color[1])


def _pick_screen_color(app):
    # Hide window before picking
    app.root.withdraw()
    app.root.after(300, lambda: _run_xcolor(app))


def _run_xcolor(app):
    try:
        result = subprocess.run(['xcolor'], capture_output=True, text=True, timeout=10)
        hex_color = result.stdout.strip()
        if hex_color.startswith("#") and len(hex_color) == 7:
            _update_color(app, hex_color)
    except Exception as e:
        messagebox.showerror("Error", f"xcolor failed: {e}")
    finally:
        app.root.deiconify()



def _update_color(app, value: str):
    app.color_hex_var.set(value)
    try:
        app.root.clipboard_clear()
        app.root.clipboard_append(value)
    except Exception:
        pass

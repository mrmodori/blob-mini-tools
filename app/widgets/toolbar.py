import tkinter as tk
from tkinter import ttk
from utils.tooltip import ToolTip
from core.config import CONFIG

def create_toolbar(app):
    """Create a toolbar and attach it to app.root. Requires `app.theme` and `app.borderless`."""
    toolbar = ttk.Frame(app.root, height=CONFIG["toolbar"]["height"])
    toolbar.pack(fill='x')
    
    # Adding text
    title_label = ttk.Label(toolbar, text=CONFIG["window"]["title"], anchor='w')
    title_label.pack(side='left', padx=5)

    toolbar.bind("<ButtonPress-1>", app.movement.start_move)
    toolbar.bind("<B1-Motion>", app.movement.do_move)

    # Close button
    close_btn = tk.Button(toolbar, text='✕', border=0, command=app.on_close)
    close_btn.pack(side='right', padx=(0, 5), pady=2)
    ToolTip(close_btn, "Close application")

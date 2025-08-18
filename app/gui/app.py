import tkinter as tk
from tkinter import ttk

from core.config import CONFIG
from core.window_position import load_window_position, save_window_position
from core.window_mover import MovementManager

from widgets.toolbar import create_toolbar
from widgets.notes.notes_tab import create_notes_tab
from widgets.notes.notes import load_notes, save_notes
from widgets.calc.calc_tab import create_calc_tab
from widgets.color.color_tab import create_color_tab

class MultitoolApp:
    def __init__(self, root):
        self.root = root
        self.root.resizable(False, False)
        self.root.title(CONFIG['window']['title'])
        self.root.geometry(CONFIG['window']['geometry'])
        self.root.minsize(*CONFIG['window']['minsize'])
        
        # Load saved window position
        load_window_position(self.root)

        # Init managers
        self.movement = MovementManager(self.root)

        # Setup toolbar
        create_toolbar(self)

        # Setup notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        # Load notes if available
        self.saved_notes = load_notes()

        # Add tabs
        create_notes_tab(self)
        create_calc_tab(self)
        create_color_tab(self)

        # Close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Save window position
        save_window_position(self.root)

        # Save notes
        if hasattr(self, 'notes_pages'):
            notes = [txt.get('1.0', tk.END).rstrip() for txt in self.notes_pages]
            save_notes(notes)

        self.root.destroy()

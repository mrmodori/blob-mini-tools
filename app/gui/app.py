import tkinter as tk
from tkinter import ttk

from core.config import CONFIG
from core.window_position import load_window_position, save_window_position
from core.window_mover import MovementManager

from widgets.toolbar import create_toolbar
from widgets.notes.notes_tab import NotesTab
from widgets.calc.calc_tab import CalcTab
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

        # Load notes and build tabs
        saved_notes = NotesTab.load_notes()
        self.notes_tab = NotesTab(self.root, saved_notes)
        self.notebook.add(
            self.notes_tab.build(self.notebook), text=CONFIG["notes"]["title"]
        )

        self.calc_tab = CalcTab(self.root)
        self.notebook.add(
            self.calc_tab.build(self.notebook), text=CONFIG["calc"]["title"]
        )

        create_color_tab(self)

        # Close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Save window position
        save_window_position(self.root)

        # Save notes
        self.notes_tab.save()

        self.root.destroy()

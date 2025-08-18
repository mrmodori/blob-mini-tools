"""Notes tab widget.

This module defines the :class:`NotesTab` class which encapsulates all
logic for the notes feature.  The class manages its own internal notebook
where each page represents an individual note.  A special ``+`` tab allows
the user to create new notes and a context menu lets them remove existing
ones.

The previous implementation exposed a ``create_notes_tab`` function that
mutated a passed ``app`` object.  For better encapsulation and to make the
widget easier to reuse, the functionality is now contained within this
class.  State such as the list of pages, the inner notebook widget and the
context menu live on the instance itself.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, scrolledtext

from utils.tooltip import ToolTip
from core.config import CONFIG


class NotesTab:
    """Encapsulates the Notes tab and its behaviour."""

    def __init__(self, root: tk.Misc, saved_notes: list[str] | None = None) -> None:
        """Create a new ``NotesTab``.

        Parameters
        ----------
        root:
            The root ``tk`` widget used for scheduling events and creating
            context menus.
        saved_notes:
            Optional list of notes to populate initially.  If ``None`` an
            empty note is created.
        """

        self.root = root
        self.saved_notes = saved_notes or [""]

        # Widgets created during :meth:`build`.
        self.outer_frame: ttk.Frame | None = None
        self.notes_notebook: ttk.Notebook | None = None
        self.plus_tab: ttk.Frame | None = None

        # Internal state
        self.notes_pages: list[tk.Text] = []
        self._note_menu: tk.Menu | None = None

    # ------------------------------------------------------------------
    # Building and utilities
    # ------------------------------------------------------------------
    def build(self, parent_notebook: ttk.Notebook) -> ttk.Frame:
        """Build the Notes tab and return the top-level frame.

        The returned frame is *not* added to ``parent_notebook``; the caller
        is responsible for doing so.  This keeps the class decoupled from the
        layout decisions of the application.
        """

        self.outer_frame = ttk.Frame(parent_notebook)

        # Inner notebook to hold individual note pages
        self.notes_notebook = ttk.Notebook(self.outer_frame)
        self.notes_notebook.pack(expand=True, fill="both", padx=5, pady=5)

        # ``+`` tab that is always present for creating new notes
        self.plus_tab = ttk.Frame(self.notes_notebook)

        # Create existing notes
        for i, content in enumerate(self.saved_notes):
            self._add_note_page(content, index=i + 1)

        # Add the ``+`` tab at the end
        self.notes_notebook.add(self.plus_tab, text=" + ")
        ToolTip(self.plus_tab, CONFIG["notes"]["tooltip"]["add_note"])

        # Bind tab change after a short delay to ensure the notebook exists
        def _bind_later() -> None:
            assert self.notes_notebook is not None
            self.notes_notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        self.root.after(100, _bind_later)

        return self.outer_frame

    # ------------------------------------------------------------------
    def get_notes(self) -> list[str]:
        """Return the text content for all note pages."""

        return [txt.get("1.0", tk.END).rstrip() for txt in self.notes_pages]

    # ------------------------------------------------------------------
    @staticmethod
    def _select_all(event: tk.Event) -> str | None:
        """Select all text in a ``tk.Text`` widget when ``Ctrl+A`` is pressed."""

        widget = event.widget
        if isinstance(widget, tk.Text):
            widget.tag_add("sel", "1.0", "end")
            return "break"
        return None

    # ------------------------------------------------------------------
    def _add_note_page(self, content: str = "", index: int | None = None) -> ttk.Frame:
        """Create a new note page populated with ``content``."""

        assert self.notes_notebook is not None
        frame = ttk.Frame(self.notes_notebook)
        text = scrolledtext.ScrolledText(frame, wrap="word", undo=True)
        text.pack(expand=True, fill="both")
        text.insert("1.0", content)

        text.bind("<Control-a>", self._select_all)
        text.bind("<Button-1>", lambda e, t=text: t.focus_set())
        text.bind("<Button-3>", lambda e, fr=frame: self._show_context_menu(e, fr))

        # Insert before ``+`` tab if it exists
        if self.plus_tab and str(self.plus_tab) in self.notes_notebook.tabs():
            pos = self.notes_notebook.index(self.plus_tab)
            self.notes_notebook.insert(
                pos,
                frame,
                text=f"{CONFIG['notes']['label']} {index or len(self.notes_pages) + 1}",
            )
        else:
            self.notes_notebook.add(
                frame,
                text=f"{CONFIG['notes']['label']} {index or len(self.notes_pages) + 1}",
            )

        self.notes_pages.append(text)
        return frame

    # ------------------------------------------------------------------
    def _on_tab_changed(self, event: tk.Event | None = None) -> None:
        """Handle the inner notebook tab changed event."""

        assert self.notes_notebook is not None and self.plus_tab is not None
        selected = self.notes_notebook.select()
        if selected == str(self.plus_tab):
            # Create new page
            self._add_note_page(content="", index=len(self.notes_pages) + 1)

            # Re-add the plus tab at the end
            self.notes_notebook.forget(self.plus_tab)
            self.notes_notebook.add(self.plus_tab, text=" + ")

            # Auto-select the newly added note (second last tab)
            tabs = self.notes_notebook.tabs()
            if len(tabs) >= 2:
                self.notes_notebook.select(tabs[-2])

    # ------------------------------------------------------------------
    def _show_context_menu(self, event: tk.Event, frame: ttk.Frame) -> None:
        """Display a context menu for closing note pages."""

        if len(self.notes_pages) <= 1:
            return  # don't allow removing the last note

        if self._note_menu is None:
            self._note_menu = tk.Menu(self.root, tearoff=0)
            self._note_menu.add_command(label="Close Note", command=lambda: None)

        # Always update the command before showing the menu
        self._note_menu.entryconfigure(0, command=lambda fr=frame: self._close_note_page(fr))

        try:
            self._note_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self._note_menu.grab_release()

    # ------------------------------------------------------------------
    def _close_note_page(self, frame: ttk.Frame) -> None:
        """Close the provided note page."""

        if len(self.notes_pages) <= 1:
            return

        assert self.notes_notebook is not None and self.plus_tab is not None

        try:
            idx = self.notes_notebook.index(frame)
        except Exception:
            return

        # Prevent accidental selection of the ``+`` tab
        selected_tab = self.notes_notebook.select()
        if selected_tab == str(frame):
            for tab_id in self.notes_notebook.tabs():
                if tab_id not in (str(frame), str(self.plus_tab)):
                    self.notes_notebook.select(tab_id)
                    break

        if idx < len(self.notes_pages):
            del self.notes_pages[idx]

        self.notes_notebook.forget(frame)

        # Re-label remaining tabs sequentially
        for i, tab_id in enumerate(self.notes_notebook.tabs()):
            if tab_id == str(self.plus_tab):
                continue
            self.notes_notebook.tab(tab_id, text=f"{CONFIG['notes']['label']} {i + 1}")


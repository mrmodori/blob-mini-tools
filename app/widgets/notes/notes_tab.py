import tkinter as tk
from tkinter import ttk, scrolledtext
from utils.tooltip import ToolTip
from core.config import CONFIG
def create_notes_tab(app):
    # Outer tab for Notes in main notebook
    notes_tab = ttk.Frame(app.notebook)
    app.notebook.add(notes_tab, text=CONFIG["notes"]["title"])

    # Inner notebook for individual note pages
    app.notes_notebook = ttk.Notebook(notes_tab)
    app.notes_notebook.pack(expand=True, fill='both', padx=5, pady=5)
    
    # Store references to text widgets
    app.notes_pages = []

    # Load saved notes (or create one empty)
    if not hasattr(app, 'saved_notes'):
        app.saved_notes = [""]

    # Add the "+" tab first so it's available during _add_note_page
    app.plus_tab = ttk.Frame(app.notes_notebook)

    # Now add existing notes
    for i, content in enumerate(app.saved_notes):
        _add_note_page(app, content, index=i + 1)

    app.notes_notebook.add(app.plus_tab, text=" + ")
    ToolTip(app.plus_tab, CONFIG["notes"]["tooltip"]["add_note"])

    def _bind_later():
        app.notes_notebook.bind("<<NotebookTabChanged>>", lambda e: _on_tab_changed(app))

    app.root.after(100, _bind_later)

def _select_all(event):
    widget = event.widget
    if isinstance(widget, tk.Text):
        widget.tag_add('sel', '1.0', 'end')
        return 'break'


def _add_note_page(app, content="", index=None):
    frame = ttk.Frame(app.notes_notebook)
    text = scrolledtext.ScrolledText(frame, wrap='word', undo=True)
    text.pack(expand=True, fill='both')
    text.insert('1.0', content)
    
    text.bind('<Control-a>', _select_all)
    text.bind('<Button-1>', lambda e, t=text: t.focus_set())
    text.bind('<Button-3>', lambda e, fr=frame: _show_context_menu(app, e, fr))

    # Add to tab before "+" or at end
    if app.plus_tab and str(app.plus_tab) in app.notes_notebook.tabs():
        pos = app.notes_notebook.index(app.plus_tab)
        app.notes_notebook.insert(pos, frame, text=f"{CONFIG['notes']['label']} {index or len(app.notes_pages) + 1}")
    else:
        app.notes_notebook.add(frame, text=f"{CONFIG['notes']['label']} {index or len(app.notes_pages) + 1}")

    app.notes_pages.append(text)
    return frame


def _on_tab_changed(app):
    selected = app.notes_notebook.select()
    if selected == str(app.plus_tab):
        # Create new page
        _add_note_page(app, content="", index=len(app.notes_pages) + 1)
        # Re-add plus tab at the end
        app.notes_notebook.forget(app.plus_tab)
        app.notes_notebook.add(app.plus_tab, text=" + ")
        # Auto-select the newly added note
        tabs = app.notes_notebook.tabs()
        if len(tabs) >= 2:
            app.notes_notebook.select(tabs[-2])


def _show_context_menu(app, event, frame):
    if len(app.notes_pages) <= 1:
        return  # don't allow removing the last note

    if not hasattr(app, '_note_menu'):
        app._note_menu = tk.Menu(app.root, tearoff=0)
        app._note_menu.add_command(label="Close Note", command=lambda: None)

    # Always update the command before showing the menu
    app._note_menu.entryconfigure(0, command=lambda fr=frame: _close_note_page(app, fr))

    try:
        app._note_menu.tk_popup(event.x_root, event.y_root)
    finally:
        app._note_menu.grab_release()



def _close_note_page(app, frame):
    if len(app.notes_pages) <= 1:
        return

    try:
        idx = app.notes_notebook.index(frame)
    except Exception:
        return

    # PREVENT accidental "+ tab" selection
    selected_tab = app.notes_notebook.select()
    if selected_tab == str(frame):
        # Choose first non-plus tab (or another valid fallback)
        for tab_id in app.notes_notebook.tabs():
            if tab_id != str(frame) and tab_id != str(app.plus_tab):
                app.notes_notebook.select(tab_id)
                break

    # Remove page from internal list
    if idx < len(app.notes_pages):
        del app.notes_pages[idx]

    # Remove tab frame
    app.notes_notebook.forget(frame)

    # Re-label tabs to be sequential
    for i, tab_id in enumerate(app.notes_notebook.tabs()):
        if tab_id == str(app.plus_tab):
            continue
        app.notes_notebook.tab(tab_id, text=f"{CONFIG['notes']['label']} {i + 1}")

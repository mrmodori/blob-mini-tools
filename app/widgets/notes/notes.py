import json

NOTES_FILE = "notes.json"

def load_notes():
    """Load saved notes from file or return a default list."""
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [""]

def save_notes(notes):
    """Persist notes to the notes file."""
    try:
        with open(NOTES_FILE, "w", encoding="utf-8") as f:
            json.dump(notes, f)
    except Exception:
        pass

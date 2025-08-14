import os
import json

POS_FILE = "winpos.json"

def load_window_position(root):
    """Apply saved geometry (if available) to the root window."""
    if os.path.exists(POS_FILE):
        try:
            with open(POS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            geometry = data.get("geometry")
            if geometry:
                root.geometry(geometry)
        except Exception:
            pass

def save_window_position(root):
    """Store current geometry to file."""
    data = {"geometry": root.geometry()}
    try:
        with open(POS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f)
    except Exception:
        pass

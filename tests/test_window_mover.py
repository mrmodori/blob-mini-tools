import types
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.window_mover import MovementManager


class DummyRoot:
    """Minimal stand-in for a tkinter root window."""

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y
        self.geometry_calls = []

    def winfo_x(self):
        return self._x

    def winfo_y(self):
        return self._y

    def geometry(self, value):
        self.geometry_calls.append(value)
        # Update internal coordinates for subsequent queries
        x_str, y_str = value.lstrip("+").split("+")
        self._x = int(x_str)
        self._y = int(y_str)


def make_event(x_root, y_root):
    return types.SimpleNamespace(x_root=x_root, y_root=y_root)


def test_do_move_applies_deltas_to_window_position():
    root = DummyRoot(x=100, y=200)
    mover = MovementManager(root)

    mover.start_move(make_event(300, 400))
    mover.do_move(make_event(310, 415))

    assert root.geometry_calls[-1] == "+110+215"


def test_sequential_moves_are_based_on_initial_cursor_start():
    root = DummyRoot(x=100, y=200)
    mover = MovementManager(root)

    mover.start_move(make_event(300, 400))
    mover.do_move(make_event(305, 405))
    mover.do_move(make_event(310, 415))

    assert root.geometry_calls == ["+105+205", "+110+215"]


import types
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.core.window_mover import MovementManager

class DummyRoot:
    """Tiny stand-in for a tkinter root; records geometry calls."""
    def __init__(self, x=0, y=0):
        self._x, self._y = x, y
        self.geometry_calls = []

    def winfo_x(self): return self._x
    def winfo_y(self): return self._y

    def geometry(self, value):
        # Record "+X+Y" and update internal coords so subsequent reads are realistic.
        self.geometry_calls.append(value)
        x_str, y_str = value.lstrip("+").split("+")
        self._x, self._y = int(x_str), int(y_str)

def ev(x, y):  # minimal event-like object
    return types.SimpleNamespace(x_root=x, y_root=y)

import pytest

@pytest.mark.parametrize(
    "start_xy, anchor_xy, move_xy, expect_geometry",
    [
        # +10,+15 movement from (100,200) -> "+110+215"
        ((100, 200), (300, 400), (310, 415), "+110+215"),
        # Negative movement: -20,-5 from (100,200) -> "+80+195"
        ((100, 200), (300, 400), (280, 395), "+80+195"),
        # Zero movement: no change -> "+100+200"
        ((100, 200), (300, 400), (300, 400), "+100+200"),
    ],
)
def test_window_move_is_anchor_delta_based(start_xy, anchor_xy, move_xy, expect_geometry):
    # STEP 1: Create window at known coords.
    root = DummyRoot(*start_xy)
    mover = MovementManager(root)

    # STEP 2: Press/anchor at initial cursor position (start of drag).
    mover.start_move(ev(*anchor_xy))

    # STEP 3: Drag to new cursor position; expect window = start + (cursor_delta).
    mover.do_move(ev(*move_xy))
    assert root.geometry_calls[-1] == expect_geometry

def test_multiple_moves_use_same_anchor_for_consistency():
    # STEP 1: Start at (100,200).
    root = DummyRoot(100, 200)
    mover = MovementManager(root)

    # STEP 2: Anchor once at (300,400).
    mover.start_move(ev(300, 400))

    # STEP 3: Two moves; each recomputed from the original anchor (no cumulative drift).
    mover.do_move(ev(305, 405))
    mover.do_move(ev(310, 415))

    assert root.geometry_calls == ["+105+205", "+110+215"]

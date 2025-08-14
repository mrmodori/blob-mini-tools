class MovementManager:
    def __init__(self, root):
        self.root = root
        self.borderless = False
        self._saved_geometry = None
        self._drag_start_x = 0
        self._drag_start_y = 0

    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def do_move(self, event):
        dx = event.x_root - self._drag_start_x
        dy = event.y_root - self._drag_start_y
        self.root.geometry(f"+{dx}+{dy}")

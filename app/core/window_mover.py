class MovementManager:
    def __init__(self, root):
        self.root = root
        self.borderless = False
        self._saved_geometry = None
        self._cursor_start_x = 0
        self._cursor_start_y = 0
        self._win_start_x = 0
        self._win_start_y = 0

    def start_move(self, event):
        self._cursor_start_x = event.x_root
        self._cursor_start_y = event.y_root
        self._win_start_x = self.root.winfo_x()
        self._win_start_y = self.root.winfo_y()

    def do_move(self, event):
        dx = event.x_root - self._cursor_start_x
        dy = event.y_root - self._cursor_start_y
        new_x = self._win_start_x + dx
        new_y = self._win_start_y + dy
        self.root.geometry(f"+{new_x}+{new_y}")

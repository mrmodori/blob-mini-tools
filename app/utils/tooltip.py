import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay  # milliseconds
        self.tipwindow = None
        self._after_id = None

        self.widget.bind("<Enter>", self._on_enter)
        self.widget.bind("<Leave>", self._on_leave)

    def _on_enter(self, _event):
        self._schedule()

    def _on_leave(self, _event):
        self._unschedule()
        self._hide_tip()

    def _schedule(self):
        self._unschedule()
        self._after_id = self.widget.after(self.delay, self._show_tip)

    def _unschedule(self):
        if self._after_id:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show_tip(self):
        if self.tipwindow or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify='left',
            background='#ffffe0',
            foreground='#000000',
            relief='solid',
            borderwidth=1,
            font=('TkDefaultFont', 9)
        )
        label.pack(ipadx=1)

    def _hide_tip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

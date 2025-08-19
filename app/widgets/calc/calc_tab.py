import tkinter as tk
from tkinter import ttk, Listbox
from utils.safe_eval import SafeEvaluator
from utils.tooltip import ToolTip
from core.config import CONFIG


class CalcTab:
    """Encapsulates the calculator tab and its state."""

    def __init__(self, root: tk.Misc) -> None:
        self.root = root
        self.evaluator = SafeEvaluator()

        # Widgets initialized in build()
        self.outer_frame: ttk.Frame | None = None
        self.result_var = tk.StringVar(value="")
        self.result_entry: ttk.Entry | None = None
        self.input_entry: ttk.Entry | None = None
        self.history_list: Listbox | None = None

    def build(self, parent_notebook: ttk.Notebook) -> ttk.Frame:
        """Build the calculator UI and return the top-level frame."""

        self.outer_frame = ttk.Frame(parent_notebook)

        # --- Top Section: Result + Input ---
        top_frame = ttk.Frame(self.outer_frame)
        top_frame.pack(fill="x", padx=10, pady=(8, 4))

        self.result_entry = ttk.Entry(
            top_frame, textvariable=self.result_var, state="readonly", justify="right"
        )
        self.result_entry.pack(fill="x")
        ToolTip(self.result_entry, "Calculation result (read-only)")

        self.input_entry = ttk.Entry(top_frame)
        self.input_entry.pack(fill="x", pady=(4, 0))
        ToolTip(self.input_entry, "Enter expression (e.g., 3 + 4 * 2)")
        self.input_entry.bind("<Return>", lambda e: self._calculate())
        self.input_entry.bind("<KP_Enter>", lambda e: self._calculate())
        self.input_entry.bind("<Button-1>", lambda e: self.input_entry.focus_set())

        # --- Middle: Button Grid ---
        btn_frame = ttk.Frame(self.outer_frame)
        btn_frame.pack(padx=10, pady=4)

        buttons = [
            ("7", 0, 0), ("8", 0, 1), ("9", 0, 2), ("/", 0, 3),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2), ("*", 1, 3),
            ("1", 2, 0), ("2", 2, 1), ("3", 2, 2), ("-", 2, 3),
            ("0", 3, 0), (".", 3, 1), ("C", 3, 2), ("+", 3, 3),
            ("(", 4, 0), (")", 4, 1), ("=", 4, 2),
        ]

        for (text, row, col) in buttons:
            btn = ttk.Button(btn_frame, text=text, width=5)
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            if text == "C":
                btn.configure(command=self._clear)
                tip = "Clear input"
            elif text == "=":
                btn.configure(command=self._calculate)
                tip = "Calculate"
            else:
                btn.configure(command=lambda t=text: self._insert(t))
                tip = f"Insert '{text}'"
            ToolTip(btn, tip)

        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

        # --- Bottom: History ---
        history_frame = ttk.LabelFrame(self.outer_frame, text="History")
        history_frame.pack(fill="both", expand=False, padx=10, pady=(0, 8))

        scrollbar = ttk.Scrollbar(history_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.history_list = Listbox(history_frame, height=6, yscrollcommand=scrollbar.set)
        self.history_list.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.history_list.yview)

        return self.outer_frame

    # ------------------------------------------------------------------
    def _insert(self, text: str) -> None:
        if self.input_entry is not None:
            self.input_entry.insert(tk.END, text)

    def _clear(self) -> None:
        if self.input_entry is not None:
            self.input_entry.delete(0, tk.END)
        self.result_var.set("")

    def _calculate(self) -> None:
        if self.input_entry is None:
            return
        expr = self.input_entry.get().strip()
        if not expr:
            return
        try:
            result = self.evaluator.eval(expr)
            self.result_var.set(str(result))
            if self.history_list is not None:
                self.history_list.insert(tk.END, f"{expr} = {result}")
                if self.history_list.size() > CONFIG["calc"]["max_history"]:
                    self.history_list.delete(0)
                self.history_list.yview_moveto(1.0)
        except Exception:
            self.result_var.set("Error")

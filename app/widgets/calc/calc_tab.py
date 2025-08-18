import tkinter as tk
from tkinter import ttk, Listbox
from utils.safe_eval import SafeEvaluator
from utils.tooltip import ToolTip
from core.config import CONFIG

def create_calc_tab(app):
    calc_tab = ttk.Frame(app.notebook)
    app.notebook.add(calc_tab, text="Calc")

    # --- Evaluator ---
    evaluator = SafeEvaluator()

    # --- Top Section: Result + Input ---
    top_frame = ttk.Frame(calc_tab)
    top_frame.pack(fill='x', padx=10, pady=(8, 4))

    app.result_var = tk.StringVar(value="")
    app.calc_result_entry = ttk.Entry(top_frame, textvariable=app.result_var, state='readonly', justify='right')
    app.calc_result_entry.pack(fill='x')
    ToolTip(app.calc_result_entry, "Calculation result (read-only)")

    app.calc_input = ttk.Entry(top_frame)
    app.calc_input.pack(fill='x', pady=(4, 0))
    ToolTip(app.calc_input, "Enter expression (e.g., 3 + 4 * 2)")
    app.calc_input.bind('<Return>', lambda e: _calculate())
    app.calc_input.bind('<KP_Enter>', lambda e: _calculate())
    app.calc_input.bind('<Button-1>', lambda e: app.calc_input.focus_set())

    # --- Middle: Button Grid ---
    btn_frame = ttk.Frame(calc_tab)
    btn_frame.pack(padx=10, pady=4)

    buttons = [
        ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
        ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
        ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
        ('0', 3, 0), ('.', 3, 1), ('C', 3, 2), ('+', 3, 3),
        ('(', 4, 0), (')', 4, 1), ('=', 4, 2),
    ]

    def _insert(t):
        app.calc_input.insert(tk.END, t)

    def _clear():
        app.calc_input.delete(0, tk.END)
        app.result_var.set("")

    def _calculate():
        expr = app.calc_input.get().strip()
        if not expr:
            return
        try:
            result = evaluator.eval(expr)
            app.result_var.set(str(result))
            app.calc_history.insert(tk.END, f"{expr} = {result}")
            if app.calc_history.size() > CONFIG['calc']['max_history']:
                app.calc_history.delete(0)
            app.calc_history.yview_moveto(1.0)
        except Exception:
            app.result_var.set("Error")

    for (text, row, col) in buttons:
        btn = ttk.Button(btn_frame, text=text, width=5)
        btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
        if text == 'C':
            btn.configure(command=_clear)
            tip = "Clear input"
        elif text == '=':
            btn.configure(command=_calculate)
            tip = "Calculate"
        else:
            btn.configure(command=lambda t=text: _insert(t))
            tip = f"Insert '{text}'"
        ToolTip(btn, tip)

    for i in range(4):
        btn_frame.columnconfigure(i, weight=1)
    for i in range(5):
        btn_frame.rowconfigure(i, weight=1)

    # --- Bottom: History ---
    history_frame = ttk.LabelFrame(calc_tab, text="History")
    history_frame.pack(fill='both', expand=False, padx=10, pady=(0, 8))

    scrollbar = ttk.Scrollbar(history_frame, orient='vertical')
    scrollbar.pack(side='right', fill='y')

    app.calc_history = Listbox(history_frame, height=6, yscrollcommand=scrollbar.set)
    app.calc_history.pack(side='left', fill='both', expand=True)
    scrollbar.config(command=app.calc_history.yview)

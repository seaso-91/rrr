import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES

class SimulationView(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.selected_exe = ttk.Combobox(self, values=["Option 1", "Option 2", "Option 3"])
        self.selected_exe.pack(side="top", padx=10, pady=10, fill="x", expand=False)


    @property
    def options(self):
        return self.selected_exe['values']

    @options.setter
    def options(self, value):
        self.selected_exe.config(values=value)

    def bind_select_exe(self, callback):
        self.selected_exe.bind("<<ComboboxSelected>>", callback)
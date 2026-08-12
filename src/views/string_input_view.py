import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import DND_FILES

class Information(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = tk.Label(self, text="Current Code: None")
        self.label.pack(side="top", fill="x")

        self.description_label = tk.Label(self, text="Description: None")
        self.description_label.pack(side="top", fill="x")

        self._input = None

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        print(f"Setting input: {value.code}")
        self._input = value
        if value is not None:
            self.label.config(text=f"Current Code: {value.code}")
            self.description_label.config(text=f"Description: {value.description}")
        else:
            self.label.config(text="Current Code: None")
            self.description_label.config(text="Description: None")
        
class TextArea(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._inserting = False
        self.suppress_modified = False
        self._updating = False

        self._modified_callback = None
        self._on_click_callback = None
        self._key_left_callback = None
        self._key_right_callback = None
        self._key_up_callback = None
        self._key_down_callback = None
        self._key_tab_callback = None
        self._start_move_cursor_callback = None
        self._move_cursor_callback = None

        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(
            self,
            wrap="none",
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            padx=10,
            pady=10,
        )
    
        scrollbar.config(command=self.text.yview)
        self.text.bind("<ButtonRelease-1>", self.on_click)
        self.text.bind("<<Modified>>", self.on_text_change)
        self.text.bind("<FocusIn>", self.start_update)
        self.text.bind("<FocusOut>", self.end_update)
        self.text.bind("<<Paste>>", self.on_paste)
        
        self.text.drop_target_register(DND_FILES)

        self.text.pack(side="bottom", fill="both", expand=True)


    def bind_modified(self, callback):
        self._modified_callback = callback

    def bind_drop(self, callback):
        self.text.dnd_bind("<<Drop>>", callback)

    def bind_on_click(self, callback):
        self._on_click_callback = callback

    def bind_key_left(self, callback):
        self._key_left_callback = callback

    def bind_key_right(self, callback):
        self._key_right_callback = callback

    def bind_key_tab(self, callback):
        self._key_tab_callback = callback

    def bind_start_move_cursor(self, callback):
        self._start_move_cursor_callback = callback

    def bind_move_cursor(self, callback):
        self._move_cursor_callback = callback

    def on_click(self, event=None):
        self.start_update(event)
        self.text.focus_set()
        if self._on_click_callback:
            self._on_click_callback(event)

    def start_update(self, event=None):
        if self._updating:
            return

        self._updating = True
        self.text.bind("<KeyRelease-Up>", self._move_cursor_callback)

        self.text.bind("<KeyRelease-Down>", self._move_cursor_callback)

        self.text.bind("<KeyPress-Left>", self._start_move_cursor_callback)
        self.text.bind("<KeyRelease-Left>", self._key_left_callback)

        self.text.bind("<KeyPress-Right>", self._start_move_cursor_callback)
        self.text.bind("<KeyRelease-Right>", self._key_right_callback)

        self.text.bind("<KeyPress-Tab>", self.do_nothing)
        self.text.bind("<KeyRelease-Tab>", self._key_tab_callback)

        self.text.bind("<<Paste>>", self.on_paste)

    def do_nothing(self, event=None):
        if self._inserting:
            return "break"

        if self._updating:
            #remove focus from the text to trigger the end_update method
            self.text.focus_set()
            return "break"

    def on_paste(self, event=None):
        self.start_update(event)
        self.text.after(1, self.end_update)
    
    def end_update(self, event=None):
        if not self._updating:
            return

        self.text.unbind("<KeyRelease-Up>")
        self.text.unbind("<KeyRelease-Down>")
        self.text.unbind("<KeyPress-Left>")
        self.text.unbind("<KeyRelease-Left>")
        self.text.unbind("<KeyPress-Right>")
        self.text.unbind("<KeyRelease-Right>")
        self.text.unbind("<KeyPress-Tab>")
        self.text.unbind("<KeyRelease-Tab>")
        self.text.unbind("<<Paste>>")

        self.on_text_change(force = True)
        self._updating = False

    def on_text_change(self, event=None, force=False):
        if self.suppress_modified:
            self.text.edit_modified(False)
            return
        
        if not force and not self.text.edit_modified():
            return
        
        self.text.edit_modified(False)

        if self._modified_callback:
            self._modified_callback()

    def get_text(self):
        return self.text.get("1.0", tk.END)

    def set_text(self, value):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", value)

    @property
    def cursor_position(self) -> int:
        try:
            return int(self.text.count("1.0", "insert", "chars")[0])
        except Exception:
            return 0

    def select(self, start: int, end: int):
        start_idx = f"1.0 + {start} chars"
        end_idx = f"1.0 + {end} chars"

        self.text.tag_remove("sel", "1.0", tk.END)
        self.text.tag_add("sel", start_idx, end_idx)

        self.text.mark_set("insert", start_idx)
        self.text.see(start_idx)


class Commands(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toggle_button = tk.Button(self, text="Toggle Inserting Mode", command=self._toggle_inserting)
        self.toggle_button.pack(side="left", fill="x", expand=True)

        self.write_button = tk.Button(self, text="Write")
        self.write_button.pack(side="left", fill="x", expand=True)

        self.set_file_button = tk.Button(self, text="Set Name")
        self.set_file_button.pack(side="left", fill="x", expand=True)

        self.export_button = tk.Button(self, text="Export")
        self.export_button.pack(side="left", fill="x", expand=True)

        self.inserting = True
        self.toggle_inserting_callback = None
        self._toggle_inserting(None)
        

    def bind_export(self, callback):
        self.export_button.config(command=callback)

    def bind_write(self, callback):
        self.write_button.config(command=callback)

    def bind_set_file_name(self, callback):
        self.set_file_button.config(command=callback)

    def bind_toggle_inserting(self, callback):
        self.toggle_inserting_callback = callback

    def _toggle_inserting(self, event = None):
        self.inserting = not self.inserting

        if self.inserting:
            self.toggle_button.config(text="Inserting Mode: ON")
        else:
            self.toggle_button.config(text="Inserting Mode: OFF")

        if self.toggle_inserting_callback:
            self.toggle_inserting_callback(event, self.inserting)


class ErrorLabel(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(text="", foreground="red")

    @property
    def message(self):
        return self.cget("text")
    
    @message.setter
    def message(self, message: str):
        self.config(text=message)

    def clear(self):
        self.config(text="")

class Widget(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.information = Information(self)
        self.information.pack(side="top", fill="x")
        self.text_area = TextArea(self)
        self.text_area.pack(side="top", fill="both", expand=True)
        self.error_label = ErrorLabel(self)
        self.error_label.pack(side="bottom", fill="x")
        self.commands = Commands(self)
        self.commands.pack(side="bottom", fill="x")
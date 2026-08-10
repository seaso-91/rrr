
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from pathlib import Path
from RRData import InputData
from tkinterdnd2 import DND_FILES, TkinterDnD

class Information(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.label = tk.Label(self, text="Current Code: None")
        self.label.pack(side="top", fill="x")

        self.description_label = tk.Label(self, text="Description: None")
        self.description_label.pack(side="top", fill="x")

class TextArea(ttk.Frame):
    def __init__(self, input_data: InputData, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._inserting = False
        self._current_code = None
        self._updating = False

        # Create the scrollbar
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.text_widget = tk.Text(
            self,
            wrap="none",
            yscrollcommand=scrollbar.set,
            font=("Arial", 10),
            padx=10,
            pady=10,
        )
        self.text_widget.pack(side="bottom", fill="both", expand=True)

        scrollbar.config(command=self.text_widget.yview)

        self.input_data = input_data
        self.text = str(self.input_data)
        
        self.text_widget.bind("<<Modified>>", self.on_text_change)
        self.text_widget.bind("<FocusIn>", self.start_update)
        self.text_widget.bind("<FocusOut>", self.end_update)
        self.text_widget.bind("<ButtonRelease-1>", self.on_click)

        self.text_widget.drop_target_register(DND_FILES)
        self.text_widget.dnd_bind("<<Drop>>", self.handle_drop)

        self.suppress_modified = False

    def on_click(self, event=None):
        self.start_update(event)
        self.set_current_code()
        if self._inserting and self._current_code is not None:
            self.select_code(self._current_code)

    def start_update(self, event=None):
        if self._updating:
            return
        
        self.text_widget.bind("<KeyRelease-Up>", self.move_cursor)
        self.text_widget.bind("<KeyRelease-Down>", self.move_cursor)
        self.text_widget.bind("<KeyRelease-Left>", self.move_cursor)
        self.text_widget.bind("<KeyRelease-Right>", self.move_cursor_right)
        self.text_widget.bind("<KeyPress-Tab>", self.do_nothing)
        self.text_widget.bind("<KeyRelease-Tab>", self.move_cursor_right)
        self.text_widget.bind("<KeyPress-Return>", self.do_nothing)
        self.text_widget.bind("<KeyRelease-Return>", self.move_cursor_right)

        self._updating = True

    def do_nothing(self, event=None):
        if self._inserting:
            return "break"

        if self._updating:
            #remove focus from the text_widget to trigger the end_update method
            self.text_widget.focus_set()        

    def end_update(self, event=None):
        if not self._updating:
            return
        
        self.text_widget.unbind("<KeyRelease-Up>")
        self.text_widget.unbind("<KeyRelease-Down>")
        self.text_widget.unbind("<KeyRelease-Left>")
        self.text_widget.unbind("<KeyRelease-Right>")
        self.text_widget.unbind("<KeyPress-Tab>")
        self.text_widget.unbind("<KeyRelease-Tab>")
        self.text_widget.unbind("<KeyPress-Return>")
        self.text_widget.unbind("<KeyRelease-Return>")

        self.on_text_change(force=True)
        self._updating = False

    def on_text_change(self, event=None, force=False):
        if self.suppress_modified:
            self.text_widget.edit_modified(False)
            return

        if not force and not self.text_widget.edit_modified():
            return

        self.text_widget.edit_modified(False)

        self._flush()

    def move_cursor(self, event):
        self.set_current_code()
        if self._inserting and self._current_code is not None:
            self.select_code(self._current_code)

    def move_cursor_right(self, event):
        if self._inserting:
            this_code = False
            next_code = None
            for row in self.input_data.parent.input_sequence:
                for input in row:
                    if input.code == self._current_code:
                        this_code = True
                    elif this_code:
                        next_code = input.code
                        break
                if next_code is not None:
                    break
            new_cursor_position = self.input_data.get_position(next_code) if next_code is not None else self._get_cursor_position()
            self.text_widget.mark_set("insert", f"{new_cursor_position[0] + 1}.{new_cursor_position[1]}")
        self.set_current_code()
        if self._inserting and self._current_code is not None:
            self.select_code(self._current_code)

    def set_current_code(self):
        try:
            current_position = self._get_cursor_position()
            self._current_code = self.input_data.get_code_from_position(position = current_position)
        except Exception as e:
            self._current_code = None
        self.master.information.label.config(text=f"Current Code: {self._current_code if self._current_code is not None else 'None'}")
        self.master.information.description_label.config(text=f"{self.input_data.parent.inputs[self._current_code].description if self._current_code in self.input_data.parent.inputs else 'None'}")

    def _get_cursor_position(self) -> tuple[int, int]:
        line, column = map(int, self.text_widget.index("insert").split("."))
        return line-1, column

    def select_code(self, code: str):
        try:
            row, start, end = self.input_data.get_position(code)
            self.text_widget.tag_remove("sel", "1.0", tk.END)
            self.text_widget.tag_add("sel", f"{row + 1}.{start}", f"{row + 1}.{end}")
            self.text_widget.mark_set("insert", f"{row + 1}.{start}")
            self.text_widget.see(f"{row + 1}.{start}")
        except Exception as e:
            print(f"Error selecting code '{code}': {e}")

    def get_new_input_string(self) -> str:
        """
        Returns the new input string from the variable that is currently being edited.
        """
        current_code = self._current_code
        if current_code is None:
            raise ValueError("Cannot get new input string: no code is selected.")
        row, col = self.input_data.get_row_and_column(current_code)
        line = self.text_widget.get(f"{row + 1}.0", f"{row + 1}.end")

        #iterate through the line, counting commas until the num_commas==col
        #skick commas that are inside of brackets
        if col == 0:
            start_index = -1
        else:
            start_index = self._find_comma_position(line, col)

        # search in reverse to find the end index of the current code
        # do this in case there is a broken input string
        num_cols = len(self.input_data.parent.input_sequence[row])

        end_index = self._find_comma_position(line[::-1], num_cols - col) +1
        end_index = len(line) - end_index

        return line[start_index+1:end_index].strip()
    
    def _find_comma_position(self, line: str, col: int) -> int:
        num_commas = 0
        inside_brackets = 0
        for i, char in enumerate(line):
            if char == "{":
                inside_brackets += 1
            elif char == "}":
                inside_brackets -= 1
            elif char == "," and inside_brackets == 0:
                num_commas += 1
            if num_commas == col:
                return i
        return -1  # Return -1 if the column was not found

    def _flush(self):
        cursor_position = self._get_cursor_position()
        try:
            if self._current_code is None:
                return
            self.input_data.set_values_by_string(string=self.get_new_input_string(), code = self._current_code)
            self._set_text_without_trigger(self.input_data)
            self.text_widget.config(fg="black")
        except Exception as e:
            self.text_widget.config(fg="red")
        finally:
            self.text_widget.mark_set("insert", f"{cursor_position[0] + 1}.{cursor_position[1]}")

    def _set_text_without_trigger(self, text: str):
        self.suppress_modified = True
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", text if text is not None else "")
        self.text_widget.edit_modified(False)
        self.suppress_modified = False

    def handle_drop(self, event):
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        file=Path(file_path)
        if file.is_file():
            try:
                self.end_update()
                self.input_data.set_data(data = file)
                self.master.refresh()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load data from {file_path}: {e}")


class Commands(ttk.Frame):
    def __init__(self, text_frame: TextArea, input_data: InputData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_frame = text_frame
        self.input_data = input_data

        self.toggle_button = tk.Button(self, text="Toggle Inserting Mode", command=self.toggle_inserting_mode)
        self.toggle_button.pack(side="left", fill="x", expand=True)

        self.write_button = tk.Button(self, text="Write Input File", command=self.input_data.write_input_file)
        self.write_button.pack(side="left", fill="x", expand=True)

        self.set_file_button = tk.Button(self, text="Set Input File Name", command=self.set_input_file_name)
        self.set_file_button.pack(side="left", fill="x", expand=True)

        self.export_button = tk.Button(self, text="Export Input File")
        self.export_button.pack(side="left", fill="x", expand=True)

    def set_input_file_name(self):
        current_name = self.input_data.input_file

        new_name = tk.filedialog.asksaveasfilename(
            initialfile=Path(current_name).name if current_name else "",
            defaultextension=".dat",
            filetypes=[
                ("DAT files", "*.dat"),
                ("All files", "*.*")    
            ]
        )
        try:
            if new_name:
                self.input_data.set_input_file_name(Path(new_name).name)
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input File Name", str(e))

    def toggle_inserting_mode(self):
        self.text_frame._inserting = not self.text_frame._inserting
        if self.text_frame._inserting:
            self.toggle_button.config(text="Inserting Mode: ON")
            if self.text_frame._current_code is not None:
                self.text_frame.select_code(self.text_frame._current_code)
        else:
            self.toggle_button.config(text="Inserting Mode: OFF")
            self.text_frame.text_widget.tag_remove("sel", "1.0", tk.END)

class Widget(ttk.Frame):
    def __init__(self, input_data: InputData, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_data = input_data
        self.information = Information(self)
        self.text = TextArea(master=self, input_data=self.input_data)
        self.commands = Commands(master=self, text_frame=self.text, input_data=self.input_data)

        self.information.pack(side="top", fill="x")
        self.text.pack(side="top", fill="both", expand=True)
        self.commands.pack(side="bottom", fill="x")

        # add a margin to the frame
        self.pack(padx=10, pady=10)

        self.text._set_text_without_trigger(str(self.input_data))

    def set(self, text: str):
        self.text._set_text_without_trigger(text)

    def get(self) -> str:
        return self.text.text_widget.get("1.0", tk.END)

    def refresh(self):
        self.text._set_text_without_trigger(str(self.input_data))
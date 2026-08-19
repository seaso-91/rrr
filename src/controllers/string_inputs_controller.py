from src.models.string_input import StringInput as StringInput
from src.views.string_input_view import Widget as StringInputView
from src.controllers.controller import BaseController
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

class StringInputsController(BaseController):
    def __init__(self, model: StringInput, view: StringInputView):
        super().__init__()
        self.model = model
        self.view = view
        self.view.commands.bind_export(self.handle_export)
        self.view.commands.bind_write(self.handle_write)
        self.view.commands.bind_set_file_name(self.handle_set_file_name)
        self.view.commands.bind_toggle_inserting(self.handle_toggle_inserting)

        self.view.text_area.bind_drop(self.handle_drop)
        self.view.text_area.bind_modified(self.handle_modified)
        self.view.text_area.bind_on_click(self.handle_click)
        self.view.text_area.bind_key_left(self.handle_key_left)
        self.view.text_area.bind_key_right(self.handle_key_right)
        self.view.text_area.bind_key_tab(self.handle_key_tab)
        self.view.text_area.bind_start_move_cursor(self.handle_start_move_cursor)
        self.view.text_area.bind_move_cursor(self.handle_move_cursor)

        self._inserting = False

    def handle_modified(self, event= None, force=False):
        self.view.text_area.text.tag_remove("red", "1.0", tk.END)
        self.view.text_area.text.tag_remove("black", "1.0", tk.END)
        print("flushing to model")
        self.model.text = self.view.text_area.text.get("1.0", tk.END)
        try:
            self.model.validate()
            self.model.set_values()
            self.view.error_label.clear()
        except Exception as e:
            self.show_error(e.message, e.position)

    def show_error(self, message: str, position: int):
        self.view.error_label.message = message
        self.view.text_area.text.tag_add("black", "1.0", f"1.0 + {position-1} chars")
        self.view.text_area.text.tag_add("red", f"1.0 + {position-1} chars", tk.END)
        self.view.text_area.text.tag_configure("red", foreground="red")
        self.view.text_area.text.tag_configure("black", foreground="black")
        #self.view.text_area.text.mark_set("insert", f"1.0 + {position} chars")

    def update_input_label(self):
        self.view.information.input = self.model.get_input()

    def handle_key_left(self, event):
        print("key left")
        self.set_cursor_position()
        if self._inserting:
            if self._current_input_index == self.model.input.index:
                start, end = self.model.input.prev()
            else:
                start, end = self.model.input.current()
            self.view.text_area.select(start, end)
        self.update_input_label()

    def handle_key_right(self, event):
        print("key right")
        self.set_cursor_position()
        if self._inserting:
            if self._current_input_index == self.model.input.index:
                start, end = self.model.input.next()
            else:
                start, end = self.model.input.current()
            self.view.text_area.select(start, end)
            self.set_cursor_position()
        self.update_input_label()

    def handle_key_tab(self, event):
        print("key tab")
        self.set_cursor_position()
        start, end = self.model.input.next()
        if self._inserting:
            self.view.text_area.select(start, end)
        else:
            self.view.text_area.text.mark_set("insert", f"1.0 + {start} chars")
        self.update_input_label()
        return "break"

    def handle_start_move_cursor(self, event):
        print("start move cursor")
        self.set_cursor_position()
        self._current_input_index = self.model.input.index
    
    def handle_move_cursor(self, event):
        print("move cursor")
        self.set_cursor_position()
        self.update_input_label()
        if self._inserting:
            start, end = self.model.input.current()
            self.view.text_area.select(start, end)

    def handle_drop(self, event):
        print("drop")
        file_path = event.data
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        file=Path(file_path)
        if file.is_file():
            try:
                self.view.text_area.set_text(file.read_text())
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to load data from {file_path}: {e}")

    def set_cursor_position(self):
        print(f"{self.view.text_area.cursor_position=}")
        self.model.cursor_position = self.view.text_area.cursor_position

    def handle_click(self, event):
        print("click")
        self.set_cursor_position()
        self.update_input_label()
        if self._inserting:
            start, end = self.model.input.current()
            self.view.text_area.select(start, end)

    def handle_toggle_inserting(self, event, inserting: bool):
        print("toggle inserting")
        self._inserting = inserting
        if self._inserting:
            start, end = self.model.input.current()
            self.view.text_area.select(start, end)

    def handle_write(self, event = None):
        self.model._data.flush()
        self.model._data.parent.write()
        # if self.model._data.parent.write():
        #     tk.messagebox.showinfo("Success", "Input file written successfully.")
        # else:
        #     tk.messagebox.showerror("Error", "Failed to write input file.")

    def handle_export(self, event):
        ...
    
    def handle_set_file_name(self):
        print("set file name")
        current_name = self.model._executable.path / self.model._executable.input_file.name
        print(f"Current input file name: {current_name}")
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
                self.model._executable.input_file.name = Path(new_name).name
                self.model._executable.path = Path(new_name).parent
                print(f"New input file name set to: {self.model._executable.input_file}")
                print(f"New input file path set to: {self.model._executable.path}")
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input File Name", str(e))


    def handle_request(self, request):
        """
        Handles the request to validate and set values for the input text.
        Args:
            request (dict): The request containing the input text.

        Returns:
            dict: The JSON response.
        """
        # Implement the request handling logic here
        response_data = {"message": "Request handled successfully"}
        return self.send_json_response(response_data)
    
if __name__ == "__main__":
    from src.models.aevap import AEVAP
    from src.models.acond import ACOND
    from src.models.asys import ASYS_DX, ASYS_HP
    from src.views.string_input_view import Widget as StringInputView
    from src.controllers.data_controller import DataController

    from tkinterdnd2 import TkinterDnD
    root = TkinterDnD.Tk()

    aevap = AEVAP()
    acond = ACOND()
    asys_dx = ASYS_DX()
    asys_hp = ASYS_HP()

    data_controller = DataController(asys_dx)

    from src.models.string_input import StringInput
    model = StringInput(data_controller)
    view = StringInputView(root)
    view.pack(fill=tk.BOTH, expand=True)

    controller = StringInputsController(model, view)
    
    root.mainloop()
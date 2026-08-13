from tkinter import ttk
from tkinterdnd2 import DND_FILES
import tkinter as tk

            

class ComboBox(ttk.Frame):
    def __init__(self, master, label, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label = ttk.Label(self, text=label, takefocus=False, font=("Default", 8))
        self.label.pack(side="top", fill="none", anchor="w")
        self.combobox = ttk.Combobox(self, takefocus=False)
        self.combobox.pack(side="top", fill="x")
    
    def bind_combobox_selected(self, callback):
        self.combobox.bind("<<ComboboxSelected>>", callback)

    @property
    def value(self):
        # get the current value of the combobox
        return self.combobox.get()

    @value.setter
    def value(self, value):
        # set the current value of the combobox
        self.combobox.set(value)

    @property
    def options(self):
        # get the available options for the combobox
        return self.combobox["values"]

    @options.setter
    def options(self, value):
        # set the available options for the combobox
        self.combobox["values"] = value

class InputEntry(ttk.Frame):
    def __init__(self, master, label, *args, **kwargs):
        super().__init__(master, padding=4, takefocus=False, *args, **kwargs)
        self.label = ttk.Label(self, takefocus=False, text=label)
        self.label.pack(side="top", fill="x", anchor ="w")
        self.entry = ttk.Entry(self, takefocus=True)
        self.entry.pack(side="top", fill="x")

    def bind_modified_callback(self, callback):
        self.bind("<<Modified>>", callback)

class ErrorLabel(ttk.Label):
    def __init__(self, *args, **kwargs):
        super().__init__(wraplength=240, justify="left", *args, **kwargs)
        self.config(text="", foreground="red")

    @property
    def message(self):
        return self.cget("text")
    
    @message.setter
    def message(self, message: str):
        self.config(text=message)
        self.grid()

    def clear(self):
        self.config(text="")
        self.grid_remove()

class InputWidget(ttk.LabelFrame):
    def __init__(self, master, text="Input", *args, **kwargs):
        super().__init__(master, text=text, takefocus=False, padding=8, *args, **kwargs)

        self.root_view = None  # This will be set when the group is added to the InputView
        
        self.columnconfigure(0, weight=2, minsize=20)
        self.columnconfigure(1, weight=30)
        self.columnconfigure(2, weight=0)

        style = ttk.Style()
        style.configure("TLabel", font=("Default", 8))

        self.multi_type = ComboBox(self, label="Multi Type")
        self.multi_type.combobox.configure(width=10)

        self.group = ComboBox(self, label="Group")
        self.group.combobox.configure(width=10)
        
        self.entry = InputEntry(self, label="Entry")
        desc_text = "Description: A very long test description that should wrap. "
        desc_text += "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        self.description = ttk.Label(
            self,
            text=desc_text,
            wraplength=240,
            justify="left",
            anchor="w",
        )
        self.error_label = ErrorLabel(self)
        self.error_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=4, pady=(0, 4))
        self.error_label.clear()

        self.entry.grid(row=0, column=0, columnspan= 2, rowspan=1, sticky=tk.NSEW, padx=(4, 4))
        self.description.grid(row=1, column=0, columnspan=2, padx=4, pady=(0,3), sticky=tk.W)
        self.multi_type.grid(row=0, column=2, sticky=tk.EW, padx=4, pady=(0, 0))
        self.group.grid(row=1, column=2, sticky=tk.EW, padx=4, pady=(0, 0))

        self.entry.bind("<FocusIn>", self.ensure_visible)

    def bind_modified_callback(self, callback):
        self.entry.entry.bind("<KeyRelease>", callback)

    def bind_multi_type_callback(self, callback):
        self.multi_type.bind_combobox_selected(callback)

    def bind_group_change(self, callback):
        self.group.bind_combobox_selected(callback)

    def ensure_visible(self, event=None):
        if self.root_view is not None:
            self.root_view.ensure_visible(event)

class GroupFrame(ttk.Frame):
    def __init__(self, master, group, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.group = group
        self.root_view = None  # This will be set when the group is added to the InputView
        self.columnconfigure(0, weight=0, minsize = 370)

        self.label = ttk.Button(self, text=f"Category {group}", takefocus=False, command=self.toggle_visibility)

        self.label.grid(row=0, column=0, sticky=tk.EW, padx=4, pady=(2, 4))

        self._shown = True

        self.inputs = []

    def add_input(self, input_widget: InputWidget):
        input_widget.grid(row=len(self.inputs)+1, column=0, sticky=tk.EW, padx=4, pady=4)
        self.inputs.append(input_widget)

    def toggle_visibility(self):
        self._shown = not self._shown
        self.label.configure(text=f"Category {self.group} {'' if self._shown else '(hidden)'}")
        for input_widget in self.inputs:
            if self._shown:
                input_widget.grid()
            else:
                input_widget.grid_remove()


class InputView(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.groups = dict()
        self.inputs = dict()
        
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def get_group(self, group_name: str) -> GroupFrame:
        if group_name not in self.groups:
            raise ValueError(f"Group '{group_name}' not found in InputView.")
        return self.groups[group_name]

    def add_category(self, name: str, group: GroupFrame):
        self.groups[name] = group
        group.root_view = self
        group.grid(row=len(self.groups), column=0, sticky=tk.NSEW, padx=4, pady=4)

    def add_input(self, code: str, input_widget: InputWidget, group_name: str):
        if group_name not in self.groups:
            raise ValueError(f"Group '{group_name}' not found in InputView.")
        input_widget.root_view = self
        self.inputs[code] = input_widget
        self.groups[group_name].add_input(input_widget)
        
    def _on_canvas_configure(self, event):
        # Keeps the inner frame matching the canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        # Native mouse wheel scrolling support
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ensure_visible(self, event):
        """Calculates deeply nested widget coordinates to scroll the canvas view."""
        widget = event.widget
        
        # Calculate nested top boundary relative to self.scrollable_frame
        widget_top = 0
        current = widget
        while current and current != self.scrollable_frame:
            widget_top += current.winfo_y()
            current = current.master # Walk up the window hierarchy tree
            
        widget_bottom = widget_top + widget.winfo_height()
        
        # Get visible layout windows on canvas
        canvas_top = self.canvas.canvasy(0)
        canvas_bottom = canvas_top + self.canvas.winfo_height()
        
        # Calculate full scrolling height available
        total_scroll_height = self.scrollable_frame.winfo_height()
        if total_scroll_height == 0:
            return

        # Execution logic: Adjust viewport positioning ratios
        if widget_top < canvas_top:
            # Scroll up to bring top of input into view
            self.canvas.yview_moveto(widget_top / total_scroll_height)
            
        elif widget_bottom > canvas_bottom:
            # Scroll down to bring bottom into view (centered with margin buffer)
            fraction = (widget_bottom - self.canvas.winfo_height() + 10) / total_scroll_height
            self.canvas.yview_moveto(max(0.0, fraction))

if __name__ == "__main__":
    root = tk.Tk()
    input_view = InputView(root)
    input_view.pack(side="top", fill="both", expand=True)
    input_view.add_group_frame("Group 1")
    input_view.add_group_frame("Group 2")

    input_view.add_input_widget_to_group("Group 1", "Input 1")
    input_view.add_input_widget_to_group("Group 1", "Input 2")
    input_view.add_input_widget_to_group("Group 2", "Input 3")
    input_view.add_input_widget_to_group("Group 2", "Input 4")


    root.mainloop()



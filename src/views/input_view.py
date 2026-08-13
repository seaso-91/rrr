from tkinter import ttk
from tkinterdnd2 import DND_FILES
import tkinter as tk

            

class ComboBox(ttk.Frame):
    def __init__(self, master, label, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.label = ttk.Label(self, text=label, font=("Default", 8))
        self.label.pack(side="top", fill="none", anchor="w")
        self.combobox = ttk.Combobox(self)
        self.combobox.pack(side="top", fill="x")

        self._on_change_callback = None

    def set_on_change_callback(self, callback):
        self.combobox.bind("<<ComboboxSelected>>", callback)

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
        super().__init__(master, padding=4, *args, **kwargs)
        self.label = ttk.Label(self, text=label)
        self.label.pack(side="top", fill="x", anchor ="w")
        self.entry = ttk.Entry(self)
        self.entry.pack(side="top", fill="x")

    def set_on_change_callback(self, callback):
        self.bind("<<Modified>>", callback)

class InputWidget(ttk.LabelFrame):
    def __init__(self, master, text="Input", *args, **kwargs):
        super().__init__(master, text=text, padding=8, *args, **kwargs)

        self.columnconfigure(0, weight=2, minsize=20)
        self.columnconfigure(1, weight=30)
        self.columnconfigure(2, weight=0)

        self.code = ttk.Label(self, text="Code: None")

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

        self.code.grid(row=0, column=0, rowspan=1, sticky=tk.NSEW, padx=(0, 8))
        self.entry.grid(row=0, column=1, rowspan=1, sticky=tk.NSEW, padx=(8, 8))
        self.description.grid(row=1, column=0, columnspan=2, padx=4, pady=(0,3), sticky=tk.W)
        self.multi_type.grid(row=0, column=2, sticky=tk.EW, padx=4, pady=(0, 0))
        self.group.grid(row=1, column=2, sticky=tk.EW, padx=4, pady=(0, 0))
        

class GroupFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.columnconfigure(0, weight=0, minsize = 320)

        self.label = ttk.Button(self, text="Input Category: None", command=self.toggle_visibility)

        self.label.grid(row=0, column=0, sticky=tk.EW, padx=4, pady=(2, 4))

        self.input_widgets = []

    def toggle_visibility(self):
        for widget in self.input_widgets:
            if widget.winfo_viewable():
                widget.grid_remove()
            else:
                widget.grid()

    def add_input_widget(self, input_widget):
        self.input_widgets.append(input_widget)
        input_widget.grid(row=len(self.input_widgets), column=0, columnspan=2, sticky=tk.EW, padx=4, pady=4)

    def remove_input_widget(self, input_widget):
        self.input_widgets.remove(input_widget)
        input_widget.grid_remove()

class InputView(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.group_frames = {}

    def add_group_frame(self, group_name):
        if group_name not in self.group_frames:
            group_frame = GroupFrame(self)
            group_frame.label.config(text=f"Input Category: {group_name}")
            group_frame.grid(row=len(self.group_frames), column=0, sticky=tk.NSEW, padx=4, pady=4)
            self.group_frames[group_name] = group_frame

    def remove_group_frame(self, group_name):
        if group_name in self.group_frames:
            self.group_frames[group_name].grid_remove()
            del self.group_frames[group_name]

    def add_input_widget_to_group(self, group_name, text):
        self.add_group_frame(group_name)

        group = self.group_frames[group_name]
        widget = InputWidget(group, text=text)

        group.add_input_widget(widget)
        return widget

    def remove_input_widget_from_group(self, input_widget, group_name):
        if group_name in self.group_frames:
            self.group_frames[group_name].remove_input_widget(input_widget)

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



from doctest import master
from sys import executable
import tkinter as tk
from tkinter import ttk
import src.models.rr as rr
# module for creating GUI components


class ExecutableWidget(tk.Frame):
    def __init__(self, master, executable: rr.Executable, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.dat_frame = executable.data.input.get_widget(master=self)
        self.dat_frame.pack(side="left", fill="x", pady=5, padx=5)
        self.input_frame = ScrollableFrame(self)
        self.input_frame.pack(side="right", fill="both", expand=True)
        for input in executable.inputs:
            input_widget = executable.inputs[input].Widget(master=self.input_frame.scrollable_frame)
            input_widget.bindExecutable(executable)
        self.pack(fill="both", expand=True)

            
class InputWidget(tk.Frame):
    # A basic widget containing a frame and only a text box for the input
    # also includes the input description and code
    def __init__(self, master, input: rr.Input, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.input = input
        self.frame = ttk.Frame(master, width=600, height=300, relief=tk.RIDGE, borderwidth=2)
        self.frame.pack(fill="x", pady=5, padx=5)
        self.code = ttk.Label(self.frame, text=input.code)
        self.code.pack(side="left", padx=5)
        self.description = ttk.Label(self.frame, text=input.description, width=30)
        self.description.pack(side="left", padx=5)
        self.entry = ttk.Entry(self.frame)
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<FocusOut>", self.end_update)
        self.entry.bind("<FocusIn>", self.start_update)
        self.updating = False
        self.currentvalue = self.get()

    def start_update(self, event):
        if self.updating:
            return
        self.updating = True
        self.currentvalue = self.get()

    def end_update(self, event):
        if not self.updating:
            return
        value = self.get()
        if self.input.setValue(value):
            self.updating = False
        else:
            self.updating = False
            self.set(self.currentvalue)

    def get(self):
        return self.entry.get()

    def set(self, value):
        if not self.updating:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, value)
            self.currentvalue = value
                
    def bindExecutable(self, executable: rr.Executable):
        self.executable = executable
            
    def getExecutable(self):
        if self.executable:
            return self.executable
        else:
            print("no executable found")
            return None


class InputRangeWidget(InputWidget):
    # contains an InputWidget object with additional fields below the main entry.
    # the leftmost element in the additional row is a checkbox with the label "multi value"
    # if the checkbox is unchecked. then the min and max entries are disabled.
    # if the checkbox is checked, the min and max entries are enabled.
    def __init__(self, master, input: rr.InputRange, *args, **kwargs):
        super().__init__(master, input, *args, **kwargs)
        self.min_entry = ttk.Entry(self.frame, width=10)
        self.min_entry.config(state=tk.DISABLED)
        self.multi_value_var = tk.BooleanVar()
        self.multi_value_checkbox = ttk.Checkbutton(self.frame, text="Multi Value", variable=self.multi_value_var, command=self.toggle_min_max)
        self.multi_value_checkbox.pack(side="left", padx=5)
        self.max_entry = ttk.Entry(self.frame, width=10)
        self.max_entry.pack(side="left", padx=10)
        self.min_entry.pack(side="left", padx=10)
        self.toggle_min_max()
        self.min_entry.bind("<FocusOut>", self.update_min)
        self.max_entry.bind("<FocusOut>", self.update_max)

    def update_max(self, event):
        min_value = self.get_min()
        max_value = self.get_max()
        self.input.setValues((min(min_value, max_value), max(min_value, max_value)))
                  
    def update_min(self, event):
        min_value = self.get_min()
        max_value = self.get_max()
        self.input.setValues((min(min_value, max_value), max(min_value, max_value)))

            
    def toggle_min_max(self):
        if self.multi_value_var.get():
            self.min_entry.config(state=tk.NORMAL)
            self.max_entry.config(state=tk.NORMAL)
        else:
            self.min_entry.config(state=tk.DISABLED)
            self.max_entry.config(state=tk.DISABLED)

    def get_min(self):
        return self.input._coerce(self.min_entry.get())

    def get_max(self):
        return self.input._coerce(self.max_entry.get())

    def set_min(self, value):
        self.min_entry.delete(0, tk.END)
        self.min_entry.insert(0, value)

    def set_max(self, value):
        self.max_entry.delete(0, tk.END)
        self.max_entry.insert(0, value)
        

class InputClassWidget(InputWidget):
    # contains an InputWidget object with additional fields below the main entry.
    # the leftmost element in the additional row is a checkbox with the label "multi value"
    # if the checkbox is unchecked. then multiselect is disabled
    # if the checkbox is checked, then multiselect is enabled
    def __init__(self, master, input: rr.InputClass, *args, **kwargs):
        super().__init__(master, input, *args, **kwargs)
        self.multi_value_var = tk.BooleanVar()
        self.entry.destroy()
        self.entry = ttk.Combobox(self.frame, values=input.options)
        self.entry.pack(side="left", padx=5)
        self.multi_value_checkbox = ttk.Checkbutton(self.frame, text="Multi Value", variable=self.multi_value_var, command=self.toggle_multiselect)
        self.multi_value_checkbox.pack(side="left", padx=5)
        self.multi_select_combobox = MultiSelectCombobox(self.frame, choices=input.options)
        self.multi_select_combobox.pack(side="left", padx=5)
        self.toggle_multiselect()  # Initialize the state of the multi-select combobox based on the checkbox

    def toggle_multiselect(self):
        if self.multi_value_var.get():
            self.multi_select_combobox.config(state="normal")
        else:
            self.multi_select_combobox.config(state="disabled")



class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        
        # 1. Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        # 2. Create the internal frame that will hold your actual widgets
        self.scrollable_frame = tk.Frame(self.canvas)
        
        # 3. Bind the internal frame configuration changes to update the canvas scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        # 4. Embed the internal frame inside the canvas window object
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # 5. Bind the canvas resizing to ensure the internal frame stretches to full width
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        
        # 6. Configure canvas scrolling behavior
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # 7. Pack the layout elements
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Optional: Bind mouse wheel scrolling globally over this widget
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        # Keeps the inner frame matching the canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        # Native mouse wheel scrolling support
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

class MultiSelectCombobox(ttk.Entry):
    def __init__(self, master, choices, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.choices = choices
        self.popup = None
        
        # Make the entry look like a combobox read-only field
        self.bind("<Button-1>", self.show_popup)

    def show_popup(self, event):
        if self.popup:
            return
            
        # Create a borderless pop-up window right below the entry field
        self.popup = tk.Toplevel(self)
        self.popup.wm_overrideredirect(True)
        
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.popup.wm_geometry(f"{self.winfo_width()}x120+{x}+{y}")
        
        # Create multi-select listbox
        self.listbox = tk.Listbox(self.popup, selectmode="multiple", exportselection=0)
        self.listbox.pack(fill="both", expand=True)
        
        for choice in self.choices:
            self.listbox.insert(tk.END, choice)
            
        # Bind selection change event to update the text field in real-time
        self.listbox.bind("<<ListboxSelect>>", self.update_text)
        
        # Close pop-up if user clicks anywhere else
        self.popup.bind("<FocusOut>", self.close_popup)
        self.listbox.focus_set()
        
    def update_text(self, event):
        selected_indices = self.listbox.curselection()

        # Force convert every item to a string using str()
        selected_values = [str(self.listbox.get(i)) for i in selected_indices]

        # Clear the entry and insert the safely joined string
        self.delete(0, tk.END)
        self.insert(0, ", ".join(selected_values))

    def close_popup(self, event=None):
        if self.popup:
            self.popup.destroy()
            self.popup = None

# class InputFileWidget(ttk.Frame):
#     def __init__(self, master, input_file: RR.InputFile, *args, **kwargs):
#         super().__init__(master, *args, **kwargs)

#         self.input_file = input_file
#         self.save_job = None
#         self.updating = False
#         self.suppress_modified = False

#         # Create the scrollbar
#         scrollbar = tk.Scrollbar(self)
#         scrollbar.pack(side="right", fill="y")        

#         self.text_widget = tk.Text(
#             self,
#             wrap="none",
#             yscrollcommand=scrollbar.set,
#             font=("Arial", 10),
#             padx=10,
#             pady=10,
#         )
#         self.text = input_file.read()
#         self.updating = False
#         self.text_widget.bind("<<Modified>>", self.on_text_change)
#         self.text_widget.bind("<FocusIn>", self.start_update)
#         self.text_widget.bind("<FocusOut>", self.end_update)


#         self.text_widget.pack(side="left", fill="both", expand=False)
#         self._set_text_without_trigger(self.text)

#         scrollbar.config(command=self.text_widget.yview)

#     def start_update(self, event=None):
#         if self.updating:
#             return
#         self.current_value = self.get()
#         self.updating = True

#     def end_update(self, event=None):
#         if not self.updating:
#             return
#         self.on_text_change(force=True)
#         self.updating = False

#     def on_text_change(self, event=None, force=False):
#         if self.suppress_modified:
#             self.text_widget.edit_modified(False)
#             return

#         if not force and not self.text_widget.edit_modified():
#             return

#         self.text_widget.edit_modified(False)

#         if self.save_job is not None:
#             self.after_cancel(self.save_job)

#         ms_delay = 1 if force else 1000
#         self.save_job = self.after(ms_delay, self.save_file)

#     def save_file(self):
#         text = self.text_widget.get("1.0", tk.END)
#         if self.input_file.validate(data = text):
#             print(text)
#             print("Validation passed.")
#             self.text_widget.config(fg="black")
#             self.input_file.write(text, source_widget=True)
#         else:
#             #change the text to red
#             print("Validation failed.")
#             self.text_widget.config(fg="red")
#             print("Validation failed.")
#         self.save_job = None

#     def set(self, text: str):
#         if not self.updating:
#             self._set_text_without_trigger(text)
#             self.current_value = text

#     def _set_text_without_trigger(self, text: str):
#         self.suppress_modified = True
#         self.text_widget.delete("1.0", tk.END)
#         self.text_widget.insert("1.0", text if text is not None else "")
#         self.text_widget.edit_modified(False)
#         self.suppress_modified = False

#     def get(self) -> str:
#         return self.text_widget.get("1.0", tk.END)


        
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollable Frame Example")
    root.geometry("400x300")

    # Instantiate the custom scrollable frame
    frame = ScrollableFrame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Populate the frame with sample buttons to test scrolling
    for i in range(30):
        btn = ttk.Button(frame.scrollable_frame, text=f"Scrollable Button {i+1}")
        btn.pack(fill="x", padx=5, pady=5)

    root.mainloop()
from ast import In
from re import S

from tkinterdnd2 import TkinterDnD
import tkinter as tk

from src.controllers.string_inputs_controller import StringInputsController
from src.controllers.data_controller import DataController
from src.controllers.executable_controller import ExeController
from src.controllers.inputs_controller import InputsController

from src.models.aevap import AEVAP
from src.models.acond import ACOND
from src.models.asys import ASYS_DX, ASYS_HP
from src.models.data import Data
from src.models.string_input import StringInput

from src.views.simulation_view import SimulationView
from src.views.string_input_view import Widget as StringInputView
from src.views.input_view import InputView

from src.models.rr_enums import Program

class SimulationController:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        
        self.simulation_view = SimulationView(self.root)
        self.simulation_view.pack(side="top", fill="both", expand=True)
        self.simulation_view.options = [program.name for program in Program]
        self.selected_executable: Program | None = None
        self.simulation_view.bind_select_exe(self.handle_select_exe)
        self.input_view: InputView | None = None
        self.string_input_view: StringInputView | None = None

        self.simulation_view.selected_exe.current(0)
        self.handle_select_exe(None)

        self.root.mainloop()

    def handle_select_exe(self, event):
        executable_name = self.simulation_view.selected_exe.get()
        self.selected_executable = Program[executable_name].cls()

        if self.input_view:
            self.input_view.pack_forget()
        if self.string_input_view:
            self.string_input_view.pack_forget()

        if self.selected_executable is None:
            return
        
        self.data_controller = DataController(self.selected_executable)
        self.executable_controller = ExeController(self.selected_executable)

        inputs = []
        for i, row in enumerate(self.selected_executable.input_sequence):
            for col, input in enumerate(row):
                input._category = f"Row {i+1}"
                inputs.append(input)

        self.string_input = StringInput(self.data_controller)
        self.string_input_view = StringInputView(master=self.simulation_view)
        self.string_inputs_controller = StringInputsController(self.string_input, self.string_input_view)
        self.string_input_view.pack(side="left", fill="both", expand=True)

        self.input_view = InputView(master=self.simulation_view)
        self.inputs_controller = InputsController(inputs, self.input_view, self.data_controller)
        self.input_view.pack(side="right", fill="both", expand=False, anchor="e")



if __name__ == "__main__":
    simulation_controller = SimulationController()
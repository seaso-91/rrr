from pathlib import Path
from src.models.rr_enums import Program
import subprocess
from itertools import product
from src.models.input import Input

class Executable():
    def __init__(self, program: Program,  
                 result_mapping: dict, 
                 input_sequence: list[list[Input]],
                 required_dats: list[str] = []):
        self.program = program
        self.path = Path.cwd()
        self._initialize_inputs(input_sequence=input_sequence)
        self.input_sequence = input_sequence
        self.result_mapping = result_mapping
        self.required_dats = required_dats
        from src.models.rr_data import Data
        self.data = Data(parent=self)

    def _initialize_inputs(self, input_sequence: list[list[Input]]):
        self.inputs = {}
        for row in input_sequence:
            for input in row:
                assert input.code not in self.inputs, f"Duplicate input code found: {input.code}"
                self.inputs[input.code] = input
                input.parent = self

    def setPath(self, path: Path):
        self.path = path

    def setInput(self, key: str, value) -> bool:
        try:
            self.inputs[key].setValue(value)
            self.results.ready = False
        except Exception as e:
            print(f"Error setting input '{key}' <- {value}: {e}")
            return False
        return True
    
    def write(self):
        self.input_file.write()

    def run(self):
        try:
            result = subprocess.run([self.path / self.program.exe, self.data.input.input_file.name], capture_output=True, text=True, cwd=self.path)
            if result.stderr:
                print("AEVAP Error: ", result.stderr)
            self.data.output.load()
            number_of_results = self.data.output.number_of_results()
            if number_of_results != self.data.input.expected_number_of_results:
                self.data.input.set_start_index(self.data.input.start_index + number_of_results)
                self.data.input.write_input_file()
                self.run()

        except Exception as e:
            print(f"Error occurred while running AEVAP: {e}")

    def importData(self, path: Path = None):
        self.input_file.importData(path=path)

    def getMultiValuedInputs(self) -> list[Input]:
        multi_valued_inputs = []
        for input in self.inputs:
            if self.inputs[input].values is not None and len(self.inputs[input].values) > 0:
                multi_valued_inputs.append(input)
        return multi_valued_inputs
    
    def getInputString(self):
        inputString = ""
        for input in self.input_sequence:
            for key in input:
                if key in self.inputs:
                    inputString += f"{self.inputs[key]},"
                else:
                    raise KeyError(f"Input key '{key}' not found.")
            inputString = inputString[:-1] + "\n"  # remove last comma and add newline
        return inputString + "0"
    
    def getInputStrings(self):
        # Get all combinations of multi-valued inputs and return the corresponding input strings.
        multi_keys = self.getMultiValuedInputs()
        if not multi_keys:
            return self.getInputString()

        original_values = {key: self.inputs[key].getValue() for key in multi_keys}
        value_lists = [self.inputs[key].values for key in multi_keys]
        input_strings = []

        for combo in product(*value_lists):
            for key, value in zip(multi_keys, combo):
                self.inputs[key].setValue(value)
            input_strings.append(self.getInputString())

        for key, value in original_values.items():
            self.inputs[key].setValue(value)

        input_string = ""
        for string in input_strings:
            input_string += string + "\n"

        return input_string
    
    def Widget(self, *args, **kwargs):
        from src.views.rrx import ExecutableWidget
        self.widget = ExecutableWidget(executable=self, *args, **kwargs)
        self.widget.pack(side="left")
        return self.widget


class InputFile():
    def __init__(self, parent: Executable, name: str = "d1.dat"):
        self.name = name
        self.parent = parent
        self.reading = False
        self.widget = None
        try:
            self.read()
        except Exception as e:
            pass

    def read(self, path: Path = None):
        if path is None:
            path = self.parent.path / self.name
        try:
            with open(path, "r") as f:
                data = f.read()
            return data
        except Exception as e:
            print(f"Error occurred while importing data from {path}: {e}")

    def write(self, data: str = None, source_widget: bool = False) -> bool:
        if self.reading:
            return False
        if data is None:
            data = self.parent.getInputStrings()
            push_to_executable = False
        else:
            if not self.validate(data=data):
                raise ValueError("Invalid data format.")
            push_to_executable = True
        try:
            with open(self.parent.path / self.name, "w") as f:
                f.write(data)
                success = True
        except Exception as e:
            print(f"Error occurred while writing data to {self.parent.path / self.name}: {e}")
            success = False
        if push_to_executable:
            self.parent.importData()
        if success and self.widget is not None and not source_widget:
            self.widget.set(data)
        return success

    def setValue(self, data: str) -> bool:
        if self.write(data=data):
            return True
        return False

    def setName(self, name: str):
        self.name = name

    def Widget(self, *args, **kwargs):
        from views.rrx import InputFileWidget
        self.widget = InputFileWidget(input_file=self, *args, **kwargs)
        return self.widget
    
    def importData(self, path: Path = None):
        if path is None:
            path = self.parent.path / self.name
        self.reading = True
        imported_data = self.read(path=path)
        new_inputs = self.splitData(imported_data)
        self.setInputs(new_inputs)
        self.reading = False

    def setInputs(self, inputs: dict):
        if self.validate(inputs = inputs):
            for input in inputs:
                self.parent.setInput(input, inputs[input])

    def splitData(self, data: str):
        split_data = {}
        lines = data.strip().split("\n")
        for i, row in enumerate(self.parent.input_sequence):
            values = lines[i].strip().split(",")
            for j, input in enumerate(row):
                if values[j] == '' or values[j] == 'None':
                    values[j] = None
                split_data[input] = values[j]
        return split_data

    def validate(self, inputs: dict = None, data: str = None) -> bool:
        if data is None:
            data = self.read()
        if inputs is None:
            inputs = self.splitData(data)
        for input in inputs:
            is_valid = self.parent.inputs[input].validate(inputs[input])
            if not is_valid:
                print(f"Validation failed for input: {input} with value: {inputs[input]}")
                return False
        return True

class Result():
    def __init__(self,
                 column: int,
                 value: any):
        self.column = column
        self.value = value
    
class Results():
    def __init__(self, parent: Executable):
        self.parent = parent
        self.ready = False
        self.results = {}
    
    #the results are a csv file with the first row being the column headers and the remaining rows being the data.
    def _load(self):
        try:
            with open(self.parent.path / f"{self.parent.name}.csv", "r") as f:
                lines = f.readlines()
            headers = lines[0].strip().split(",")
            for line in lines[1:]:
                values = line.strip().split(",")
                for i, header in enumerate(headers):
                    if header in self.parent.result_mapping:
                        key = self.parent.result_mapping[header]
                        if key not in self.results:
                            self.results[key] = []
                        self.results[key].append(values[i])
            self.ready = True
        except Exception as e:
            print(f"Error loading results: {e}")

    def get(self, key: str):
        if not self.ready:
            raise Exception("Results are not ready yet.")
        if key in self.results:
            return self.results[key]
        else:
            raise KeyError(f"Result key '{key}' not found.")

if __name__ == "__main__":
    from src.models.aevap import AEVAP
    from tkinterdnd2 import TkinterDnD
    root = TkinterDnD.Tk()
    aevap = AEVAP()
    root.title("AEVAP GUI")
    widget = aevap.Widget(master=root)
    widget.pack(side="left")
    root.mainloop()
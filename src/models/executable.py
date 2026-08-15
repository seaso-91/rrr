from pathlib import Path
from src.models.rr_enums import Program
import subprocess
from itertools import product
from src.models.input import Input
from tools.decorators import timer_decorator as timer

class Executable():
    def __init__(self, program: Program,  
                 result_mapping: dict, 
                 input_sequence: list[list[Input]],
                 required_dats: list[str] = []):
        self.program = program
        self._path = Path.cwd()
        self._initialize_inputs(input_sequence=input_sequence)
        self.input_sequence = input_sequence
        self.result_mapping = result_mapping
        self.required_dats = required_dats
        self.input_file = InputFile(parent=self)
        self.output_file = OutputFile(parent=self)
        from src.models.data import InputData, OutputData
        self.input_data: InputData = InputData()
        self.output_data: OutputData = OutputData()
        self.result: subprocess.CompletedProcess = None

    def _initialize_inputs(self, input_sequence: list[list[Input]]):
        self.inputs = {}
        for row in input_sequence:
            for input in row:
                assert input.code not in self.inputs, f"Duplicate input code found: {input.code}"
                self.inputs[input.code] = input
                input.parent = self
    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, path: Path):
        self._path = path

    
    def write(self):
        self.input_file.write()

    def run(self):
        self.execute()
        self.output_data.push(self.input_data.run_data, self.output_file.load(), self.result)

    def execute(self):
        self.result = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        try:
            self.result = subprocess.run(
                [self.path / self.program.exe, self.input_file.name],
                capture_output=True,
                text=True, 
                cwd=self.path,
                check=True
                )
        except Exception as e:
            self.result.stderr = str(e)
            


    

class InputFile():
    def __init__(self, parent: Executable, name: str = "d1.dat"):
        self._name = name
        self.parent = parent

    def get_input_string(self):
        input_string = ""
        for run_id in self.parent.input_data.run_data:
            run_data = self.parent.input_data.run_data[run_id]
            for inputs in self.parent.input_sequence:
                for input in inputs:
                    if input.code in run_data:
                        input_string += f"{run_data[input.code]},"
                    else:
                        print(f"Run data for run_id {run_id} does not contain key '{input.code}'. Available keys: {list(run_data.keys())}")
                        raise KeyError(f"Input key '{input.code}' not found.")
                input_string = input_string[:-1] + "\n"  # remove last comma and add newline
            input_string += "0\n"  # add the terminating zero for each run
        return input_string[:-1]  # remove last newline

    def write(self) -> bool:
        if self.parent.input_data.number_of_runs > 0:
            input_string = self.get_input_string()
            try:
                with open(self.parent.path / self._name, "w") as f:
                    f.write(input_string)
                return True
            except Exception as e:
                print(f"Error writing input file: {e}")
                return False
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name: str):
        self._name = name

class OutputFile():
    def __init__(self, parent: Executable):
        self.parent = parent

    @property
    def name(self):
        return self.parent.path / f"{self.parent.program.name}.csv"
    
    #the results are a csv file with the first row being the column headers and the remaining rows being the data.
    def load(self):
        results = []
        try:
            with open(self.name, "r") as f:
                lines = f.readlines()
                if len(lines) < 2:
                    return results
            for line in lines[1:]:
                results.append({})
                values = line.strip().split(",")
                for key, column in self.parent.result_mapping.items():
                    results[-1][key] = values[column-1].strip()
            return results

        except Exception as e:
            print(f"Error loading output file: {e}")
            return


from src.models.data import OutputData, InputData
from src.controllers.controller import BaseController
from src.models.executable import Executable
from src.models.rr_enums import Program

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import shutil
import random


##FIXME move dats to each module
# PROGRAM_INFO = {
#     # Program.ACOND: (RR.ACOND(),[Dat.COIL, Dat.COIL1, Dat.REF]),
#     # Program.ACU: (RR.ACU(),[Dat.COIL, Dat.COIL1, Dat.COMP, Dat.COMPL, Dat.REF]),
#     Program.AEVAP: (AEVAP,[Dat.COIL, Dat.COIL1, Dat.REF]),
#     # Program.ASYS: (RR.ASYS(),[Dat.COIL, Dat.COIL1, Dat.COMP, Dat.COMPL, Dat.REF, Dat.REVALV]),

#     # Program.AWCSYS: (
#     #     RR.AWCSYS(),
#     #     [Dat.BPHE, Dat.COIL, Dat.COIL1, Dat.COMAIR, Dat.COMP, Dat.COMPL,
#     #     Dat.EDCON, Dat.EDEVA, Dat.PACKLESS, Dat.REF, Dat.REVALV, Dat.TURBO],
#     # ),
#     # Program.AWESYS: (
#     #     RR.AWESYS(),
#     #     [Dat.BPHE, Dat.COIL, Dat.COIL1, Dat.COMAIR, Dat.COMP, Dat.COMPL,
#     #     Dat.EDCON, Dat.EDEVA, Dat.PACKLESS, Dat.REF, Dat.REVALV, Dat.TURBO],
#     # ),

#     # Program.COMP: (RR.COMP(),[Dat.COMP, Dat.COMPL, Dat.REF]),

#     # Program.FAD: (RR.FAD(),[Dat.COIL, Dat.COIL1, Dat.REF]),
#     # Program.STA: (RR.STA(),[Dat.COIL, Dat.COIL1, Dat.REF]),
#     # Program.WLHPA: (RR.WLHPA(),[Dat.COIL, Dat.COIL1, Dat.REF]),

#     # Program.WCL: (
#     #     RR.WCL(),
#     #     [Dat.BPHE, Dat.COMAIR, Dat.EDCON, Dat.EDEVA,
#     #     Dat.PACKLESS, Dat.REF, Dat.TURBO]
#     # ),
#     # Program.WEL: (
#     #     RR.WEL(),
#     #     [Dat.BPHE, Dat.COMAIR, Dat.EDCON, Dat.EDEVA,
#     #     Dat.PACKLESS, Dat.REF, Dat.TURBO]
#     # ),

#     # Program.WCSYS: (
#     #     RR.WCSYS(),
#     #     [Dat.BPHE, Dat.COIL, Dat.COIL1, Dat.COMAIR, Dat.COMP, Dat.COMPL,
#     #     Dat.EDCON, Dat.EDEVA, Dat.PACKLESS, Dat.REF, Dat.REVALV, Dat.TURBO],
#     # ),
#     # Program.WCESYS: (
#     #     RR.WCESYS(),
#     #     [Dat.BPHE, Dat.COIL, Dat.COIL1, Dat.COMAIR, Dat.COMP, Dat.COMPL,
#     #     Dat.EDCON, Dat.EDEVA, Dat.PACKLESS, Dat.REF, Dat.REVALV, Dat.TURBO]
#     # ),

#     # Program.WCU: (
#     #     RR.WCU(),
#     #     [Dat.BPHE, Dat.COMAIR, Dat.COMP, Dat.COMPL,
#     #     Dat.EDCON, Dat.EDEVA, Dat.PACKLESS, Dat.REF, Dat.TURBO]
#     # ),
#     # Program.WWSYS: (
#     #     RR.WWSYS(),
#     #     [Dat.BPHE, Dat.COMAIR, Dat.COMP, Dat.COMPL,
#     #     Dat.EDCON, Dat.EDEVA, Dat.PACKLESS, Dat.REF, Dat.REVALV, Dat.TURBO]
#     # )
# }

from enum import Enum

class ExeController(BaseController):
    def __init__(self, executable: Executable, input_data: InputData, output_data: OutputData, min_workers_on_hand: int = 10):
        super().__init__()
        self.executable = executable
        self.input_data = input_data
        self.output_data = output_data
        self.min_workers_on_hand = min_workers_on_hand
        self.directory = Path.cwd()
        self.executable_list = ExecutableList(executable.program, self.directory / "programs", self.directory / "KCC")
    
    def run(self, max_workers=1):
        while self.input_data.number_of_runs > 0:
            number_of_runs = self.input_data.number_of_runs
            if number_of_runs < max_workers:
                max_workers = number_of_runs
            executables = self.executable_list.get(max_workers)
            for executable in executables:
                executable.input_data.run_data = self.input_data.get(number_of_runs=number_of_runs // len(executables) + 1)
 
            self.batch_run(executables=executables)

            for executable in executables:
                self.input_data.return_run(executable.output_data.retry)
                self.output_data.add_input_data(executable.output_data.successes)
                self.output_data.add_input_data(executable.output_data.failures)
                self.output_data.add_results(executable.output_data.results)
                
                self.executable_list.check_in(executable)
                

    def batch_run(self, executables: list[Executable]):
        with ProcessPoolExecutor(max_workers=len(executables)) as pool:
            return list(pool.map(self._run_job, executables))
        
    @staticmethod
    def _run_job(executable: Executable) -> Executable:
        executable.run()
        return executable

class ExecutableStatus(Enum):
    READY = "Ready"
    BUSY = "Busy"

class ExecutableList():
    #the list is a dictionary of lists of RR.Executable
    #the key is the name of the executable and the value is a list of that Executable
    def __init__(self, program: Program, spooled_programs_path: Path, source_programs_path: Path):
        self.program = program
        self.executables: dict[str, dict[str, object]] = {}
        self.spooled_programs_path = spooled_programs_path
        self.source_programs_path = source_programs_path

    def add(self, executable: Executable) -> None:
        if executable.program != self.program:
            raise ValueError(f"Executable {executable.program.name} does not match list program {self.program.name}.")
        #check if the executable is already in the list
        if executable.path.name in self.executables.keys():
            raise ValueError(f"Executable {executable} already exists in list.")
        else:
            self.executables[executable.path.name] = {"status": ExecutableStatus.READY, "executable": executable}

    def get(self, number_of_executables) -> list[Executable]:
        result_list = []
        while number_of_executables > self.number_of_ready_executables:
            self.spool_up()
        while number_of_executables < self.number_of_ready_executables and self.number_of_ready_executables > self.min_workers_on_hand:
            self._kill(self.pop())
        while number_of_executables > 0:
            result_list.append(self.check_out())
            number_of_executables -= 1
        return result_list

    def check_out(self) -> Executable:
        for key in self.executables.keys():
            if self.executables[key]["status"] == ExecutableStatus.READY:
                self.executables[key]["status"] = ExecutableStatus.BUSY
                return self.executables[key]["executable"]
        raise ValueError("No ready executables available.")

    def check_in(self, executables: list[Executable]|Executable) -> None:
        if isinstance(executables, list):
            executables = [executables]
        for executable in executables:
            if executable.path.name in self.executables:
                if self.executables[executable.path.name]["executable"] == executable:
                    self.executables[executable.path.name]["status"] = ExecutableStatus.READY
                else:
                    raise ValueError(f"Executable {executable} not found in list.")
            else:
                raise ValueError(f"Executable {executable} not found in list.")

    def pop(self) -> Executable:
        #pop the first item in the dictionary
        for key in self.executables.keys():
            if self.executables[key]["status"] == ExecutableStatus.READY:
                result = self.executables.pop(key)
                return result["executable"]
    
    @property
    def number_of_ready_executables(self) -> int:
        return len([exe for exe in self.executables.values() if exe["status"] == ExecutableStatus.READY])

    def _kill(self, executable: Executable) -> bool:
        #delete the directory and all its contents
        path = executable.path
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            self.removeExecutable(executable)
            return True
        return False

    def _getNewID(self) -> str:
        #create a random number and check if it exists in the directory, if it does, create a new one until it doesn't exist
        while True:
            new_id = str(random.randint(10000, 99999))
            if not (self.directory / new_id).exists():
                return new_id

    def _findExistingExecutables(self):
        #check subfolders. they must be a 5 digit number and contain a single .exe file
        for path in self.directory.iterdir():
            if path.is_dir() and path.name.isdigit() and len(path.name) == 5:
                exe_files = list(path.glob("*.exe"))
                if len(exe_files) == 1:
                    name = Path(exe_files[0]).name[:-4]
                    print(f"Found existing executable: {name} in {path}")
                    executable = self._new_executable()
                    executable.path = path
                    self.executable_list.add(executable)
                    
    def _new_executable(self) -> Executable:
        try:
            print(f"Creating new executable: {self.program.name}")
            executable_class = self.program.cls
            executable = executable_class()
            return executable
        except Exception as e:
            raise ValueError(f"Executable {self.program.name} not found: {e}")
        
    def spool_up(self):
        executable = self._new_executable()
        new_id = self._getNewID()
        new_path = self.spooled_programs_path / str(new_id)
        Path(new_path).mkdir(parents=True, exist_ok=True)

        dats_to_copy = executable.required_dats

        #copy the executable and the dat files to the specified path
        shutil.copy(self.source_programs_path / executable.program.exe, new_path)
        factory = executable.program.cls
        new_executable = factory()
        for file_name in dats_to_copy:
            shutil.copy(self.source_programs_path / file_name.dat, new_path)
        new_executable.path = new_path
        self.add(new_executable)


if __name__ == "__main__":
    from src.models.aevap import AEVAP
    from src.controllers.data_controller import DataController
    from time import time

    aevap = AEVAP()
    input_data = InputData()
    output_data = OutputData()
    manager = ExeController(executable=aevap, input_data=input_data, output_data=output_data)

    data_controller = DataController(aevap)

    data_controller.import_dat(Path("C:\\Users\\jajones\\Desktop\\rrr\\D1.DAT"))
    data_controller.set_values("TAE", list(map(str, range(80, 90, 1))), "1")

    manager.run(max_workers=2)

    print(f"Successes: {len(output_data.successes)}")
    print(f"Failures: {len(output_data.failures)}")
   
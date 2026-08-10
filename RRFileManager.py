
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import shutil
import random
import RR
from RREnums import Dat, Program
import copy
from AEVAP import AEVAP
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

class Manager():
    def __init__(self, directory: Path = Path.cwd()):
        self.executable_list = ExecutableList()
        self.directory = directory
        self._findExistingExecutables()

    def run(self, executable: RR.Executable, max_workers=None):
        while len(self.executable_list.getExecutables(executable.program)) < max_workers:
            self.spoolUp(executable)
        executables = self.executable_list.getExecutables(executable.program)
        self.split_input(from_exe=executable, to_exe=executables)
        with ProcessPoolExecutor(max_workers=max_workers) as pool:
            return list(pool.map(self._run_job, self.executable_list.getExecutables(executable.program)))
        
    def spoolUp(self, executable: RR.Executable) -> RR.Executable:
        new_id = self._getNewID()
        new_path = self.directory / str(new_id)
        Path(new_path).mkdir(parents=True, exist_ok=True)

        dats_to_copy = executable.required_dats

        #copy the executable and the dat files to the specified path
        shutil.copy(executable.program.exe, new_path)
        factory = executable.program.cls
        new_executable = factory()
        for file_name in dats_to_copy:
            shutil.copy(file_name.dat, new_path)
        new_executable.setPath(new_path)
        self.executable_list.addExecutable(new_executable)
        return new_executable

    def _kill(self, executable: RR.Executable) -> bool:
        #delete the directory and all its contents
        path = executable.path
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
            self.executable_list.removeExecutable(executable)
            return True
        return False


    @staticmethod
    def _run_job(executable: RR.Executable) -> RR.Executable:
        executable.run()
        return executable

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
                    executable = self._newExecutable(Program[name])
                    executable.setPath(path)
                    self.executable_list.addExecutable(executable)
                    
    def _newExecutable(self, program: Program) -> RR.Executable:
        try:
            print(f"Creating new executable: {program.name}")
            executable_class = program.cls
            executable = executable_class()
            return executable
        except Exception as e:
            raise ValueError(f"Executable {program.name} not found: {e}")
        
    def _readInput(self, input_file: Path) -> tuple[int, list[str]]:
        with open(input_file, "r") as f:
            lines = f.readlines()
        run_indices = [i for i, line in enumerate(lines) if line.strip() == "0"]
        return len(run_indices), lines

    def split_input(self, from_exe: RR.Executable, to_exe: list[RR.Executable]|RR.Executable) -> None:
        if not isinstance(to_exe, list):
            to_exe = [to_exe]

        number_of_splits = len(to_exe)
        for split, executable in enumerate(to_exe, start=0):
            executable.data.input.set_data(from_exe.data.input, force=True)
            executable.data.input.set_split(number_of_splits, split)
            executable.data.input.write_input_file()

    def _readInput(self, input_file: Path) -> tuple[int, list[str]]:
        with open(input_file, "r") as f:
            lines = f.readlines()
        run_indices = [i for i, line in enumerate(lines) if line.strip() == "0"]
        return len(run_indices), lines
    
class ExecutableList():
    #the list is a dictionary of lists of RR.Executable
    #the key is the name of the executable and the value is a list of that Executable
    def __init__(self):
        self.executables = {}

    def addExecutable(self, executable: RR.Executable) -> None:
        if executable.program.name not in self.executables:
            self.executables[executable.program.name] = []
        #check if the executable is already in the list
        if executable in self.executables[executable.program.name]:
            raise ValueError(f"Executable {executable} already exists in list.")
        else:
            self.executables[executable.program.name].append(executable)

    def removeExecutable(self, executable: RR.Executable) -> None:
        if executable.program.name in self.executables:
            if executable in self.executables[executable.program.name]:
                self.executables[executable.program.name].remove(executable)
                if len(self.executables[executable.program.name]) == 0:
                    del self.executables[executable.program.name]
            else:
                raise ValueError(f"Executable {executable} not found in list.")
        else:
            raise ValueError(f"Executable {executable} not found in list.")

    def getExecutables(self, program: Program) -> list[RR.Executable]:
        if program.name in self.executables:
            return self.executables[program.name]
        else:
            return []
    
    def __iter__(self):
        for name in self.executables.keys():
            for executable in self.executables[name]:
                yield executable



if __name__ == "__main__":
    from time import time
    from AEVAP import AEVAP
    from pathlib import Path

    run_information = {
        "number_of_runs": 0,
        "duration": 0,
        "number_of_workers": 0,
    }

    log = []

    manager = Manager()
    aevap = AEVAP()
    aevap.setPath(Path.cwd())
    aevap.data.input.set_input_file_name("deleteme.dat")
    aevap.data.input.import_data_from_dat("d1.dat")

    aevap.inputs["TAE"].setValue(81)
    number_of_trials = 1
    
    for max_workers in range(1,26,2):
        for max_TAE in range(82, 89, 3):
            for max_TWB in range(80, 81, 3):
                for max_CFM in range(6000, 6100, 100):
                    TAE_values = list(map(str, range(80, max_TAE, 1)))
                    TWB_values = list(map(str, range(70, max_TWB, 1)))
                    CFM_values = list(map(str, range(4000, max_CFM, 100)))
                    aevap.data.input.set_values("TAE", TAE_values, "1")
                    aevap.data.input.set_values("TWB", TWB_values, "2")
                    aevap.data.input.set_values("CFM", CFM_values, "3")
                    run_information["number_of_runs"] = aevap.data.input.number_of_runs()
                    run_information["number_of_workers"] = max_workers
                    total_time = 0
                    for trial in range(number_of_trials):
                        start_time = time()
                        results = manager.run(aevap, max_workers=max_workers)
                        total_time += time() - start_time

                    run_information["duration"] = total_time / number_of_trials
                    log.append(run_information.copy())
                    print_string = f"Number of runs: {run_information['number_of_runs']}, Duration: {run_information['duration']:.2f} seconds, Number of workers: {run_information['number_of_workers']} \n"
                    print(print_string)
                    #append to output file
                    with open("output.txt", "a") as f:
                        f.write(print_string)

    for entry in log:
        print(f"Number of runs: {entry['number_of_runs']}, Duration: {entry['duration']:.2f} seconds, Number of workers: {entry['number_of_workers']}")

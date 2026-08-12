from enum import Enum
import importlib

class Program(Enum):
    ACOND = "ACOND"
    ACU = "ACU"
    AEVAP = "AEVAP"
    ASYS = "ASYS"
    AWCSYS = "AWCSYS"
    AWESYS = "AWESYS"
    COMP = "COMP"
    FAD = "FAD"
    STA = "STA"
    WCL = "WCL"
    WCSYS = "WCSYS"
    WCU = "WCU"
    WEL = "WEL"
    WESYS = "WESYS"
    WLHPA = "WLHPA"
    WWSYS = "WWSYS"

@property
def loaded_class(self):
    module = importlib.import_module(self.value.upper())
    return getattr(module, self.value.upper())

@property
def name(self):
    return self.value

@property
def exe(self):
    return f"{self.value}.exe"

Program.cls = loaded_class
Program.exe = exe
Program.name = name

class Dat(Enum):
    BPHE = "BPHE"
    COIL = "COIL"
    COIL1 = "COIL1"
    COMAIR = "COMAIR"
    COMP = "COMP"
    COMPL = "COMPL"
    EDCON = "EDCON"
    EDEVA = "EDEVA"
    PACKLESS = "PACKLESS"
    REF = "REF"
    REVALV = "REVALV"
    TURBO = "TURBO"

@property
def dat(self):
    return f"{self.value}.dat"

Dat.name = name
Dat.dat = dat


if __name__ == "__main__":
    new_executable = Program.AEVAP.cls()
    print(f"The class: {Program.AEVAP.cls}")
    print(f"The name: {Program.AEVAP.name}")
    print(f"The executable: {Program.AEVAP.exe}")
    print(f"The dat file: {Dat.COIL.dat}")
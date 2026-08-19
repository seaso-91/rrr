from enum import Enum
import importlib


class Program(Enum):
    ACOND = "acond.acond"
    ACU = "acu.acu"
    AEVAP = "aevap.aevap"
    ASYS = "asys.asys"
    ASYS_DX = "asys.asys_dx"
    ASYS_HP = "asys.asys_hp"
    AWCSYS = "awcsys.awcsys"
    AWESYS = "awesys.awesys"
    COMP = "comp.comp"
    FAD = "fad.fad"
    STA = "sta.sta"
    WCL = "wcl.wcl"
    WCSYS = "wcsys.wcsys"
    WCU = "wcu.wcu"
    WEL = "wel.wel"
    WESYS = "wesys.wesys"
    WLHPA = "wlhpa.wlhpa"
    WWSYS = "wwsys.wwsys"

@property
def loaded_class(self):
    module = importlib.import_module(f"src.models.{self.value.split('.')[0]}")
    return getattr(module, self.value.split('.')[0].upper())

@property
def name(self):
    return self.value.split('.')[0].upper()

@property
def exe(self):
    return f"{self.name}.exe"

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

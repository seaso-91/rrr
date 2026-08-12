import pytest
from src.models import rr_enums as e

def test_cls():
    assert str(e.Program.AEVAP.cls) == "<class 'src.models.aevap.AEVAP'>", "The cls property should return the correct class for AEVAP."

def test_name():
    assert str(e.Program.AEVAP.name) == "AEVAP", "The name property should return the correct name for AEVAP."

def test_exe():
    assert str(e.Program.AEVAP.exe) == "AEVAP.exe", "The exe property should return the correct executable name for AEVAP."

def test_dat():
    assert str(e.Dat.COIL.dat) == "COIL.dat", "The dat property should return the correct dat file name for COIL."

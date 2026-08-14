import subprocess
import runpy
import sys
from pathlib import Path
from enum import Enum
class Module(Enum):
    EXECUTABLE_CONTROLLER = "src.controllers.executable_controller"
    EXECUTABLE = "src.models.executable"
    TESTING_BLOCK_INPUT = "tests.testing_block_input"
    RR_INPUT_TEXT = "src.controllers.rr_input_text"
    STRING_INPUTS_CONTROLLER = "src.controllers.string_inputs_controller"
    INPUTS_CONTROLLER = "src.controllers.inputs_controller"
    TESTING = "tests.testing"

if __name__ == "__main__":

    
    target_module = Module.EXECUTABLE_CONTROLLER.value

    runpy.run_module(target_module, run_name="__main__", alter_sys=True)

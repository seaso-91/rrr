import subprocess
import runpy
import sys
from pathlib import Path
from enum import Enum
class Module(Enum):
    RR_FILE_MANAGER = "src.controllers.rr_file_manager"
    RR = "src.models.rr"
    TESTING_BLOCK_INPUT = "tests.testing_block_input"
    RR_INPUT_TEXT = "src.controllers.rr_input_text"
    STRING_INPUTS_CONTROLLER = "src.controllers.string_inputs_controller"
    INPUTS_CONTROLLER = "src.controllers.inputs_controller"
    TESTING = "tests.testing"

if __name__ == "__main__":

    
    target_module = Module.TESTING.value

    runpy.run_module(target_module, run_name="__main__", alter_sys=True)

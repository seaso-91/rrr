import subprocess
import runpy
import sys
from pathlib import Path
from enum import Enum
class Module(Enum):

    STRING_INPUTS_CONTROLLER = "src.controllers.string_inputs_controller"
    EXECUTABLE_CONTROLLER = "src.controllers.executable_controller"
    INPUTS_CONTROLLER = "src.controllers.inputs_controller"
    SIMULATION_CONTROLLER = "src.controllers.system_controller"

    
    TESTING_BLOCK_INPUT = "tests.testing_block_input"
    TESTING = "tests.testing"
    DATA_CONTROLLER = "src.controllers.data_controller"

if __name__ == "__main__":
    target_module = Module.SIMULATION_CONTROLLER.value
    runpy.run_module(target_module, run_name="__main__", alter_sys=True)

    
import subprocess
import runpy
import sys
from pathlib import Path
from enum import Enum
class Module(Enum):
    RR_FILE_MANAGER = "src.controllers.rr_file_manager"
    RR_MODEL = "src.models.rr"
    TESTING_BLOCK_INPUT = "tests.testing_block_input"

if __name__ == "__main__":

    
    target_module = Module.RR_FILE_MANAGER.value

    runpy.run_module(target_module, run_name="__main__", alter_sys=True)

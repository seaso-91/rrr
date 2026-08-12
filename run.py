import subprocess
import runpy
import sys
from pathlib import Path
if __name__ == "__main__":

    # directory = Path("C:\\Users\\jajones\\Desktop\\rrr\\programs\\14007")
    # exe = directory / "AEVAP.exe"

    # result = subprocess.run(
    #     [str(exe), "d1.dat"],
    #     capture_output=True,
    #     text=True,
    #     cwd=directory
    # )
    # print(result.stdout)
    target_module = "src.controllers.rr_file_manager"
    #target_module = "src.models.rr"

    runpy.run_module(target_module, run_name="__main__", alter_sys=True)

    # from src.models.aevap import AEVAP
    # from tkinterdnd2 import TkinterDnD
    # root = TkinterDnD.Tk()
    # aevap = AEVAP()
    # root.title("AEVAP GUI")
    # widget = aevap.Widget(master=root)
    # widget.pack(side="left")
    # root.mainloop()
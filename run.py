import runpy
import sys
if __name__ == "__main__":

    target_module = "src.controllers.rr_file_manager"
    #target_module = "src.models.rr"
    target_module = "src.models.rr_enums"

    runpy.run_module(target_module, run_name="__main__", alter_sys=True)

    # from src.models.aevap import AEVAP
    # from tkinterdnd2 import TkinterDnD
    # root = TkinterDnD.Tk()
    # aevap = AEVAP()
    # root.title("AEVAP GUI")
    # widget = aevap.Widget(master=root)
    # widget.pack(side="left")
    # root.mainloop()
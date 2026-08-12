if __name__ == "__main__":
    from src.models.aevap import AEVAP
    from tkinterdnd2 import TkinterDnD
    root = TkinterDnD.Tk()
    aevap = AEVAP()
    root.title("AEVAP GUI")
    widget = aevap.Widget(master=root)
    widget.pack(side="left")
    root.mainloop()
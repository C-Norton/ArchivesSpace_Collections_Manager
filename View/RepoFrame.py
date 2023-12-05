from tkinter import ttk
import MasterFrame
class RepoFrame(ttk.Frame):
    def __init__(self,masterframe:MasterFrame):
        super().__init__()
        self.masterframe = masterframe
        repocount = self.masterframe.main.datamodel.getRepositoryCount()
        if repocount == 0:
            pass
        elif repocount <= 3:
            pass
        elif repocount <= 6:
            pass
        else:
            pass

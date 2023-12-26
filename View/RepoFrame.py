import tkinter
from tkinter import ttk

import View.MasterFrame as MasterFrame


class RepoFrame(ttk.Frame):
    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.masterframe = parent
        self.pack(side="bottom", fill="x")
        self.checkbuttons = dict()

    def refresh(self):
        repos = self.masterframe.main.connectionmanager.get_repository_list()

        i = 0
        for repo in repos:
            repo = repos[f"{repo}"]
            checkvar = tkinter.IntVar()
            self.checkbuttons.update(
                {
                    repo["uri"]: (
                        checkvar,
                        ttk.Checkbutton(
                            self,
                            text=repo["repo_code"],
                            variable=checkvar,
                            onvalue=1,
                            offvalue=0,
                        ).grid(column=i % 3, row=i // 3),
                    )
                }
            )
            i += 1
        for child in self.winfo_children():
            child.grid_configure(padx=2, pady=5)

    def get_selected_repos(self):
        uris: list = list()
        for repo, checkbutton in self.checkbuttons:
            checkbutton: ttk.Checkbutton
            s = None
            checkbutton.getint(s)
            if s:
                uris += [repo]

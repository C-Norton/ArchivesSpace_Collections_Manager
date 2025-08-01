import tkinter
from tkinter import ttk

import view.MasterFrame as MasterFrame


class RepoFrame(ttk.Frame):
    """This frame adds checkboxes for each repository other than the base system repository."""

    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.pack(side="bottom", fill="x")
        self.check_buttons = dict()

    def refresh(self):
        repos = self.master_frame.connection_manager.get_repository_list()

        i = 0
        for repo in repos:
            repo = repos[f"{repo}"]
            checkvar = tkinter.IntVar()
            self.check_buttons.update(
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
        for repo, checkbutton in self.check_buttons:
            checkbutton: ttk.Checkbutton
            s = None
            checkbutton.getint(s)
            if s:
                uris += [repo]

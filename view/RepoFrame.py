
import tkinter
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from view.MasterFrame import MasterFrame


class RepoFrame(ttk.Frame):
    """This frame adds checkboxes for each repository other than the base system repository."""

    def __init__(self, parent: ttk.Frame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.check_buttons = dict()

    def refresh(self):
        repos = self.master_frame.connection_manager.get_repositories()

        for index, repo in enumerate(repos):
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
                        ).grid(column=index % 3, row=index // 3),
                    )
                }
            )

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

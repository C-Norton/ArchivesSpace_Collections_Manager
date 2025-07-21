import tkinter
from tkinter import ttk
from View import MasterFrame


class QueryFrame(ttk.Frame):
    """
    This is a breakout of individual query segments. It's still a work in progress
    """

    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.master_frame = parent
        self.frame = ttk.Frame(master=self.master_frame)
        self.pack(side="bottom", fill="x")
        self.width = 1
        self.height = 1
        self.operator = tkinter.StringVar()
        self.operator.set("AND")
        self.draw_query_frame(None, 0)

    def draw_query_frame(self, query: str, depth: int):
        for i in range(depth):
            label = ttk.Label(self, text="    ")
            label.pack(side="left", fill="x")
        label = ttk.Label(self, text=query)
        label.pack(side="left", fill="x")
        operator = ttk.OptionMenu(self.frame, self.operator, *["AND", "OR"])
        operator.pack(side="left", fill="x")
        remove = ttk.Button(self.frame, name="remove", command=self.remove)
        remove.pack(side="left", fill="x")

    def remove(self):
        pass

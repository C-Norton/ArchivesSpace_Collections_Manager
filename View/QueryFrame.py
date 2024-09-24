from tkinter import ttk, Grid
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
        self.draw_query_frame(None)

    def draw_query_frame(self, query: str, depth :int):
        for i in range(depth):
            label = ttk.Label(self, text="    ")
            label.pack(side="left", fill="x")
        label = ttk.Label(self, text=query)
        label.pack(side="left", fill="x")
        operator = ttk.OptionMenu(self.frame, self.master_frame.operators, *["AND", "OR"])
        operator.pack(side="left", fill="x")
        remove = ttk.Button(self.frame,name="Remove",command=self.remove)
        remove.pack(side="left", fill="x")
    def remove(self):
        pass
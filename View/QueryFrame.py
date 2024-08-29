class QueryFrame(ttk.Frame):


    def __init__(self, parent: MasterFrame):
        super().__init__(master=parent, padding="3 3 12 12")
        self.masterframe = parent
        self.pack(side="bottom", fill="x")
        self.width = 1
        self.height = 1
        self.draw_query_frame()

    def draw_query_frame(self, query : str):
        pass
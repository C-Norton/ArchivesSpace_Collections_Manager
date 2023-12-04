# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import tkinter
from tkinter import ttk

import View.MenuFrame


class MainGui():


    def __init__(self):
        root = tkinter.Tk()
        root.geometry("750x200")
        masterFrame = ttk.Frame()
        logging.debug("Frame Created")

        # Set the properties of our main frame
        masterFrame.pack(fill="both", expand=True)
        root.title("ArchivesSpace Collections Manager")

        View.MenuFrame.drawMenuFrame(ttk.Frame(masterFrame, padding="3 3 12 12"))

        # Start setting up the lower portion of our window
        queryRegion = ttk.Frame(masterFrame, padding="3 3 12 12")
        queryRegion.pack(side="bottom", fill='x')
        ttk.Label(queryRegion, text="foo").grid(column=1, row=1)

        for child in queryRegion.winfo_children():
            child.grid_configure(padx=5, pady=5)
        logging.debug("UI initialized successfully!")

        masterFrame.mainloop()
        masterFrame.focus_force()
        logging.info("UI started successfully!")



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = MainGui()

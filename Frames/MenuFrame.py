import logging
from tkinter import ttk, Grid

import main


def drawMenuFrame(menu):
    menu.pack(side="top", fill='x')
    logging.debug("Initial frame setup complete")

    # Create top menu
    Buttons = [
        ttk.Button(menu, text="Configure Connection", command=main.CollectionsManagerGui.connectionDialog).grid(
            column=0, row=0,
            sticky="EW"),
        ttk.Button(menu, text="Save Connection", command=main.CollectionsManagerGui.saveConnection).grid(column=1,
                                                                                                         row=0,
                                                                                                         sticky="EW"),
        ttk.Button(menu, text="Manage Saved Connections").grid(column=2, row=0, sticky="EW"),
        ttk.Button(menu, text="Test Connection", command=main.CollectionsManagerGui.testConnection).grid(column=3,
                                                                                                         row=0,
                                                                                                         sticky="EW"),
        ttk.Button(menu, text="Save Query").grid(column=4, row=0, sticky="EW"),
        ttk.Button(menu, text="Load Query").grid(column=5, row=0, sticky="EW"),
        ttk.Button(menu, text="Refresh Repositories").grid(column=6, row=0, sticky="EW"),
        ttk.Button(menu, text="Help", command=main.CollectionsManagerGui.helpButton).grid(column=7, row=0, sticky="EW")]

    logging.debug("buttons created")

    # Set up dynamic button resizing
    Grid.rowconfigure(menu, index=0, weight=1)
    for i in range(len(Buttons)):
        Grid.columnconfigure(menu, index=i, weight=1)

    for child in menu.winfo_children():
        child.grid_configure(padx=2, pady=5)
    logging.debug("Main menu created successfully!")

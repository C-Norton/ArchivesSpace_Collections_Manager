# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import Controller.ConnectionManager as CM
import Model.DataModel as DM
import View.MasterFrame as MF
import Controller.Connection

import faulthandler

class Main:
    connection_manager: CM.ConnectionManager = None
    data_model: DM.DataModel = None
    master_frame: MF.MasterFrame = None

    def __init__(self):
        Main.connection_manager = CM.ConnectionManager(self)
        Main.data_model = DM.DataModel(self)
        Main.master_frame = MF.MasterFrame(self)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    faulthandler.enable()
    app = Main()

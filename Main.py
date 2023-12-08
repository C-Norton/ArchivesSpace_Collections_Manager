# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging
import Controller.ConnectionManager as CM
import Model.DataModel as DM
import View.MasterFrame as MF
import Controller.Connection


class Main():

    connectionmanager : CM.ConnectionManager = None
    datamodel : DM.DataModel = None
    masterframe : MF.MasterFrame = None
    def __init__(self):
        Main.connectionmanager = CM.ConnectionManager(Controller.Connection.Connection("","",""))
        Main.datamodel = DM.DataModel()
        Main.masterframe = MF.MasterFrame(self)







if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = Main()

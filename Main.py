import logging

import model.DataModel as DM
import view.MasterFrame as MF

import faulthandler




class Main:
    connection_manager = None
    data_model: DM.DataModel = None
    master_frame: MF.MasterFrame = None

    def __init__(self):
        from controller.connection_manager import ConnectionManager

        Main.data_model = DM.DataModel(self)
        Main.connection_manager = ConnectionManager(self)

        Main.master_frame = MF.MasterFrame(Main.connection_manager)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    faulthandler.enable()
    app = Main()

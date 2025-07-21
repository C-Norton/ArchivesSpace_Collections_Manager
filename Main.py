import logging

import Model.DataModel as DM
import View.MasterFrame as MF

import faulthandler


class Main:
    connection_manager = None
    data_model: DM.DataModel = None
    master_frame: MF.MasterFrame = None

    def __init__(self):
        from Controller import ConnectionManager as CM

        Main.connection_manager = CM.ConnectionManager()
        Main.data_model = DM.DataModel(self)
        Main.master_frame = MF.MasterFrame(self)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    faulthandler.enable()
    app = Main()

#! /bin/python
from bus import Module,BUS_TYPE,Payloads
from config import MongooseConfig,loadConfig
from interfaces import getInterface, Interface
from gcode import GCodeParser
from tuitools import clear

cfg:MongooseConfig = loadConfig()
interface:Interface = getInterface(cfg.interface)
parser = GCodeParser()

def gBusCallback(payload:Payloads.GBUS):
    gCode = parser.parse(payload.gcode)
    print(gCode.format())

def main():
    clear()
    module:Module = Module(
        module_name='gcode-interface',
        requiredBusses=((BUS_TYPE.GBUS,))
        )

    module.busIO.set_GBUS_callback(gBusCallback)

    module.connect()
    module.start(loopForever=True)


if __name__=="__main__":
    main()


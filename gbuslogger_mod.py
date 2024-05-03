#! /bin/python
from bus import Module,BUS_TYPE,Payloads
from gcode import GCodeParser
from tuitools import clear

def gBusCallback(payload:Payloads.GBUS):
    gCode = parser.parse(payload.gcode)
    print(gCode.format())

def main():
    clear()
    module:Module = Module(
        mongoose_id='gbuslogger',
        requiredBusses=((BUS_TYPE.GBUS,))
        )
    module.busIO.set_GBUS_callback(gBusCallback)
    module.connect()
    module.start(loopForever=True)


if __name__=="__main__":
    parser = GCodeParser()
    main()


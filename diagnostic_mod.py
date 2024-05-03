#! /bin/python
from bus import Module,BUS_TYPE,Payloads
from tuitools import colorize as cs, Colors, clear

colorLookup = (
        Colors.RED,
        Colors.LIGHT_RED,
        Colors.ORANGE,
        Colors.BLUE)
LOG_TAG=cs("LOG".rjust(10),Colors.LIGHT_CYAN)
def logCallback(payload:Payloads.Log):
    color = (colorLookup[payload.level] 
             if payload.level < 4 
             else Colors.LIGHT_GRAY)
    name = cs(payload.name,Colors.LIGHT_GRAY)
    message = cs(payload.msg,color)
    print(f'{LOG_TAG}: {name} - {message}')

STATUS_TAG=cs("STATUS".rjust(10),Colors.LIGHT_PURPLE)
def statusCallback(payload:Payloads.Status):
    print(f'{STATUS_TAG}: {payload.id} : {payload.status}')

COMMAND_TAG=cs("COMMAND".rjust(10),Colors.LIGHT_GREEN)
def commandCallback(payload:Payloads.Command):
    print(f'{COMMAND_TAG}: {payload.source}->{payload.dest} : {payload.command}')
    

def main():
    clear()
    module:Module = Module(
        mongoose_id='diagnostic',
        requiredBusses=(BUS_TYPE.LOG,BUS_TYPE.STATUS,BUS_TYPE.COMMAND)
        )

    module.busIO.set_LOG_callback(logCallback)
    module.busIO.set_STATUS_callback(statusCallback)
    module.busIO.set_COMMAND_callback(commandCallback,filter=lambda P:True)

    module.connect()
    module.start(loopForever=True)

if __name__=="__main__":
    main()



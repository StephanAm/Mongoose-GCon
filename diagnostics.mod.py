#! /bin/python
from bus import Module,BUS_TYPE,Payloads
from tuitools import colorize_string as cs, Colors, clear

colorLookup = (
        Colors.RED,
        Colors.LIGHT_RED,
        Colors.ORANGE,
        Colors.BLUE)
def logCallback(payload:Payloads.Log):
    color = (colorLookup[payload.level] 
             if payload.level < 3 
             else Colors.LIGHT_GRAY)
    name = cs(payload.name,Colors.LIGHT_GRAY)
    message = cs(payload.msg,color)
    print(f'{name}: {message}')

def statusCallback(payload:Payloads.Message):
    print(f'STATUS: {payload.name} : {payload.status}')

def commandCallback(payload:Payloads.Command):
    print(f'COMMAND: {payload.source}->{payload.dest} : {payload.command}')
    

def main():
    clear()
    module:Module = Module(
        module_name='diagnostics',
        requiredBusses=(BUS_TYPE.LOG,BUS_TYPE.STATUS,BUS_TYPE.COMMAND)
        )

    module.busIO.set_LOG_callback(logCallback)
    module.busIO.set_STATUS_callback(statusCallback)
    module.busIO.set_COMMAND_callback(commandCallback)

    module.connect()
    module.start(loopForever=True)

if __name__=="__main__":
    main()



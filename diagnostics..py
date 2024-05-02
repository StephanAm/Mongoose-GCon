from bus import Module,BUS_TYPE,MessageDefs

def logCallback(msg:MessageDefs.LogMessage):
    print(msg)

def statusCallback(msg:MessageDefs.StatusMessage):
    print(msg)

module:Module = Module(
    module_name='diagnostics',
    requiredBusses=(BUS_TYPE.LOG,BUS_TYPE.STATUS)
    )

module.busIO.set_LOG_callback(logCallback)
module.busIO.set_STATUS_callback(statusCallback)


module.connect()
module.start(loopForever=True)




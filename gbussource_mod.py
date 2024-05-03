#! /bin/python
from bus import Module,BUS_TYPE,Payloads,MONGOOSE_IDS,RunState,STATUS
from gcode import GCodeParser
from tuitools import clear
from time import sleep

class Handler:
    def __init__(self,module:Module):
        self.mongoose_id = module.mongoose_id
        self.log = module.log
        module.busIO.set_COMMAND_callback(self.commandCallback)
        module.busIO.set_STATUS_callback(self.statusCallback)
        self.module = module
        self.args:dict = {}
        self.isProcessing=False
        self.isPaused=False
        self.gcodeIterator=None
        self.gcodes=None
        self.sink_status = STATUS.UNKNOWN
    def statusCallback(self,payload:Payloads.Status):
        if payload.id == MONGOOSE_IDS.GBUS_SINK:
            self.sink_status = payload.status

    def commandCallback(self,payload:Payloads.Command):
        match payload.command:
            case Payloads.COMMAND.SET:
                self.args.update(payload.args)
            case Payloads.COMMAND.RUN: self.run()
            case Payloads.COMMAND.PAUSE:self.pause()
            case Payloads.COMMAND.STOP:self.stop()
                    
    def run(self):
        camfile = self.args.get('camfile',None)
        if camfile is None:
            self.log.error("Can't start: CAM file has not bee set")
            return
        if self.isPaused:
            self.isPaused = False
            self.log.info("Resuming run")
            self.module.setStatus(STATUS.PAUSED)
            return
        if self.isProcessing:
            self.log.warn("Got a 'RUN' istruction but i'm already running")
            return
        with open(camfile) as f:
            self.gcodes = f.readlines()
        self.log.info("CAM file loaded, starting run")
        self.gcodeIterator = iter(self.gcodes)
        self.isProcessing = True
        self.module.setStatus(STATUS.RUNNING)

    def stop(self):
        self.gcodeIterator=None
        self.gcodes=None
        self.isProcessing=False
        self.isPaused=False
        self.module.setStatus(STATUS.STOPPED)
        self.log.info("Run stopped")

    def pause(self):
        if not self.isProcessing:
            self.log.info("Not currently running")
            return
        self.log.info("Run paused")
        self.isPaused=True
        self.module.setStatus(STATUS.PAUSED)

    def processingloop(self):
        while self.isProcessing:
            sleep(0.05)
            if self.isPaused:
                sleep(0.1)
            else:
                try:
                    if self.sink_status == STATUS.RUNNING:
                        self.module.busIO.send_GBUS(next(self.gcodeIterator))
                    else:
                        sleep(0.1)
                except StopIteration:
                    self.log.info('processing complete')
                    self.stop()

    def mainloop(self):
        while self.module.run_loop:
            self.processingloop()
            sleep(0.5)
        self.log.debug('Aborting Mainloop')

def main():
    clear()
    id=MONGOOSE_IDS.GBUS_SOURCE
    module:Module = Module(
        mongoose_id=id,
        requiredBusses=((BUS_TYPE.COMMAND,BUS_TYPE.STATUS))
        )
    handler = Handler(module)
    module.connect()
    module.start(
        loopForever=False,
        start_up_status=STATUS.STOPPED)
    handler.mainloop()

if __name__=="__main__":
    parser = GCodeParser()
    main()


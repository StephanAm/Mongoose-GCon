#! /bin/python
from bus import Module,BUS_TYPE,MONGOOSE_IDS,STATUS,Payloads
from config import GBusSinkConfig,loadConfig
from interfaces import getInterface, Interface
from gcode import GCodeParser
from tuitools import clear
import queue

class GcodeQueue(queue.Queue):
    def __init__(self, waterlevel:int, headroom:int,hyst=2) -> None:
        super().__init__()
        self.wlh=waterlevel+hyst
        self.wll=waterlevel-hyst

        self.hyst=hyst
    
    def put(self,item)->bool:
        super().put(item,block=False)
    
    def tooFull(self):return self.qsize() > self.wlh
    def tooEmpty(self):return self.qsize() < self.wll
        

class Handler:
    def __init__(self,module:Module,queue:GcodeQueue,interface:Interface):
        self.interface=interface
        self.module=module
        self.queue=queue
        self.log = self.module.log
        module.busIO.set_GBUS_callback(self.gBusCallback)
        self.status = STATUS.RUNNING

    def setStatus(self,newStatus):
        if self.status == newStatus:
            return
        self.status == newStatus
        self.module.setStatus(status=newStatus)

    def gBusCallback(self, payload:Payloads.GBUS):
        try:
            self.queue.put(payload.gcode)
        except queue.Full:
            self.log.error("GBUS BUFFER OVERRUN")
            self.module.panic()

        if self.queue.tooFull():
            self.module.setStatus(STATUS.PAUSED)
        
    def mainLoop(self):
        while self.module.run_loop:
            try:
                gcode = self.queue.get(timeout=0.1)
                self.interface.send(gcode)
            except queue.Empty:
                ...
                # Timing out is not a problem.
                # Just breaking out of the wait for housekeeping
            if self.queue.tooEmpty():
                self.module.setStatus(STATUS.RUNNING)


def main():
    clear()
    config:GBusSinkConfig = loadConfig(MONGOOSE_IDS.GBUS_SINK,config_cls=GBusSinkConfig)
    interface:Interface = getInterface(config)
    module:Module = Module(
        mongoose_id=MONGOOSE_IDS.GBUS_SINK,
        requiredBusses=((BUS_TYPE.GBUS,))
        )
    
    queue = GcodeQueue(config.waterlevel,config.headroom)
    handler = Handler(module,queue,interface)

    module.connect()
    module.start(loopForever=False)
    handler.mainLoop()

if __name__=="__main__":
    parser = GCodeParser()
    main()


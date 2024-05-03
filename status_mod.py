#! /bin/python
from config import loadAllConfig, MongooseConfig
from typing import Dict
from bus import Module, BUS_TYPE, Payloads, STATUS
from tuitools import WindowInterface,Colors,colorize
import curses

statusIcons = {
    STATUS.RUNNING:('',11),
    STATUS.PAUSED:('',13),
    STATUS.STOPPED:('',13),
    STATUS.DOWN:('',10),
    STATUS.UNKNOWN:('',9)}

class Handler:
    def __init__(self,config,scr,module):

        self.config:Dict[str:MongooseConfig] = config
        self.scr:WindowInterface = scr
        self.mongoose_status = {k:STATUS.UNKNOWN for k,_ in config.items()}
        module.busIO.set_STATUS_callback(self.statusCallback)
        module.busIO.set_COMMAND_callback(self.commandCallback)
        self.request_status = module.request_status
        self.module=module
        self.log = self.module.log

    def printStatuses(self):
        for i,mongoose in enumerate(self.config.values()):
            name=mongoose.name
            self.scr.addstr(i,10,mongoose.name)
            status = self.mongoose_status[mongoose.mongoose_id]
            icon,color = statusIcons[status]
            self.scr.addstr(i,8,icon,curses.color_pair(color))
        self.scr.refresh()

    def statusCallback(self, payload:Payloads.Status):
        self.mongoose_status[payload.id] = payload.status
        self.printStatuses()

    def commandCallback(self, payload:Payloads.Command):
        print(f'COMMAND: {payload.source}->{payload.dest} : {payload.command}')
    
    def mainloop(self):
        while self.module.run_loop:
            key = self.scr.getch()
            match key:
                case curses.KEY_F5:
                    self.request_status()

def main(scr):
    config = loadAllConfig()
    module:Module = Module(
        mongoose_id='statusmonitor',
        requiredBusses=(BUS_TYPE.STATUS,BUS_TYPE.COMMAND)
    )
    module.connect()
    module.start(loopForever=False)

    handler = Handler(config,scr,module)
    handler.printStatuses()
    
    handler.mainloop()
    


if __name__=="__main__":
    try:
        scr = curses.initscr()
        curses.start_color()
        curses.use_default_colors()
        curses.noecho()
        scr.keypad(True)
        for i in range(16):
            curses.init_pair(i + 1, i, -1)
        scr.clear()
        main(scr)
    finally:
        curses.nocbreak()
        scr.keypad(False)
        curses.echo()
        curses.endwin()
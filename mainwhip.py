#! /bin/python
import tuitools
from filelocations import cam_directory
from os import listdir
from mainwhip_lib import State
from bus import RunState,Module,BusIO,MONGOOSE_IDS,Payloads

w = tuitools.Whiptail(title="Main Whip", backtitle="Mongoose controller")

def choose_file(state:State, bus:BusIO):
    files = listdir(cam_directory)
    choice,code = w.menu("Choose Cam File",files)
    if code==0:
        state.camfile=cam_directory.joinpath(choice).absolute()
    bus.send_COMMAND(
        Payloads.COMMAND.SET,
        MONGOOSE_IDS.GBUS_SOURCE,
        camfile=str(state.camfile)
    )
    
def start_streaming(state:State, bus:BusIO):
    bus.send_COMMAND(
        Payloads.COMMAND.RUN,
        MONGOOSE_IDS.GBUS_SOURCE)
    
    # do starting things
    state.runState = RunState.RUNNING

def pause_streaming(state:State, bus:BusIO):
    bus.send_COMMAND(
        Payloads.COMMAND.PAUSE,
        MONGOOSE_IDS.GBUS_SOURCE)
    state.runState = RunState.PAUSED

def stop_streaming(state:State, bus:BusIO):
    bus.send_COMMAND(
        Payloads.COMMAND.STOP,
        MONGOOSE_IDS.GBUS_SOURCE
    )
    state.runState = RunState.STOPPED

def show_status(state:State, bus:BusIO):
    msg= "\n".join((
        f"Selected File:{state.camfile}",
        f"Current Run State: {state.runState}"
    ))
    w.msgbox(msg)

def main_menu(state:State, bus:BusIO):
    while True:
        choice,code = w.menu(
            "Main Menu", 
            [("1","Status"), 
            ("2","Choose File"), 
            ("3","Start"), 
            ("4","Pause"), 
            ("5","Stop"),
            ("6","Exit")])
        match choice:
            case '1': show_status(state, bus)
            case '2': choose_file(state, bus)
            case '3': start_streaming(state, bus)
            case '4': pause_streaming(state, bus)
            case '5': stop_streaming(state, bus)
            case '6': break
def main():
    module = Module(
        mongoose_id='mainwhip'
    )
    module.connect()
    module.start(loopForever=False)
    
    state = State()
    main_menu(state,module.busIO)
    module.killAll()

    module.stop()
if __name__=="__main__":
    main()


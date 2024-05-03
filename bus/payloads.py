from dataclasses import dataclass,field,asdict
from . import _module_status
from enum import Enum
import json

class COMMAND(str,Enum):
    RUN="RUN"           # Instructs a Mongoose to start/resum operation
    PAUSE="PAUSE"       # Instructs a Mongoose to pause operation. Only useful for stateful jobs, i.e. processing a file
    STOP="STOP"         # Instructs a Mongoose to suspend normal operation
    SET="SET"           # Instructs a Mongoose to set some value in its internal state.

class SYSTEM_COMMAND(str, Enum):
    KILL="KILL"
    PANIC="PANIC"
    STATUS_UPDATE="STATUS_UPDATE"

class PayloadFormatError(Exception):
    def __init__(self,message,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.message = message

class BusPayload:
    def serialize(self):
        'Returns json format. Override this if another format is required'
        return json.dumps(asdict(self))
    
    @classmethod
    def deserialize(cls,src:str):
        'Accepts json format. Override this if another format is required'
        try:
            return cls(**(json.loads(src)))
        except json.JSONDecodeError as x:
            raise PayloadFormatError(f'{cls.__name__} was unable to deserialize the message') from x


@dataclass
class System(BusPayload):
    source:str
    dest:str
    command:SYSTEM_COMMAND
    
    def __post_init__(self):
        self.command=SYSTEM_COMMAND(self.command)

# COMMAND="command"
@dataclass
class Command(BusPayload):
    source:str
    dest:str
    command:COMMAND
    args:dict=field(default_factory=dict)
    
    def __post_init__(self):
        self.command=COMMAND(self.command)

# STATUS="status"
@dataclass
class Status(BusPayload):
    id:str
    status:_module_status.STATUS=field()
    def __post_init__(self):
        self.status = _module_status.STATUS(self.status)

# GBUS="gbus"
@dataclass
class GBUS(BusPayload):
    gcode:str
    def serialize(self):
        return self.gcode
    @classmethod
    def deserialize(cls, src: str):
        return(cls(gcode=src))

# LOG="log"
@dataclass
class Log(BusPayload):
    level:int
    name:str
    msg:str

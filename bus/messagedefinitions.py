from dataclasses import dataclass,field,asdict
import json

class MessageFormatError(Exception):
    def __init__(self,message,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.message = message

class BusMessage:
    
    def serialize(self):
        'Returns json format. Override this if another format is required'
        return json.dumps(asdict(self))
    
    @classmethod
    def deserialize(cls,src:str):
        'Accepts json format. Override this if another format is required'
        try:
            return cls(**(json.loads(src)))
        except json.JSONDecodeError as x:
            raise MessageFormatError(f'{cls.__name__} was unable to deserialize the message') from x


# PANIC="panic"
@dataclass
class SystemMessage(BusMessage):
    source:str
    dest:str
    command:str


# COMMAND="command"
@dataclass
class CommandMessage(BusMessage):
    source:str
    dest:str
    command:str

# STATUS="status"
@dataclass
class StatusMessage(BusMessage):
    name:str
    status:str

# GBUS="gbus"
@dataclass
class GbusMessage(BusMessage):
    gcode:str
    def serialize(self):
        return self.gcode
    @classmethod
    def deserialize(cls, src: bytes):
        return(cls(gcode=src.decode()))

# LOG="log"
@dataclass
class LogMessage(BusMessage):
    level:int
    name:str
    msg:str

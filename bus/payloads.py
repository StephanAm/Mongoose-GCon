from dataclasses import dataclass,field,asdict
import json

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


# PANIC="panic"
@dataclass
class System(BusPayload):
    source:str
    dest:str
    command:str

# COMMAND="command"
@dataclass
class Command(BusPayload):
    source:str
    dest:str
    command:str

# STATUS="status"
@dataclass
class Message(BusPayload):
    name:str
    status:str

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

from interfaces.common import Interface, Response
import time

class DummyInterface(Interface):
    type='dummy'
    def __init__(self,type,delay) -> None:
        _ = type
        self.delay = delay

    def send(self,gcode:str)-> Response:
        time.sleep(self.delay)
        return Response()
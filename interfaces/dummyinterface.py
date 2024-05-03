from interfaces.common import Interface, Response
import time

class DummyInterface(Interface):
    type='dummy'
    def __init__(self,delay) -> None:
        self.delay = delay

    def send(self,gcode:str)-> Response:
        print(gcode)
        time.sleep(self.delay)
        return Response()
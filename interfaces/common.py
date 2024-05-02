class Response:
    def format(self):
        return "OK"

class Interface:
    type='abstract'
    def send(gcode:str) -> Response:
        raise NotImplementedError()
        
from interfaces.dummyinterface import DummyInterface
from interfaces.common import Interface

_Interfaces = (DummyInterface,)

def getInterface(settings:dict):
    type = settings['type']
    I = next(filter(lambda i: i.type == type,_Interfaces))
    i:Interface = I(**settings)
    return i

def getInterfaceTypes():
    return [i.name for i in _Interfaces]



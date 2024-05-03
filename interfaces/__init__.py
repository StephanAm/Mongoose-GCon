from interfaces.dummyinterface import DummyInterface
from interfaces.common import Interface
from config import GBusSinkConfig

_Interfaces = (DummyInterface,)

def getInterface(config:GBusSinkConfig):
    type = config.type
    I = next(filter(lambda i: i.type == type,_Interfaces))
    i:Interface = I(**config.properties)
    return i

def getInterfaceTypes():
    return [i.name for i in _Interfaces]



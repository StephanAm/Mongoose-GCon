from typing import Iterable,Callable,Dict
from .bustypes import BUS_TYPE,topicFromBus
from paho.mqtt import client as paho_client
import bus.messagedefinitions as messagedefinitions

def thowBusNotSet(bus):
    bus=bus
    def thrower(*args,**kwargs):
        raise Exception(f'{bus} needs to be set in required busses to be able to add callback')
    return thrower

def thowCallbackAlreadySet(bus):
    bus=bus
    def thrower(*args,**kwargs):
        raise Exception(f'Callback for {bus} has already been set')
    return thrower

class BusIO:
    def __init__(self,module_name,required_busses:Iterable[BUS_TYPE],client:paho_client):
        self.module_name = module_name
        self.busses:Iterable[BUS_TYPE] = required_busses
        self.client:paho_client.Client = client
        if not BUS_TYPE.COMMAND in required_busses:
            self.set_COMMAND_callback = thowBusNotSet(BUS_TYPE.COMMAND)
        if not BUS_TYPE.STATUS in required_busses:
            self.set_STATUS_callback = thowBusNotSet(BUS_TYPE.STATUS)
        if not BUS_TYPE.SYSTEM in required_busses:
            self.set_SYSTEM_callback = thowBusNotSet(BUS_TYPE.SYSTEM)
        if not BUS_TYPE.GBUS in required_busses:
            self.set_GBUS_callback = thowBusNotSet(BUS_TYPE.GBUS)
        if not BUS_TYPE.LOG in required_busses:
            self.set_LOG_callback = thowBusNotSet(BUS_TYPE.LOG)
    
    def set_COMMAND_callback(self,callback:Callable[[messagedefinitions.CommandMessage],None]):
        self.COMMAND_callback=callback
        self.set_COMMAND_callback=thowCallbackAlreadySet(BUS_TYPE.COMMAND)
    
    def set_STATUS_callback(self,callback:Callable[[messagedefinitions.StatusMessage],None]):
        self.STATUS_callback=callback
        self.set_STATUS_callback=thowCallbackAlreadySet(BUS_TYPE.STATUS)
    
    def set_SYSTEM_callback(self,callback:Callable[[messagedefinitions.SystemMessage],None]):
        self.SYSTEM_callback=callback
        self.set_SYSTEM_callback=thowCallbackAlreadySet(BUS_TYPE.SYSTEM)
    
    def set_GBUS_callback(self,callback:Callable[[messagedefinitions.GbusMessage],None]):
        self.GBUS_callback=callback
        self.set_GBUS_callback=thowCallbackAlreadySet(BUS_TYPE.GBUS)
    
    def set_LOG_callback(self,callback:Callable[[messagedefinitions.LogMessage],None]):
        self.LOG_callback=callback
        self.set_LOG_callback=thowCallbackAlreadySet(BUS_TYPE.LOG)

    def handleMessage(self, bus:BUS_TYPE, payload:str):
        match bus:
            case BUS_TYPE.COMMAND: self.COMMAND_callback(messagedefinitions.CommandMessage.deserialize(payload))
            case BUS_TYPE.STATUS: self.STATUS_callback(messagedefinitions.StatusMessage.deserialize(payload))
            case BUS_TYPE.SYSTEM: self.SYSTEM_callback(messagedefinitions.SystemMessage.deserialize(payload))
            case BUS_TYPE.GBUS: self.GBUS_callback(messagedefinitions.GbusMessage.deserialize(payload))
            case BUS_TYPE.LOG: self.LOG_callback(messagedefinitions.LogMessage.deserialize(payload))
            case _: raise ValueError(f'{bus} is not a valid bus type')

    def send_COMMAND(self,msg:messagedefinitions.CommandMessage)->None:
        self.client.publish(topicFromBus(BUS_TYPE.COMMAND),msg.serialize())
        
    def send_STATUS(self,msg:messagedefinitions.StatusMessage)->None:
        self.client.publish(topicFromBus(BUS_TYPE.STATUS),msg.serialize())
    
    def send_PANIC(self,msg:messagedefinitions.SystemMessage)->None:
        self.client.publish(topicFromBus(BUS_TYPE.SYSTEM),msg.serialize())
    
    def send_GBUS(self,msg:messagedefinitions.GbusMessage)->None:
        self.client.publish(topicFromBus(BUS_TYPE.GBUS),msg.serialize())
    
    def send_LOG(self,msg:messagedefinitions.LogMessage)->None:
        self.client.publish(topicFromBus(BUS_TYPE.LOG),msg.serialize())
    
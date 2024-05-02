from typing import Iterable,Callable,Dict
from .bustypes import BUS_TYPE,topicFromBus
from paho.mqtt import client as paho_client
import bus.payloads as payloads

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
    
    def set_COMMAND_callback(
            self,
            callback:Callable[[payloads.Command],None],
            filter:Callable[[payloads.Command],None]=None):
        if not filter:
            self.COMMAND_callback=callback
        else:
            def COMMAND_callback(payload: payloads.Command):
                if not filter(payload): return
                callback(payload)
            self.COMMAND_callback = COMMAND_callback
        self.set_COMMAND_callback=thowCallbackAlreadySet(BUS_TYPE.COMMAND)
    
    def set_STATUS_callback(self,callback:Callable[[payloads.Message],None]):
        self.STATUS_callback=callback
        self.set_STATUS_callback=thowCallbackAlreadySet(BUS_TYPE.STATUS)
    
    def set_SYSTEM_callback(self,callback:Callable[[payloads.System],None]):
        self.SYSTEM_callback=callback
        self.set_SYSTEM_callback=thowCallbackAlreadySet(BUS_TYPE.SYSTEM)
    
    def set_GBUS_callback(self,callback:Callable[[payloads.GBUS],None]):
        self.GBUS_callback=callback
        self.set_GBUS_callback=thowCallbackAlreadySet(BUS_TYPE.GBUS)
    
    def set_LOG_callback(self,callback:Callable[[payloads.Log],None]):
        self.LOG_callback=callback
        self.set_LOG_callback=thowCallbackAlreadySet(BUS_TYPE.LOG)

    def handleMessage(self, bus:BUS_TYPE, payload:str):
        match bus:
            case BUS_TYPE.COMMAND: self.COMMAND_callback(payloads.Command.deserialize(payload))
            case BUS_TYPE.STATUS: self.STATUS_callback(payloads.Message.deserialize(payload))
            case BUS_TYPE.SYSTEM: self.SYSTEM_callback(payloads.System.deserialize(payload))
            case BUS_TYPE.GBUS: self.GBUS_callback(payloads.GBUS.deserialize(payload))
            case BUS_TYPE.LOG: self.LOG_callback(payloads.Log.deserialize(payload))
            case _: raise ValueError(f'{bus} is not a valid bus type')

    def send_COMMAND(self,msg:payloads.Command)->None:
        self.client.publish(topicFromBus(BUS_TYPE.COMMAND),msg.serialize())
        
    def send_STATUS(self,msg:payloads.Message)->None:
        self.client.publish(topicFromBus(BUS_TYPE.STATUS),msg.serialize())
    
    def send_PANIC(self,msg:payloads.System)->None:
        self.client.publish(topicFromBus(BUS_TYPE.SYSTEM),msg.serialize())
    
    def send_GBUS(self,msg:payloads.GBUS)->None:
        self.client.publish(topicFromBus(BUS_TYPE.GBUS),msg.serialize())
    
    def send_LOG(self,msg:payloads.Log)->None:
        self.client.publish(topicFromBus(BUS_TYPE.LOG),msg.serialize())
    
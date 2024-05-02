from typing import Callable, Iterable
from paho.mqtt import client as paho_client
from .logger import Logger
from .bustypes import BUS_TYPE,topicFromBus, busFromTopic
from .busio import BusIO
from .messagedefinitions import CommandMessage, SystemMessage, StatusMessage, MessageFormatError

client_id_prefix="a1b4182c-"

class Module:
    def __init__(self,module_name,requiredBusses: Iterable[BUS_TYPE]={}}):
        requiredBusses = requiredBusses|{BUS_TYPE.SYSTEM}
        self.StatusUP = StatusMessage(module_name,'UP')
        self.StatusDOWN = StatusMessage(module_name,'DOWN')
        self.module_name = module_name.strip().lower().replace(' ','')
        self.id = client_id_prefix+module_name
        
        self.mqtt = paho_client.Client(
            callback_api_version=paho_client.CallbackAPIVersion.VERSION2,
            client_id=self.id)
        
        self.mqtt.on_connect=self.mqtt_connect_callback
        self.mqtt.on_message=self.mqtt_message_callback
        
        self.mqtt.will_set(
            topic=topicFromBus(BUS_TYPE.STATUS),
            payload=self.StatusDOWN.serialize(),
        )
        self.busIO = BusIO(requiredBusses,self.mqtt)
        self.busIO.set_COMMAND_callback(self.command_callback)
        self.busIO.set_PANIC_callback(self.system_callback)
        
        self.mapTopics(requiredBusses)
        
        self.log = Logger(module_name,self.busIO.send_LOG)
    
    def mapTopics(self,busses:Iterable[BUS_TYPE])->None:
        self.topics = [ (topicFromBus(bus),0) for bus in busses]
    
    def connect(self):
        self.mqtt.connect('localhost',keepalive=5)
    
    def mqtt_connect_callback(self,client, userdata, connect_flags, reason_code, properties):
        self.log.info('Connected')
        self.busIO.send_STATUS(self.StatusUP)
        self.mqtt.subscribe(self.topics)

    def mqtt_message_callback(self,client, userdata, message):
        bus = busFromTopic(message.topic)
        payload:str = message.payload.decode()
        try:
            self.busIO.handleMessage(bus,payload)
        except MessageFormatError as x:
            self.log.error(x.message)
    
    def system_callback(self, msg:SystemMessage):
        if msg.command == "PANIC":
            self.log.error('Got a PANIC. Aborting')
            exit(1)
        if msg.dest != self.module_name and msg.dest != '*':
            return
        match msg.command:
            case 'KILL':
                self.log.info('got kill command, shutting down')
                exit(0)

    def start(self,loopForever: bool=False):
        if loopForever:
            self.mqtt.loop_forever()
        else:
            self.mqtt.loop_start()
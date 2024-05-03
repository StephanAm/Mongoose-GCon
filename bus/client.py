from typing import Iterable
from paho.mqtt import client as paho_client
from .logger import Logger
from .bustypes import BUS_TYPE,topicFromBus, busFromTopic
from .busio import BusIO
from .payloads import System, Status, PayloadFormatError, SYSTEM_COMMAND
from ._module_status import STATUS
from config import loadConfig
client_id_prefix="a1b4182c-"

class BaseModule:
    def __init__(self,mongoose_id,requiredBusses: Iterable[BUS_TYPE]={}):
        self.run_loop:bool=False
        self.config = loadConfig(mongoose_id)
        requiredBusses = set(requiredBusses)|{BUS_TYPE.SYSTEM}
        self.StatusDOWN = Status(mongoose_id,STATUS.DOWN)
        self.mongoose_id = mongoose_id
        self.id = client_id_prefix+mongoose_id
        
        self.mqtt = paho_client.Client(
            callback_api_version=paho_client.CallbackAPIVersion.VERSION2,
            client_id=self.id)
        
        self.mqtt.on_connect=self.mqtt_connect_callback
        self.mqtt.on_message=self.mqtt_message_callback
        
        self.mqtt.will_set(
            topic=topicFromBus(BUS_TYPE.STATUS),
            payload=self.StatusDOWN.serialize(),
        )
        self.busIO = BusIO(mongoose_id,requiredBusses,self.mqtt)
        self.busIO.set_SYSTEM_callback(self.system_callback)
        self.mapTopics(requiredBusses)
        self.log = Logger(mongoose_id,self.busIO.send_LOG)
        self._status=STATUS.RUNNING
    
    def mapTopics(self,busses:Iterable[BUS_TYPE])->None:
        self.topics = [ (topicFromBus(bus),0) for bus in busses]
    
    def connect(self):
        self.mqtt.connect('localhost',keepalive=5)
    
    def mqtt_connect_callback(self,client, userdata, connect_flags, reason_code, properties):
        self.log.info('Connected')
        self.sendStatus()
        self.mqtt.subscribe(self.topics)

    def mqtt_message_callback(self,client, userdata, message):
        bus = busFromTopic(message.topic)
        payload:str = message.payload.decode()
        try:
            self.busIO.handleMessage(bus,payload)
        except PayloadFormatError as x:
            self.log.error(x.message)
        except Exception as x:
            self.log.exception(x)
    
    def system_callback(self, msg:System):
        if msg.command == SYSTEM_COMMAND.PANIC:
            self.log.error('Got a PANIC. Aborting')
            exit(1)

        if not (msg.dest == self.mongoose_id or msg.dest == '*'):
            return #message isn't for me
        self.log.info(f'got {msg.command}')
        match msg.command:
            case SYSTEM_COMMAND.KILL:
                self.log.info('got kill command, shutting down')
                self.run_loop=False
                self.mqtt.disconnect()
                exit(0)
                
            case SYSTEM_COMMAND.STATUS_UPDATE:
                self.sendStatus()
    
    def sendStatus(self):
        self.busIO.send_STATUS(Status(
            status=self._status,
            id=self.mongoose_id))


class Module(BaseModule):
    def start(self,loopForever: bool=False,start_up_status:STATUS=STATUS.RUNNING):
        self.run_loop=True
        self._status=start_up_status
        if loopForever:
            self.mqtt.loop_forever()
        else:
            self.mqtt.loop_start()

    def panic(self):
        self.busIO.send_SYSTEM(
            System(
                source=self.mongoose_id,
                dest='*',
                command=SYSTEM_COMMAND.PANIC
            )
        )

    def killAll(self):
        self.busIO.send_SYSTEM(
            System(
                source=self.mongoose_id,
                dest='*',
                command=SYSTEM_COMMAND.KILL,
            )
        )

    def stop(self):
        self.run_loop = False
        self.mqtt.loop_stop()


    def request_status(self):
        self.busIO.send_SYSTEM(System(
                self.mongoose_id,
                '*',
                SYSTEM_COMMAND.STATUS_UPDATE))

    def setStatus(self,status:STATUS):
        if status == self._status:
            return
        self._status=status
        self.sendStatus()
        




from .bustypes import BUS_TYPE
from .client import Module
from .busio import BusIO
from . import payloads as Payloads
import enum
from ._module_status import STATUS

class MONGOOSE_IDS(str,enum.Enum):
    GBUS_LOOGER="gbuslogger"
    DIAGNOSTIC="diagnostic"
    GBUS_SINK="gbusinterface"
    GBUS_SOURCE="gbussource"
    STATUS_MONITOR="statusmonitor"
    MAIN_WHIP="mainwhip"



class RunState(str,enum.Enum):
    STOPPED="STOPPED",
    PAUSED='PAUSED',
    RUNNING='RUNNING'
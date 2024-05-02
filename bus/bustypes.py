from enum import Enum

COMMAND_KILL="KILL"
STATUS_UP="UP"
STATUS_DOWN="DOWN"

class BUS_TYPE(Enum):
    # this is used internally by modules and can't be subscribed to.
    SYSTEM="system" 
    
    # used by module to indicate their liveness
    STATUS="status" 

    # used to send application-level commands between modules. 
    COMMAND="command" 

    # used to stream gcode from sources to sinks.
    # sinks are modules that handle gcodes. e.g simulators, interfaces etc
    # sources are modules that produce gcodes. e.g. realtime controllers and file readers.
    GBUS="gbus"

    # general status logging by modules
    LOG="log"


topic_root="/mongoose"
_topics=(
    f"{topic_root}/{BUS_TYPE.LOG.value}",
    f"{topic_root}/{BUS_TYPE.COMMAND.value}",
    f"{topic_root}/{BUS_TYPE.STATUS.value}",
    f"{topic_root}/{BUS_TYPE.SYSTEM.value}",
    f"{topic_root}/{BUS_TYPE.GBUS.value}",
)
_busses=(
    BUS_TYPE.LOG,
    BUS_TYPE.COMMAND,
    BUS_TYPE.STATUS,
    BUS_TYPE.SYSTEM,
    BUS_TYPE.GBUS
)
busToTopicLookup=dict(zip(_busses,_topics))
topicToBusLookup=dict(zip(_topics,_busses))

def topicFromBus(bus:BUS_TYPE):
    return busToTopicLookup[bus]

def busFromTopic(topic:str):
    try:
        return topicToBusLookup[topic]
    except KeyError:
        raise ValueError(f"'{topic}' does not represent a valid bus")

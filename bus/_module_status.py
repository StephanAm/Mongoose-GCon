
import enum as _enum
class STATUS(str,_enum.Enum):
    RUNNING="RUN"       # Mongoose is online and doing what it is supposed to do 
    PAUSED="PAUSE"      # Mongoose is online but it has temporarily suspended execution
    STOPPED="STOPPED"   # Mongoose is online and not processing anything. depening on the module it might need to be be re-initialized 
    DOWN="DOWN"         # Mongoose is dead, not even broken
    UNKNOWN="UNKNOWN"   # Used to indicated that we don't know the the status of a Mongoose. A mongoose can't actually be in this state

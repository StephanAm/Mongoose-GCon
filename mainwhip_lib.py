from pathlib import Path
from enum import Enum
from bus import RunState


class State():
    camfile:Path=None
    runState:RunState = RunState.STOPPED

    @property
    def isRunning(self):
        return self.runState==RunState.RUNNING
    
    @property
    def isPaused(self):
        return self.runState==RunState.PAUSED
    
    @property
    def isStopped(self):
        return self.runState==RunState.STOPPED
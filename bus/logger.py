from .messagedefinitions import LogMessage
dummyFunc = lambda x:...

class Logger:
    def __init__(self,module_name,sender,verbosity=3):
        self.verbosity=verbosity
        self.module_name=module_name
        self.sender=sender

        self.error=dummyFunc if verbosity < 1 else lambda m: self._log(m,1)
        self.warn=dummyFunc if verbosity < 2 else lambda m: self._log(m,2)
        self.info=dummyFunc if verbosity < 3 else lambda m: self._log(m,3)
        self.debug=dummyFunc if verbosity < 4 else lambda m: self._log(m,4)
        
    def _log(self,msg,l):
        self.sender(
            LogMessage(
                level=l,
                msg=msg,
                name=self.module_name
            )
        )    

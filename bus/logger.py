from .payloads import Log
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

    def exception(self,x: Exception):
        argstr = ", ".join(f"'{a}'" for a in x.args)
        self._log(f'{type(x).__name__}({argstr})',0)

    def _log(self,msg,l):
        self.sender(
            Log(
                level=l,
                msg=msg,
                name=self.module_name
            )
        )    

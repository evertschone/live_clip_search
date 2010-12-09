from LiveOSC import OSC
from OSC import CallbackManager as CallbackManagerBase

class CallbackManager(CallbackManagerBase):
    def __init__(self, logger, ignore_addresses = []):
        CallbackManagerBase.__init__(self)
        
        self._log = logger
        
    def dispatch(self, message):
        try:
            address = message[0]
            self.callbacks[address](message)
        except KeyError, e:
            if 'default' in self.callbacks and address not in ignore_addresses:
                self.callbacks['default'](address, message)
            else:
                self._log.debug("no callback available for %s" % address)

        except None, e:
            self._log.debug("Exception in ", address, " callback :", e)
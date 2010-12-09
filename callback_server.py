import RemixNet
import time

from callback_manager import CallbackManager
from threading import Thread

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
IGNORE_ADDRESSES = ["/live/master/meter", "/live/clip/meter"]

class CallbackServer(Thread):
    def __init__(self, logger, server_host = 'localhost', server_port = 9001, 
                 client_host = 'localhost', client_port = 9000):
        Thread.__init__(self)
        
        self._should_run = True
        
        self._callback_manager = CallbackManager(logger, IGNORE_ADDRESSES)
        self._callback_manager.add(self.callback_default, 'default')
        
        self._server = RemixNet.UDPServer(server_host, server_port)
        self._server.setCallbackManager(self._callback_manager)
        self._server.bind()
        
        self._udp_client = RemixNet.UDPClient(client_host, client_port)
        self._udp_client.open()
        
        self._osc_client = RemixNet.OSCClient(self._udp_client)        
        
        self._log = logger
        
    def callback_default(self, address, message):
        self._log.debug("default callback: %s\t%s" % (address, message))
        
    def quit(self):
        self._should_run = False
        
    def run(self):
        while self._should_run:
            self._server.processIncomingUDP()
            time.sleep(0.01)
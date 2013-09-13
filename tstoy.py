import threading
import logging
from irtoy import IrToy, IRTransmitError


logger = logging.getLogger('ControlApp')


class TSToy(IrToy):
    def __init__(self, serialDevice):
        super(TSToy, self).__init__(serialDevice=serialDevice)
        self.__lock = threading.Lock()

    def transmit(self, code):
        self.__lock.acquire()
        try:
            super(TSToy, self).transmit(code)
            logger.debug('IR Toy: handshake: %d bytecount: %d complete: %s'
                         % (self.handshake, self.byteCount, self.complete))
        except IRTransmitError:
            logger.debug('IR transmit error code: %s' % (code))

        self.__lock.release()

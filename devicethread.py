import json
import time
import logging
import threading
from collections import deque


logger = logging.getLogger('ControlApp')


class DeviceThread(threading.Thread):
    def __init__(self, jsondir, component, cmd_list, cmd_event, toy):
        threading.Thread.__init__(self)
        self.__cmd_list = deque(cmd_list)
        self.__cmd_event = cmd_event
        self.__toy = toy
        self.__run_cmds = True
        self.__name = component
        with open("%s/%s.json" % (jsondir, component), 'r') as inFile:
            self.__codes = json.load(inFile)

    def run(self):
        while self.__run_cmds:
            logger.debug("%s Waiting for a command event" % self.__name)
            self.__cmd_event.wait()  # Wait for device command to arrive
            while True:
                try:
                    cmdkey = self.__cmd_list.popleft()
                    if cmdkey == 'allclear':  # Quit if you get the allclear cmd
                        break
                    if cmdkey == 'Sleep':  # Allows me to enter a delay of 1 second
                        time.sleep(1)
                    else:
                        irCode = self.__codes[cmdkey]
                        if irCode:
                            logger.debug("%s Attempting to transmit %s." % (self.__name, cmdkey))
                            self.__toy.transmit(irCode)
                except IndexError:
                    break
            self.__cmd_event.clear()

    def stop(self):
        logger.debug("%s quiting." % self.__name)
        self.__run_cmds = False
        self.addCmd('allclear')

    def addCmd(self, cmdkey):
        logger.debug("%s firing %s." % (self.__name, cmdkey))
        self.__cmd_list.append(cmdkey)
        self.__cmd_event.set()

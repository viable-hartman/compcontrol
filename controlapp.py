#!/usr/bin/python

import os
import re
import sys
import json
import serial
import optparse
import logging
import threading
from tstoy import TSToy
from orderedset import OrderedSet
from devicethread import DeviceThread


def main():
    parser = optparse.OptionParser("usage %s [-h] -d /dev/ttyACMO -j \"./json/comp\"" % (__file__),
                                   add_help_option=True)
    parser.add_option('-d', '--device', action="store", type="string",
                      dest="device",
                      help="Enter IR Toy device path (e.g. /dev/ttyACM0).")
    parser.add_option('-j', '--jsondir', action="store", type="string",
                      dest="jsondir",
                      help="Enter the directory path where your component json files are stored.")
    (options, args) = parser.parse_args()

    deviceName = options.device
    jsondir = options.jsondir

    if not(deviceName or jsondir):
        print parser.usage
        exit(0)

    cDict = {}
    logger.info("Attempting to access %s" % deviceName)
    with serial.Serial(deviceName) as serialDevice:
        toy = TSToy(serialDevice)
        for infile in os.listdir(jsondir):
            component = os.path.basename(os.path.splitext(infile)[0])
            t = DeviceThread(jsondir, component, [], threading.Event(), toy)
            cDict[component] = t
            t.start()

        # Compile RegEx to match pocketsphinx_continuous output
        compre = re.compile("^\d{9}:")

        # Load our filter words
        json_data = open('./json/filterwords.json')
        data = json.load(json_data)
        setf = OrderedSet(data['filterwords'])
        json_data.close()

        # Load our action dictionary mapping file
        json_data = open('./json/actions.json')
        data = json.load(json_data)
        dictact = data['actions']
        json_data.close()

        logger.info("~~~~~~ Welcome %s ~~~~~~", os.environ['USER'])
        while True:
            line = sys.stdin.readline()
            line = line.strip(os.linesep)
            logger.debug("~~~~~~ %s ~~~~~~", line)
            if compre.match(line) is not None:
                setl = OrderedSet(line.split(" ")[1:])
                setc = setl - setf
                # Lookup matching command and send to standard out
                vcmd = " ".join(list(setc))
                if vcmd == 'quit':
                    break
                try:
                    # Get serial command from verbal command key
                    for cmd in dictact[vcmd].split("&"):
                        cmdlist = cmd.split(":")
                        while (cmdlist[2] > 0):
                            t = cDict[cmdlist[0]]
                            logger.debug("Calling Thread: %s with Command: %s" % (cmdlist[0], cmdlist[1]))
                            t.addCmd(cmdlist[1])
                            cmdlist[2] = cmdlist[2] - 1
                except:
                    pass
        logger.info("~~~~~~ Good Bye %s ~~~~~~", os.environ['USER'])

        # End all Threads.
        for c, t in cDict.iteritems():
            logger.debug("Stopping Component Thread: %s" % c)
            t.stop()
            t.join()

    logger.info("Goodbye")
    sys.exit(0)

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)
    #logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=FORMAT)
    logger = logging.getLogger('ControlApp')
    main()

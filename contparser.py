#!/usr/bin/env python

import sys
import os
import re
import json
#import pprint
from orderedset import OrderedSet

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

# Snoring or not?
snoremode = False
#pprint.pprint(dictact)
print("~~~~~~ Welcome %s ~~~~~~") % (os.environ['USER'])
while True:
    line = sys.stdin.readline()
    #line = line.rstrip(os.linesep)
    line = line.strip(os.linesep)
    print("~~~~~~ %s ~~~~~~") % (line)
    if compre.match(line) is not None:
        setl = OrderedSet(line.split(" ")[1:])
        setc = setl - setf
        # Lookup matching command and send to standard out
        cmd = " ".join(list(setc))
        if cmd == 'snore':
            print("Now in snore mode.  Will listen, but won't look up commands.")
            snoremode = True
        elif cmd == 'wake up' and snoremode:
            print("Resuming normal operations.")
            snoremode = False
        if not snoremode:
            if cmd == 'quit':
                break
            try:
                    print(dictact[cmd])
            except:
                pass
print("~~~~~~ Good Bye ~~~~~~")

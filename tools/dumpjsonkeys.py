#!/usr/bin/env python

import os
import json


indir='../usbirtoy/hackPump/hackpump/devices/components'

os.chdir(indir)
for infile in os.listdir("."):
    if infile.endswith(".json"):
        cntrl = os.path.basename(os.path.splitext(infile)[0])
        json_data = open(infile)
        data = json.load(json_data)
        for k in data:
            print("%s:%s" % (cntrl, k) )
        json_data.close()

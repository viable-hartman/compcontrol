#!/usr/bin/env python

import sys
import optparse
import subprocess


def main():
    parser = optparse.OptionParser("usage %s [-h] -t" % (__file__), add_help_option=True)
    parser.add_option('-t', '--test', action="store_true",
                      dest="test",
                      help="Set for verbal parser only test mode.")
    (options, args) = parser.parse_args()

    test = options.test

    devnull = open('/dev/null', 'w')
    p1 = subprocess.Popen(['/usr/local/cmusphinx/bin/pocketsphinx_continuous',
                           '-jsgf',
                           './jsgf/mediacontrol.gram'],
                          stdout=subprocess.PIPE, stderr=devnull)

    if test:
        p2 = subprocess.Popen(['./contparser.py'], stdin=p1.stdout)
    else:
        p2 = subprocess.Popen(['./controlapp.py',
                               '-d', '/dev/ttyACM0',
                               '-j', './json/comp'], stdin=p1.stdout)

    p1.stdout.close()
    #p2.stdout.close()
    retcode = p2.wait()
    p1.terminate()

    sys.exit(retcode)

if __name__ == '__main__':
    main()

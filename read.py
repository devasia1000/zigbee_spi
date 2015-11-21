#!/usr/bin/env python

'''
Reads Zigbee frames and turns LEDs on/off
'''

import sys
import signal
import argparse

from killerbee import *

packetcount = 0

# Command-line arguments
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-i', '--iface', '--dev', action='store', dest='devstring')
#parser.add_argument('-g', '--gps', '--ignore', action='append', dest='ignore')
parser.add_argument('-w', '--pcapfile', action='store')
parser.add_argument('-W', '--dsnafile', action='store')
parser.add_argument('-p', '--ppi', action='store_true')
parser.add_argument('-c', '-f', '--channel', action='store', type=int, default=None)
parser.add_argument('-n', '--count', action='store', type=int, default=-1)
parser.add_argument('-D', action='store_true', dest='showdev')
args = parser.parse_args()

if args.channel == None:
    print >>sys.stderr, "ERROR: Must specify a channel."
    sys.exit(1)

kb = KillerBee(device=args.devstring)
if not kb.is_valid_channel(args.channel):
    print >>sys.stderr, "ERROR: Must specify a valid IEEE 802.15.4 channel for the selected device."
    kb.close()
    sys.exit(1)
kb.set_channel(args.channel)
kb.sniffer_on()

print("zbdump: listening on \'{0}\', link-type DLT_IEEE802_15_4, capture size 127 bytes".format(kb.get_dev_info()[0]))

rf_freq_mhz = (args.channel - 10) * 5 + 2400
while args.count != packetcount:
    packet = kb.pnext()
    print packet

kb.sniffer_off()
kb.close()

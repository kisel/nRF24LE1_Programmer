#!/usr/bin/env python

import time
import serial
import argparse

epilog = '''
Programmer.py - Program to feed Intel HEX files produced by SDCC to the nRF24LE1 Arduino
programmer sketch.  Will optionally set the number of protected pages and disable read of
main memory block by SPI
'''

parser = argparse.ArgumentParser(description='Flash Intel HEX file to nRF24LE1', epilog=epilog)

parser.add_argument('--nupp', default=255,
    help='Number of write unprotected memory blocks (0 - 31) - 0xFF: All pages unprotected')
parser.add_argument('--rdismb', default=255,
    help='External read protect main memory block - 0x00 Protected, 0xFF Unprotected')
parser.add_argument('port', help='COM port with Arduino programmer')
parser.add_argument('ihx_file', help='Path to Intel HEX file')

args = parser.parse_args()

ser = serial.Serial(port=args.port, baudrate=57600)

f_ihx = open(args.ihx_file)

#Wait for Arduino reset
time.sleep(3)

# trigger start flashing operation
ser.write("\1")

while 'READY' not in ser.readline():
    pass
print('<< READY\n')

ser.write("GO {0} {1}\n".format(args.nupp, args.rdismb))

while 1:
    serial_line = ser.readline()
    print('<< ' + serial_line.strip())
    if 'OK' in serial_line:
        ihx_line = f_ihx.readline()
        print('>> ' + ihx_line.strip())
        ser.write(ihx_line)
    if "READY" in serial_line or "DONE" in serial_line:
        break

ser.close()
f_ihx.close()


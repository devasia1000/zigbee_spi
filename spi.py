#!/usr/bin/python
import spidev
import time
import sys
from time import sleep
import RPi.GPIO as GPIO

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)    

    spi = spidev.SpiDev()
    spi.open(0,0)
    return spi

def frame_write(spi, data):
    """
    Set /SEL = L to start writing to the frame buffer
    Format is | 011 reserved[4:0] |    PHR[7:0]     |   PSDU[7:0]    | ...
    Set /SEL = H to stop writing to the frame buffer
    """
    GPIO.output(40, False)
    sleep(0.01)

    cmd_byte = 0x60
    status = spi.xfer2([cmd_byte])   

    for byte in data:
        spi.xfer2([byte])
   
    print status
 
    GPIO.output(40, True)
    sleep(0.01)

def read_register(spi, address):
    """
    The register address is contained within address[5:0].
    We need to or with 0x80 to convert address to command byte
    """    
    GPIO.output(40, False)    
    sleep(0.01)

    cmd_byte = 0x80 | address
    empty_byte = 0x00

    status = spi.xfer2([cmd_byte])
    value = spi.xfer2([empty_byte])

    print ''.join('{:02x}'.format(x) for x in [int(status[0]), int(value[0])])   
    GPIO.output(40, True)    
    sleep(0.01)

    return value[0]

def write_register(spi, address, byte):
    GPIO.output(40, False)    

    cmd_byte = 0xC0 | address
    
    status = spi.xfer2([cmd_byte])
    empty = spi.xfer2([byte])

    GPIO.output(40, True)

def main(argv):
    spi = init()
    frame_write(spi, [0x02, 0x00, 0x48, 0xf4, 0x7b])
    value = read_register(spi, 0x02)
    print 'Got back value as', value
    write_register(spi, 0x02, value | 0x02)
    value = read_register(spi, 0x02)
    print 'Got back value as', value

if __name__ == "__main__":
    main(sys.argv)


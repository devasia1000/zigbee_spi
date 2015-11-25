#!/usr/bin/python
import spidev
import time
import sys
from time import sleep
import socket
import json

def init():
    spi = spidev.SpiDev()
    spi.open(0,0)

    # Choose channel
    write_register(spi, 0x08, 0x14)

    # Enable automatic FCS generation
    #write_register(spi, 0x04, 0x20)

    # Disable automatic FCS generation
    write_register(spi, 0x04, 0x00)

    # Enable all interrupts
    write_register(spi, 0x0e, 0xff)

    return spi

def frame_write(spi, data):
    """
    Set /SEL = L to start writing to the frame buffer
    Format is | 011 reserved[4:0] |    PHR[7:0]     |   PSDU[7:0]    | ...
    Set /SEL = H to stop writing to the frame buffer
    """
    # SRAM write starting from address 0x00
    cmd_byte = 0x60
    length = len(data)
    
    spi.xfer2([cmd_byte, length] + data) # append two arrays together

def read_register(spi, address):
    """
    The register address is contained within address[5:0].
    We need to or with 0x80 to convert address to command byte
    """    
    cmd_byte = 0x80 | address
    empty_byte = 0x00

    [status, value] = spi.xfer2([cmd_byte, empty_byte])
    
    return value

def write_register(spi, address, byte):
    cmd_byte = 0xC0 | address    
    [status, empty] = spi.xfer2([cmd_byte, byte])

def set_led_on(spi):
    print 'Going to turn LED on: '    

    frame_write(spi, [0xFF, 0xFF])
    print '\tStatus:', read_register(spi, 0x01)

    write_register(spi, 0x02, 0x03) # FORCE_TRX_OFF
    print '\tStatus:', read_register(spi, 0x01)

    write_register(spi, 0x02, 0x09) # PLL_ON (TX_ON)
    print '\tStatus:', read_register(spi, 0x01)

    write_register(spi, 0x02, 0x02) # TX_START
    print '\tStatus:', read_register(spi, 0x01)

    print '\tFinished sending'
    print '\tStatus after send:', read_register(spi, 0x01)

    print '\tIRQ status register:', read_register(spi, 0x0F), '(TRX_END should be enabled)'
    print '\tIRQ status register:', read_register(spi, 0x0F), '(TRX_END should be cleared)'

    print '#####################################################'    

def set_led_off(spi):
    print 'Going to turn LED off: '

    frame_write(spi, [0x01, 0x01])
    print '\tStatus:', read_register(spi, 0x01)

    write_register(spi, 0x02, 0x03) # FORCE_TRX_OFF
    print '\tStatus:', read_register(spi, 0x01)

    write_register(spi, 0x02, 0x09) # PLL_ON (TX_ON)
    print '\tStatus:', read_register(spi, 0x01)

    write_register(spi, 0x02, 0x02) # TX_START
    print '\tStatus:', read_register(spi, 0x01)

    print '\tFinished sending'
    print '\tStatus after send:', read_register(spi, 0x01)

    print '\tIRQ status register:', read_register(spi, 0x0F), '(TRX_END should be enabled)'
    print '\tIRQ status register:', read_register(spi, 0x0F), '(TRX_END should be cleared)'

    print '#####################################################'    

def main(argv):
    spi = init()
  
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('52.25.165.62', 80))
    print 'Connected to Samsung SmartThings endpoint'

    while True:

        message = client_socket.recv(4096)
        data = json.loads(message)

        led = data['display_name']
        value = data['value']

        print led, 'is', value
        if led == 'LED #1':
            if value == 'on':
                set_led_on(spi)
            if value == 'off':
                set_led_off(spi)
 
if __name__ == "__main__":
    main(sys.argv)


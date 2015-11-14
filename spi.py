#!/usr/bin/python
import spidev
import time
import sys
from time import sleep

def init():
    spi = spidev.SpiDev()
    spi.open(0,0)
    return spi

def frame_write(spi):
    """
    Set /SEL = L to start writing to the frame buffer
    Format is | 011 reserved[4:0] |    PHR[7:0]     |   PSDU[7:0]    | ...
    Set /SEL = H to stop writing to the frame buffer
    """
    # SRAM write starting from address 0x00
    cmd_byte = 0x40
    address = 0x00
    length = 0x05
   
    print spi.xfer2([cmd_byte, address, length, 0x02, 0x00, 0x27, 0x05, 0xE0])

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

def main(argv):
    spi = init()

    # Enable automatic FCS generation
    #write_register(spi, 0x04, 0x20)

    while True: 
        
        frame_write(spi)
        print 'Status:', read_register(spi, 0x01)

        write_register(spi, 0x02, 0x03) # FORCE_TRX_OFF
        print 'Status:', read_register(spi, 0x01)
        sleep(0.01)   

        write_register(spi, 0x02, 0x09) # PLL_ON (TX_ON)
        print 'Status:', read_register(spi, 0x01)
        sleep(0.01)

        write_register(spi, 0x02, 0x02) # TX_START
        print 'Status:', read_register(spi, 0x01)           
        sleep(0.01)        

        print 'Finished sending'
        print 'Status after send:', read_register(spi, 0x01) 

        print 'IRQ status register:', read_register(spi, 0x0F), '(TRX_END should be enabled)'
        print 'IRQ status register:', read_register(spi, 0x0F), '(TRX_END should be cleared)'

        print '#####################################################'

if __name__ == "__main__":
    main(sys.argv)


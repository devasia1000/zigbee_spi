#!/usr/bin/python
import spidev
import time
import sys
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
spi = spidev.SpiDev()
spi.open(0,0)

"""
Write the frame buffer data
"""
GPIO.output(40, True) # set /SEL = H
sleep(0.01)

GPIO.output(40, False) # set /SEL = L
sleep(0.01)

spi.xfer2([0x60])
spi.xfer2([0x00]) # write empty PHR

GPIO.output(40, True) # set /SEL = H
sleep(0.01)

"""
Set state to PLL_ON by writing 0x04 to register 0x02
"""
GPIO.output(40, False) # set /SEL = L
sleep(0.01)

spi.xfer2([0xC2])
spi.xfer2([0x04]) # write FORCE_PLL_ON

GPIO.output(40, True) # set /SEL = H
sleep(0.01)

"""
Write TX_START to TRX_CMD by writing 0x02 to register 0x02
"""
GPIO.output(40, False) # set /SEL = L
sleep(0.01)

spi.xfer2([0xC2])
spi.xfer2([0x02]) # write TX_START

GPIO.output(40, True) # set /SEL = H
sleep(0.01)

"""
Read state information from TRX_STATUS by reading register 0x01
"""
GPIO.output(40, False) # set /SEL = L
sleep(0.01)

spi.xfer2([0x81])
print spi.xfer2([0x00])

GPIO.output(40, True) # set /SEL = H
sleep(0.01)

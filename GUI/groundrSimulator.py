import time
#import busio
#import board
#import adafruit_rfm9x
#import RPi.GPIO as GPIO
#import adafruit_character_lcd.character_lcd as characterlcd
from datetime import datetime
#from digitalio import DigitalInOut, Direction, Pull
import csv
#import I2C_LCD_driver
from udp_server2 import udp_network


server = udp_network('127.0.0.1',5005)

# Continuous Program

pullData = open("grounddata.txt","r").read()
dataArray = pullData.split('\n')


prev_packnum = -1
for eachLine in dataArray:
    try:
        if len(eachLine)>1:
            packetnum, acceleration, orientation, temperature, pressure, altitude, latitude, longitude   = eachLine.split(' ')
            if(int(packetnum) > prev_packnum):
                print(eachLine)
                data = [packetnum, acceleration, altitude, longitude, latitude, temperature, orientation, pressure]
                server.encode_datagram_simple(data)
                server.send_encoded_datagram()
                prev_packnum = int(packetnum)
            else:
                print("OUT OF ORDER")
    except:
        #print("FAILED")
        f_u_python = 0

time.sleep(.5)

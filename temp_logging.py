import os
import glob
import time
import sys
import datetime
import urllib2
import RPi_I2C_driver
from time import *

baseURL = "https://api.thingspeak.com/update?api_key=BCQOBOXNDHS4L81T"
 
os.system('modprobe w1-gpio')
 
os.system('modprobe w1-therm')
 
base_dir = 'sys/bus/w1/devices/'
 
#beer temperature device location
beer_file = '/sys/bus/w1/devices/28-0414694e4eff/w1_slave'
 
#Determine beer temperature
def read_rawtemp_beer():
     f = open(beer_file,'r')
     lines = f.readlines()
     f.close
     return lines
 
def read_temp_beer():
     lines = read_rawtemp_beer()
     while lines[0].strip()[-3:] !='YES':
          time.sleep(0.2)
          lines = read_rawtemp_beer()
     equals_pos = lines[1].find('t=')
     if equals_pos !=-1:
          temp_string = lines[1][equals_pos+2:]
          temp_beer = float(temp_string)/1000.0
          return temp_beer

while True: #Loop

#Send Beer Temperature to Thingspeak
     beer_tempin = read_temp_beer()
     beer_tempin = (beer_tempin * 1.8) + 32

#Pull results together
     values = [datetime.datetime.now(), beer_tempin]
 
#Open Thingspeak channel and assign fields to temperatures
     j = urllib2.urlopen(baseURL + "&field1=%s" % (beer_tempin))

     mylcd = RPi_I2C_driver.lcd()
     mylcd.lcd_clear()
# test 2
     mylcd.lcd_display_string("RPi I2C test", 1)
     mylcd.lcd_display_string(" Custom chars", 2)

#Time to next loop
time.sleep(600)
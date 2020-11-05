#!/usr/bin/env python3

# https://learn.adafruit.com/adafruit-vl53l0x-micro-lidar-distance-sensor-breakout/python-circuitpython


import config
import random,subprocess,os,sys
import os.path
from os import path
import time


# Libraries used to i2c access, this is the distance sensor.
import board
import busio
import adafruit_vl53l0x



####### FUNCTIONS #########

def timestamp():
	# This function will return time stamp format MM/DD/YYYY HH:MM:SS+0000

	return time.strftime("%d %b %Y %H:%M:%S+0000",time.localtime())

def LogMe(msg):
	# This function writes line in the log file

	ts=timestamp()
	print('%s %s' % (ts,msg))

def getTID():
	# This function will generate transaction ID unique per photo taken
	return "TID"+time.strftime("%Y%d%m%H%M%S",time.localtime())


def read_sensor():

	# This function reads distance sensor data from i2c

        sensor = adafruit_vl53l0x.VL53L0X(i2c)
        return int(sensor.range)

def take_picture(tid):

	# This function takes picture and save it to queue folder
        fpic=config.queuedir+"/"+tid+".jpg"

        LogMe('%s Taking picture file is %s' % (tid,fpic))

        # Take picture

        subprocess.run(["/usr/bin/raspistill", "-q","20","-t","300","-o",fpic])




####### MAIN ########

# These variables are used to control when to process close person
ftrig=0
cttrig=0

LogMe('Started')

LogMe('Init i2c')
i2c = busio.I2C(board.SCL, board.SDA)

# Now we enter in infinite loop

while True:

        sensor = read_sensor()

        print("sensor=%s" % str(sensor))

        if sensor>=config.trig_dist_max:
                ftrig=0

        if ftrig==0:

                if sensor<config.trig_dist_max:

                        cttrig=cttrig+1
                        if cttrig>=config.maxtrig: ftrig=1

                else:
                        cttrig=0

        if ftrig==1:

                TID=getTID()
                LogMe('Range: %imm Trig TID=%s' % (sensor,TID))
                take_picture(TID)
                ftrig=2
                cttrig=0

        # This flag stops execution without CTRL+C
        # It avoids i2c crashes

        if path.exists(config.stopme):
                LogMe('Stop service requested.')
                os.remove(config.stopme)
                sys.exit(0)






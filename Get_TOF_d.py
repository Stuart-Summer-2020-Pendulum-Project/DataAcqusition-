#!/usr/bin/env python3
#
#

print("This program will print the distance to the ground and the time from start time")
print("Sample rate should be rapid")

import time 
import busio
import board
import adafruit_vl6180x as vl
import os 

# write a function that will iterate over output files to avoid overwriting data
def checkdir(f):
    i = 2
    if os.path.exists(f) == False:
        out = open(f, 'w+')
    else:
        while os.path.isfile(f) == True:
            f = 'TOF_Dat'+str(i)+'.txt'
            i = i+1
            os.path.isfile(f)
    out = f
    return out


# set up for data collection 
f = "TOF_Dat1.txt"
out = checkdir(f)
print("This experiment will write data to ", out)
data = open(out, 'w+')

# get experimental parameters from user
SPS = input("Enter samples per second: ")
#SPS = 200 
sinterval = 1/float(SPS)
ACQTIME = 1
notes = input ("Enter any short notes you would like to include in experiment log: ")

i2c = busio.I2C(board.SCL, board.SDA)

sensor = vl.VL6180X(i2c)

# log experiment
log = open("TOF_LOG.txt", 'a+')
log.write('\n'+ out + ',  ' + str(time.time()) + ', ' + time.asctime() + ', SPS:' +  SPS + ', notes:' + notes)
log.close()

print("Data acquisition beggining... ")

t0 = time.perf_counter()
while True:
	for i in range(int(SPS)):
		st = time.perf_counter()
		range_mm = sensor.range
		t = time.perf_counter() - t0
		data.write(str(range_mm) + ', ' + str(t) + '\n')	
		while (time.perf_counter() - st) < sinterval: 
			pass	

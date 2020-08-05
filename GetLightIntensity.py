#!/usr/bin/env python3
#
#
"""
This program is to pull the light intensity from the I2C sensor ADS1015. Pendulum will have light source, which will swing directly over the sensor.
"""

import time
from Adafruit import ADS1x15
import os
import matplotlib.pyplot as plt
import numpy as np

# write a function that will iterate over output files to avoid overwriting data
def checkdir(f):
	i = 2
	if os.path.exists(f) == False:
		out = open(f, 'w+')
	else:
		while os.path.isfile(f) == True:
			f = 'LightDat'+str(i)+'.txt'
			i = i+1
			os.path.isfile(f)
	out = f
	return out


# set up for data collection 
f = "LightDat.txt"
out = checkdir(f)
print("This experiment will write data to ", out)
data = open(out, 'w+')

# get experimental paramaters
SPS = input("Enter how many samples per second would you like to collect: ")
VRANGE = 4096
sinterval = 1/float(SPS)
ACQTIME = 1
notes = input("Enter any short notes for experiment log: ")

#open data collection
adc = ADS1x15()
adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=float(SPS))

print("Data acquisition beggining")
print()

t0 = time.perf_counter()
print("Data Acquisition has begun at: ",  time.asctime())

# log experiment
log = open("LOG.txt", 'a+')
log.write('\n'+ out + ',  ' + time.asctime() + ', SPS:' +  SPS + ', notes:' + notes)
log.close()

# Acquire data, write to output file
a = 0
#count = 0
while a == 0:
	#print(count)
	for i in range(int(SPS)):
		st = time.perf_counter()
		y = 0.001*adc.getLastConversionResults()
		t = time.perf_counter() - t0
		data.write(str(y) +', '+ str(t) +'\n')
		#count = count + 1
		while (time.perf_counter() - st) < sinterval:
			pass


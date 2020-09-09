#!/usr/bin/env python3
#
import board
import busio
import adafruit_fxos8700 as ada_fxos
import adafruit_fxas21002c as ada_fxas
import time
import os
import sys

# write a function that will iterate over output files to avoid overwriting data
def checkdir(f):
    i = 2
    if os.path.exists(f) == False:
        out = open(f, 'w+')
    else:
        while os.path.isfile(f) == True:
            f = '9DOF_Dat'+str(i)+'.txt'
            i = i+1
            os.path.isfile(f)
    out = f
    return out


# set up for data collection 
f = "9DOF_Dat1.txt"
out = checkdir(f)
print("\nThis experiment will write data to ", out)
data = open(out, 'w+')

i2c = busio.I2C(board.SCL, board.SDA)

fxos = ada_fxos.FXOS8700(i2c)
fxas = ada_fxas.FXAS21002C(i2c)

NARGS = 3 # arg 1 = scropt, arg 2= SPS, arg 3 = notes
args = list(sys.argv)
if len(args) != NARGS:
	print("Incorrect number of arguements given. SPS and notes for exp. log should be arguements 1 and 2. exiting...")
	sys.exit(0)
else:
	pass
try:
	float(args[1])
except ValueError:
	print("Command line arguement 1 must be numerical value to dictate number of samples per second. Arguement rejected. exiting...")
	sys.exit(0)

SPS = args[1]
VRANGE = 4096
sinterval = 1/float(SPS)
ACQTIME = 1
notes = args[2]

# log experiment
# row 2 will be numerical time so that i can calibrate with run on second pi
log = open("9DOF_LOG.txt", 'a+')
log.write('\n'+ out + ',  ' + str(time.time()) + ', ' + time.asctime() + ', SPS:' +  SPS + ', notes: ' + notes)
log.close()

# Acquire data, write to output file
a = 0
t0 = time.perf_counter()
print("Data acquisition has begun ...")
#count = 0
while a == 0:
	#print(count)
	for i in range(int(SPS)):
		st = time.perf_counter()
		acc = fxos.accelerometer
		gyr = fxas.gyroscope
		magn = fxos.magnetometer
		data.write(str(acc) + '; ' + str(gyr) + '; ' + str(magn) + '; ' + str(st - t0) + '\n')
		t = time.perf_counter() - t0
		#count = count + 1
		while (time.perf_counter() - st) < sinterval:
			pass
	


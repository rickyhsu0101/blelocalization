import sys
import signal
import serial
import thread
import time

def handler(signum, frame):
    exit(0)

def rt0():
	while(1):
		line = ser0.readline()
		if line.contains(","):
			print(line)
			data0.append(line.decode("utf-8"))

def rt1():
	while(1):
		line = ser1.readline()
		if line.contains(","):
			print(line)
			data1.append(line.decode("utf-8"))

def rt2():
	while(1):
		line = ser2.readline()
		if line.contains(","):
			print(line)
			data2.append(line.decode("utf-8"))

def rt3():
	while(1):
		line = ser3.readline()
		if line.contains(","):
			print(line)
			data3.append(line.decode("utf-8"))

data0 = []
data1 = []
data2 = []
data3 = []

DEVICE_LINUX = "/dev/ttyACM"
os = DEVICE_LINUX

if __name__ == "__main__":
	signal.signal(signal.SIGINT, handler)
	ser0 = serial.Serial('{}{}'.format(os, 0))
	ser1 = serial.Serial('{}{}'.format(os, 1))
	ser2 = serial.Serial('{}{}'.format(os, 2))
	ser3 = serial.Serial('{}{}'.format(os, 3))
	t0 = threading.Thread(None, rt0)
	t1 = threading.Thread(None, rt1)
	t2 = threading.Thread(None, rt2)
	t3 = threading.Thread(None, rt3)
	t0.start()
	t1.start()
	t2.start()
	t3.start()

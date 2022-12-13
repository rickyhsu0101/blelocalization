import sys
import signal
import serial
import _thread as thread
import threading

import time

from sklearnex import patch_sklearn
patch_sklearn()

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import math
import argparse, sys
import pandas as pd
from sklearn.svm import SVC

import matplotlib.pyplot as plt
import pickle
import numpy as np

min_v = [-100., -100.,  -97.]
sub_v = [57., 57., 54.]

def handler(signum, frame):
    exit(0)

def rt0():
    while(1):
        line = ser0.readline().decode("utf-8").strip()
        if "," in line:
            #print("0 " + line)
            sp = line.split(",")
            if len(data0[key[sp[1]]]) == 5:
                data0[key[sp[1]]].pop(0)
            data0[key[sp[1]]].append((float(sp[0])-min_v[key[sp[1]]]) / sub_v[key[sp[1]]])

def rt1():
    while(1):
        line = ser1.readline().decode("utf-8").strip()
        if "," in line:
            #print("1 " + line)
            sp = line.split(",")
            if len(data1[key[sp[1]]]) == 5:
                data1[key[sp[1]]].pop(0)
            data1[key[sp[1]]].append((float(sp[0])-min_v[key[sp[1]]]) / sub_v[key[sp[1]]])

def rt2():
    while(1):
        line = ser2.readline().decode("utf-8").strip()
        if "," in line:
            #print("2 " + line)
            sp = line.split(",")
            if len(data2[key[sp[1]]]) == 5:
                data2[key[sp[1]]].pop(0)
            data2[key[sp[1]]].append((float(sp[0])-min_v[key[sp[1]]]) / sub_v[key[sp[1]]])

def rt3():
    while(1):
        line= ser3.readline().decode("utf-8").strip()
        if "," in line:
            #print("3 " + line)
            sp = line.split(",")
            if len(data3[key[sp[1]]]) == 5:
                data3[key[sp[1]]].pop(0)
            data3[key[sp[1]]].append((float(sp[0])-min_v[key[sp[1]]]) / sub_v[key[sp[1]]])
key = {"2": 0, "26": 1, "80": 2}
data0 = [[], [], []]
data1 = [[], [], []]
data2 = [[], [], []]
data3 = [[], [], []]

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


    m = pickle.load(open("model_ori.sav", 'rb'))
    m2 = pickle.load(open("model.sav", 'rb'))
    read_data = False
    while(1):
        valid = True
        for i in range(3):
            if len(data0[i]) == 0 or len(data1[i]) == 0 or len(data2[i]) == 0 or len(data3[i]) == 0:
                valid = False
        if not read_data:
            orientation = input("Curr Orientation")
            read_data = True
        
        if valid:
            x = np.zeros(13)
            for i in range(3):
                x[0+i] = data0[i][-1]
                x[3+i] = data1[i][-1]
                x[6+i] = data2[i][-1]
                x[9+i] = data3[i][-1]
            print(x)
            x[12] = int(orientation.strip())
            o = m.predict(x.reshape(1,13))
            print("With Orientation: ")
            print(o)
            o = m2.predict(x[:12].reshape(1,12))
            print("Without Orientation: ")
            print(o)
            read_data = False
            print(o)
            print(np.argmax(o))
            
        time.sleep(1)  

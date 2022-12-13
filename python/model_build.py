import numpy as np
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


data = []
SCALE = 0.1
C_VAL = 1e-5
WITH = 0
def GetDataFromFile(file_name, artif):
    data = pd.read_csv("../data{}/".format(artif)+ file_name + "_data.csv", header = None).to_numpy()
    norm = pd.read_csv("../data{}/".format(artif)+ file_name + "_norm.csv", header = None).to_numpy()
    return data, norm
def ScaleDown(data_total, scale):
    data_size = data_total.shape[0]
    data = np.zeros((int(data_size*scale), 14))

    data_size_each = data_size// 100
    for i in range(100):
        curr_offset = int(data_size_each*i)
        curr_offset_add = int(data_size_each*(i+1))
        
        data[int(curr_offset*scale):int(curr_offset_add*scale)] = data_total[curr_offset: int(curr_offset+data_size_each*scale)]
    return data
def GetDataNew():
    data_total = pd.read_csv("../svm_1mil.csv", header = None).to_numpy()
    data_total = ScaleDown(data_total, SCALE)
    data_size = data_total.shape[0]
    data = np.zeros((int(0.8*data_size), 14))
    test = np.zeros((int(0.2*data_size), 14))

    data_size_each = data_size // 100
    for i in range(100):
        curr_offset = int(data_size_each*i)
        curr_offset_add = int(data_size_each*(i+1))
        
        data[int(curr_offset*0.8):int(curr_offset_add*0.8)] = data_total[curr_offset: int(curr_offset+data_size_each*0.8)]
        test[int(curr_offset*0.2):int(curr_offset_add*0.2)] = data_total[int(curr_offset+data_size_each*0.8):curr_offset_add]
    return data, test
def model(x, y):
    S = SVC(C = C_VAL, kernel ="linear", gamma = "auto", degree = 3)
    S.fit(x, y)
    return S
def turn_x_y(element):
    return (int(element/5), int(element % 5))
def within_x_loop(pred, x, actual):
    n = np.zeros(pred.shape)
    for i in range(pred.shape[0]):
        curr = turn_x_y(pred[i])
        act = turn_x_y(actual[i])
        if abs(curr[0] - act[0]) + abs(curr[1] - act[1]) <= x:
            n[i] = 1
    return n
def run():
    data, test = GetDataNew()
    # print(data[-1])
    # print(test[-1])
    # exit(0)
    #print("start model")\

    temp = np.zeros((data.shape[0], 5))
    temp_test =  np.zeros((test.shape[0], 5))
    temp[:,0] = data[:,2]
    temp[:,1] = data[:,5]
    temp[:,2] = data[:,8]
    temp[:,3] = data[:,11]
    temp[:,4] = data[:,12]
    S = model(temp, data[:,-1])
    temp_test[:,0] = test[:,2]
    temp_test[:,1] = test[:,5]
    temp_test[:,2] = test[:,8]
    temp_test[:,3] = test[:,11]
    temp_test[:,4] = test[:,12]
    #print(data.shape)
    
    #S = model(data[:,:13], data[:,-1])
    #pickle.dump(S, open("./model_ori_rssi_3.sav", 'wb'))
    #print("finish model")

    predict_labels = S.predict(temp_test)
    #predict_labels = S.predict(test[:, :13])
    
    #predict_labels = S.predict(data[:, :14]).reshape(25,4)
    #dict_labels = turn_x_y_vec(predict_labels)
    # print(predict_labels.shape)
    #print("predict:")
    actual_labels = test[:,-1]
    print ("C-val: {} Within: {} Scale: {} accuracy:".format(C_VAL, WITH, SCALE))

    #print(np.sum(predict_labels == actual_labels) / predict_labels.shape[0])
 
    n = within_x_loop(predict_labels, WITH, actual_labels)
    print(np.sum(n)/ n.shape[0])
    return np.sum(n)/ n.shape[0]

if __name__ == "__main__":
    C_VAL = 0.1
    SCALE = 0.1
    # run()
    # exit(0)
    data_scale = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
    c_values = [1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1]
    within = [0, 1]
    for w in within:
        WITH = w
        for c in c_values:
            C_VAL = c
            acc = []
            for s in data_scale:
                SCALE = s
                acc.append(run())
            plt.figure()
            x =np.array(data_scale)
            y = np.array(acc)
            plt.xlabel("Data Scale of 1 mil")
            plt.ylabel("Accuracy")
            plt.title("C-value: {} Within {} Square".format(C_VAL, WITH))
            plt.plot(x, y, color = 'blue')
            plt.savefig("results/c-{}-within-{}.png".format(C_VAL, WITH))
        


   





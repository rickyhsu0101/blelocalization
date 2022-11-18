import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import math
import argparse, sys
import pandas as pd
from sklearn.svm import SVC

data = []

def GetDataFromFile(file_name, artif):
    data = pd.read_csv("../data{}/".format(artif)+ file_name + "_data.csv", header = None).to_numpy()
    norm = pd.read_csv("../data{}/".format(artif)+ file_name + "_norm.csv", header = None).to_numpy()
    return data, norm

def model(x, y):
    S = SVC(C = 1, kernel ="linear", gamma = "auto", degree = 3)
    S.fit(x, y)
    return S
def turn_x_y(element):
    return (int(element/5), int(element % 5))
def within_x_loop(arr, x, lab):
    n = np.zeros(arr.shape)
    for i in range(arr.shape[0]):
        curr = turn_x_y(lab[i])
        for j in range(arr.shape[1]):
            element  = arr[i, j]
            if abs(curr[0] - element[0]) + abs(curr[1] - element[1]) <= x:
                n[i, j] = 1
    return n

if __name__ == "__main__":
    #GenerateDirection()
    parser = argparse.ArgumentParser()
    parser.add_argument("--directions", help="number of directions in the data")
    parser.add_argument("-d", "--train", required = True)
    parser.add_argument("-t", "--test", required = True)

    args = parser.parse_args()
    if args.directions is not None:
        num_directions = args.directions
    
    data, norm = GetDataFromFile(args.train, '_')
    data_test, _ = GetDataFromFile(args.test, '')

    data_test[:,:12] = data_test[:,:12] / norm.reshape((1,12))
    S = model(data[:,:14], data[:,-1])
    predict_labels = S.predict(data_test[:, :14]).reshape(4,1)
    #predict_labels = S.predict(data[:, :14]).reshape(25,4)
    turn_x_y_vec = np.vectorize(turn_x_y, otypes=[tuple])
    predict_labels = turn_x_y_vec(predict_labels)
    # print(predict_labels.shape)
    print("predict:")
    print(predict_labels)
    actual_labels = data[:,14]
    #print(actual_labels)
    #print(np.sum(predict_labels))
    #predict_labels = within_x_loop(predict_labels, 0, list(range(25)))
    predict_labels = within_x_loop(predict_labels,1, [8,1,15,19])
    print("actual:")
    print(np.array([(1, 3), (0, 1), (3, 0), (3, 3)], dtype=tuple).reshape((4,2)))
    print("correct labels:")
    print(predict_labels)
    print("percent correct:", np.sum(predict_labels) / predict_labels.shape[0])
    # predict_labels = within_x_loop(predict_labels, 2)
    # print(np.sum(predict_labels))


    #print(norm)




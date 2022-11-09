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
    S = SVC(C = 10, kernel ="poly", gamma = "auto", degree = 8)
    S.fit(x, y)
    return S

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
    S = model(data[:,:-1], data[:,-1])
    predict_labels = S.predict(data_test[:, :14])
    print(predict_labels)
    actual_labels = data_test[:,14]
    print(actual_labels)
    print(np.sum(predict_labels == actual_labels))
    #print(norm)




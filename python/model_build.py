import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import math
import argparse, sys
import pandas as pd
from sklearn.svm import SVC

data = []

def GetDataFromFile(file_name):
    data = pd.read_csv("../data/"+ file_name + "_data.csv", header = None).to_numpy()
    norm = pd.read_csv("../data/"+ file_name + "_norm.csv", header = None).to_numpy()
    return data, norm

def model(x, y):
    S = SVC(kernel ="linear", gamma = "auto")
    S.fit(x, y)
    return S

if __name__ == "__main__":
    #GenerateDirection()
    parser = argparse.ArgumentParser()
    parser.add_argument("--directions", help="number of directions in the data")
    parser.add_argument("-f", "--file_name", required = True)

    args = parser.parse_args()
    if args.directions is not None:
        num_directions = args.directions
    
    data, norm = GetDataFromFile(args.file_name)
    S = model(data[:,:-1], data[:,-1])
    print(S.predict(np.expand_dims(data[0,:14], axis = 0)))
    print(norm)




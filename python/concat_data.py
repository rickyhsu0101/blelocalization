import argparse, sys
import numpy as np
import pandas as pd
import math

num_directions = 4
def GetDataFromFile(file_names):
    x = []
    y = None
    ori = None
    for file_name in file_names:
        f = pd.read_csv('../data/' + file_name + '.csv')
        f = f.to_numpy()
        curr_data = f[:, :3]

        # first data
        if y is None:
            # labels
            y = f[:, 4]
            
            # orientation to cos sine (normalized)
            ori = np.ndarray(shape = (f.shape[0], 2))
            ori[:,0] = np.cos(f[:,3]*2*math.pi / num_directions)
            ori[:,1] = np.sin(f[:,3]*2*math.pi / num_directions)

            # set initial features RSSI
            x = curr_data
        else:

            # concatenate RSSI (different anchor)
            x = np.concatenate((x, curr_data), axis = 1)
    
    # attach orientation to RSSI data
    x = np.concatenate((x, ori), axis=1)

    # remove very small values 0
    x = np.around(x, decimals = 15)

    # attach x to y
    data = np.concatenate((x, y.reshape(f.shape[0], 1)), axis = 1)
    
    # normalize first 12 columns (normalize per column)
    norm = np.linalg.norm(data, axis = 0)[:12]
    
    return data, norm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--directions", help="number of directions in the data")
    parser.add_argument("-f", "--file_names", action ="append", help="datafile", required = True)
    parser.add_argument("-o", "--out_file", required = True)

    args = parser.parse_args()
    if args.directions is not None:
        num_directions = args.directions
    
    data,norm = GetDataFromFile(args.file_names)

    np.savetxt("../data/{}_data.csv".format(args.out_file), data, delimiter=",")
    np.savetxt("../data/{}_norm.csv".format(args.out_file), norm, delimiter=",")
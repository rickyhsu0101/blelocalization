import numpy as np
import random
if __name__ == '__main__':
    l = ["0-0-0", "0-4-1", "4-0-2", "4-4-3"]
    sensors = []
    # min_c = [100000,100000,100000]
    for pref in l:
        coords = []
        for suff in [".csv", "-2.csv"]:
            
            sample = [[],[],[]]
            channel_map = {2: 0, 26: 1, 80:2}
            f = open("../data__/" +pref+suff, 'r')
            line = f.readline().strip()
            c = [0,0,0]
            while line:
                #print(line)
                
                if line == 'DONE':
                    coords.append(sample)
                    sample = [[],[],[]]
                    # print(c)
                    
                    # min_c[0]= min(c[0], min_c[0])
                    # min_c[1]= min(c[1], min_c[1])
                    # min_c[2]= min(c[2], min_c[2])
                    c = [0,0,0]
                elif ',' in line:
                    cont = line.split(",")
                    if c[channel_map[int(cont[1])]] < 29:
                        sample[channel_map[int(cont[1])]].append(float(cont[0]))
                        c[channel_map[int(cont[1])]] += 1
               
                line = f.readline().strip()
            f.close()
        #print(coords)
        sensors.append(coords)
    array = np.asarray(sensors)
    print(array.shape)
    min_per = array.min(axis=3).min(axis=1).min(axis = 0)
    print(array.min(axis=3).min(axis=1).min(axis = 0))
    max_per = array.max(axis=3).max(axis=1).max(axis=0)
    print(array.max(axis=3).max(axis=1).max(axis=0))
    sub = max_per - min_per
    print(sub)
    array =  array.reshape(4,100,29,3)
    array = array- min_per
    array = array / sub
    array = array.reshape(4,100,3,29)
    print(array.shape)
   
    DATA_SIZE = 1000000

    farray = np.zeros((4,100,29**3, 3))
    
    for i in range(4):
        for j in range(100):
            for k in range(29):
                for l in range(29):
                    for m in range(29):
                        farray[i,j,k*29**2+l*29+m,0] = array[i,j,0,k]
                        farray[i,j,k*29**2+l*29+m,1] = array[i,j,1,l]
                        farray[i,j,k*29**2+l*29+m,2] = array[i,j,2,m]
    ffarray = np.zeros((DATA_SIZE, 14))
    print("DONE f array")
    # print(farray[3,99,29**3-1,:])
    # print(farray[3,99,29**3-15:,:])
  
    for i in range(100):
        s = set()
        while len(s) < DATA_SIZE//100:
            t = (random.randint(0,29**3-1),random.randint(0,29**3-1),random.randint(0,29**3-1),random.randint(0,29**3-1))
            if t not in s:
                ffarray[i*(DATA_SIZE//100)  + len(s), 0:3] = farray[0,i,t[0],:]
                ffarray[i*(DATA_SIZE//100) + len(s), 3:6] = farray[1,i,t[1],:]
                ffarray[i*(DATA_SIZE//100) + len(s), 6:9] = farray[2,i,t[2],:]
                ffarray[i*(DATA_SIZE//100)  + len(s), 9:12] = farray[3,i,t[3],:]
                ffarray[i*(DATA_SIZE//100)  + len(s), 12] = (i%4)/4
                ffarray[i*(DATA_SIZE//100)  + len(s), 13] = i//4
                s.add(t)


    print(ffarray.shape)
    print(ffarray[DATA_SIZE-16:])
    np.savetxt("svm.csv", ffarray, delimiter=",")


    

    
    # print(min_c )
    #print(array[0,0,0])
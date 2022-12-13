import numpy as np
import random

min_v = [-100, -100, -97]
sub_v = [57, 57, 54]
if __name__ == '__main__':
    l = ["0-0-0", "0-4-1", "4-0-2", "4-4-3"]
    data = dict()
    for p in l:
        data[p] = list()
    #sensors = []
    # min_c = [100000,100000,100000]
    for pref in l:
        #coords = []
        res = []
        for suff in [".csv", "-2.csv"]:
            
            sample = [[],[],[]]
            channel_map = {2: 0, 26: 1, 80:2}
            f = open("../data__/" +pref+suff, 'r')
            line = f.readline().strip()
            c = 0
            while line:
                #print(line)
                
                if line == 'DONE':
                    sample = [[],[],[]]
                    data[pref].append(res)
                    # a = np.array(res)
                    res = []
                    # np.savetxt("{}-{}.csv".format(pref, c), a, delimiter=",")
                    c += 1
                    # print(c)
                    
                    # min_c[0]= min(c[0], min_c[0])
                    # min_c[1]= min(c[1], min_c[1])
                    # min_c[2]= min(c[2], min_c[2])
                 
                elif ',' in line:
                    cont = line.split(",")
                    if len(sample[channel_map[int(cont[1])]]) == 5:
                        sample[channel_map[int(cont[1])]].pop(0)
                    
                    sample[channel_map[int(cont[1])]].append((float(cont[0])- min_v[channel_map[int(cont[1])]]) / sub_v[channel_map[int(cont[1])]])
                    
                    if len(sample[0]) == 5 and len(sample[1]) == 5 and len(sample[2]) == 5:
                        res.append(sample[0]+sample[1]+sample[2])
                    #c[channel_map[int(cont[1])]] += 1

               
                line = f.readline().strip()
            f.close()
            #print(c)
        #print(coords)
        #sensors.append(coords)
    
    total = []
    # print(data[l[0]][99][0])
    # exit(0)
    #file1 = open("total_data.csv", "a")
    DATA_SIZE = 1000000
    
    for i in range(100):
        s = set()
        while len(s) < DATA_SIZE // 100:
            t = (random.randint(0, len(data[l[0]][i])-1), random.randint(0, len(data[l[1]][i])-1), random.randint(0, len(data[l[2]][i])-1), random.randint(0, len(data[l[3]][i])-1))
            if t not in s:
                total.append(data[l[0]][i][t[0]] + data[l[1]][i][t[1]] + data[l[2]][i][t[2]]+data[l[3]][i][t[3]] + [int(i%4), int(i//4)])
                s.add(t)     
                        #exit(0)
        print(i)
    #file1.close()
    a = np.array(total)
    np.savetxt("data_set.csv", a, delimiter = ",")        

    
    # array = np.asarray(sensors)
    # print(array.shape)
    # min_per = array.min(axis=3).min(axis=1).min(axis = 0)
    # print(array.min(axis=3).min(axis=1).min(axis = 0))
    # max_per = array.max(axis=3).max(axis=1).max(axis=0)
    # print(array.max(axis=3).max(axis=1).max(axis=0))
    # sub = max_per - min_per
    # print(sub)
    # array =  array.reshape(4,100,29,3)
    # array = array- min_per
    # array = array / sub
    # array = array.reshape(4,100,3,29)
    # print(array.shape)
   
    # DATA_SIZE = 1000000

    # farray = np.zeros((4,100,29**3, 3))
    
    # for i in range(4):
    #     for j in range(100):
    #         for k in range(29):
    #             for l in range(29):
    #                 for m in range(29):
    #                     farray[i,j,k*29**2+l*29+m,0] = array[i,j,0,k]
    #                     farray[i,j,k*29**2+l*29+m,1] = array[i,j,1,l]
    #                     farray[i,j,k*29**2+l*29+m,2] = array[i,j,2,m]
    # ffarray = np.zeros((DATA_SIZE, 14))
    # print("DONE f array")
    # # print(farray[3,99,29**3-1,:])
    # # print(farray[3,99,29**3-15:,:])
  
    # for i in range(100):
    #     s = set()
    #     while len(s) < DATA_SIZE//100:
    #         t = (random.randint(0,29**3-1),random.randint(0,29**3-1),random.randint(0,29**3-1),random.randint(0,29**3-1))
    #         if t not in s:
    #             ffarray[i*(DATA_SIZE//100)  + len(s), 0:3] = farray[0,i,t[0],:]
    #             ffarray[i*(DATA_SIZE//100) + len(s), 3:6] = farray[1,i,t[1],:]
    #             ffarray[i*(DATA_SIZE//100) + len(s), 6:9] = farray[2,i,t[2],:]
    #             ffarray[i*(DATA_SIZE//100)  + len(s), 9:12] = farray[3,i,t[3],:]
    #             ffarray[i*(DATA_SIZE//100)  + len(s), 12] = (i%4)/4
    #             ffarray[i*(DATA_SIZE//100)  + len(s), 13] = i//4
    #             s.add(t)


    # print(ffarray.shape)
    # print(ffarray[DATA_SIZE-16:])
    # np.savetxt("svm.csv", ffarray, delimiter=",")

  
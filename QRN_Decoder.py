# coding: utf-8

# In[1]:

#all the import statements are here. 
import numpy as np
import pandas as pd
import json


# In[2]:

#raw_data = None
#bin_data = None
#data = None
def load_data(file):
    raw_data  = np.fromfile(file, dtype='uint8')
    print("bytes loaded: {0}".format(len(raw_data)))
    bin_data = raw_data.reshape(int(raw_data.shape[0]/(32)),32)
    #bin_data = raw_data
    print("Number of data frames: {0}".format(bin_data.shape[0]) )
    #bin_data = raw_data.reshape(7,38)
    #bin_data= bin_data[:,0:-3].flatten()
    #bin_data = bin_data[:,1:-2].flatten()
    #bin_data = bin_data[:,1:-2][0] #just checking with one 245 byte frame
    #bin_data = bin_data.reshape(int(bin_data.shape[0]/32),6)
    print("Number of event packets: {0}".format(bin_data.shape[0]) )
    np.savetxt('_byte_data.csv', bin_data, delimiter=',')   # X is an array

    return bin_data
#data = load_data("out.bin")          
#S1_1_n          
    


# In[3]:

##print in hex
#vhex = np.vectorize(hex)
#vhex(bin_data)

def process(infile,outfile):
    print("loading:",infile)
    bin_data =  load_data(infile)



process("/home/xueliang/git/CSP-Codebase-v2.9.1-master/QRN_3","out_QRN.csv")




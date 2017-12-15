import argparse

import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Plot data from SPEQS data file.')
parser.add_argument('--filename', type=str, 
        help='Name of SPEQS file to process')

args = parser.parse_args()


offset = 0
header = 1
crc = 2

data = np.memmap(args.filename, mode='r', offset=offset)
print (len(data))

tot_len = len(data)/241

# frames are 241 bytes long
data = data.reshape(-1, 241)

# remove header and crc
data = data[:,header:-crc]

dt = np.dtype([('0', '>u4'), ('1', '>u4'), ('2', '>u2'), ('3', '>u4'), ('4', '>u4'), ('5', '>u2'), ('6', '>u2'), ('7', '>u2'), ('8', '>u2'), ('9', '>u1'), ('10', '>u2'), ('11', '>u1'), ('frame_cnt', '>u2'), ('16', '>u2')])


data2 = data.reshape(tot_len*7, 34).view(dt)

print (len(data))
data3 = np.reshape(data,(tot_len*7,34))
np.savetxt('stuff.txt',data3, fmt='%d')

col0 = []
col1 = []
col2 = []
col3 = []
col4 = []
col5 = []
col6 = []
col7 = []
col8 = []
col9 = []
col10 = []
col11 = []
col15 = []

for i in range(len(data2)):
	col0.append(data2[i][0][0])
	col1.append(data2[i][0][1])
	col2.append(data2[i][0][2]) 
	col3.append(data2[i][0][3])
	col4.append(data2[i][0][4])
	col5.append(data2[i][0][5])
	col6.append(data2[i][0][6])
	col7.append(data2[i][0][7] & 0x3ff)
	col8.append((data2[i][0][8] & 0xffc0) >> 6)
	col9.append(((data2[i][0][8] & 0x01f) << 5) + ((data2[i][0][9] & 0xfe) >> 3))
	col10.append(((data2[i][0][9] & 0x03) << 8) + ((data2[i][0][10] & 0xff00) >> 8))
	col11.append(((data2[i][0][10] & 0x03) << 8) + ((data2[i][0][11])))

	col15.append(data2[i][0][-2])


col0 = np.array(col0)
col1 = np.array(col1)
col2 = np.array(col2)
col3 = np.array(col3)
col4 = np.array(col4)
col5 = np.array(col5)
col6 = np.array(col6)
col7 = np.array(col7)
col8 = np.array(col8)
col9 = np.array(col9)
col10 = np.array(col10)
col11 = np.array(col11)
col15 = np.array(col15)

#np.savetxt('stuff.txt',(col0, col1, col3,col4,col5,col6,col7,col8,col9,col10,col11,col15))

'''
plt.plot(col0)
plt.plot(col1)
plt.plot(col2)
plt.plot(col3)
plt.plot(col4)
plt.plot(col5)
plt.plot(col6)
plt.plot(col7)
plt.plot(col8)
plt.plot(col9)
plt.plot(col10)
plt.plot(col11)
plt.plot(col15)

plt.show()
'''

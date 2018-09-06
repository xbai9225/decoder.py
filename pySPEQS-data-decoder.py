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
    #global raw_data
    #global bin_data
    #global data
    raw_data  = np.fromfile(file, dtype='uint8')
    print("bytes loaded: {0}".format(len(raw_data)))
    bin_data = raw_data.reshape(int(raw_data.shape[0]/(255)),255)
    #bin_data = raw_data
    print("Number of data frames: {0}".format(bin_data.shape[0]) )
    #bin_data = raw_data.reshape(7,38)
    #bin_data= bin_data[:,0:-3].flatten()
    bin_data = bin_data[:,1:-2].flatten()
    #bin_data = bin_data[:,1:-2][0] #just checking with one 245 byte frame
    bin_data = bin_data.reshape(int(bin_data.shape[0]/36),36)
    print("Number of event packets: {0}".format(bin_data.shape[0]) )
    #tdf = pd.DataFrame(bin_data)
    #tdf.to_csv("_byte_data.csv")
    #data = bin_data
    np.savetxt('_byte_data.csv', bin_data, delimiter=',')   # X is an array
    #return bin_data
    return bin_data
#data = load_data("out.bin")          
#S1_1_n          
    


# In[3]:

##print in hex
vhex = np.vectorize(hex)
#vhex(bin_data)


# In[4]:

#helper function
def create_word(barr):
    h = 0
    for b in reversed(barr):
        h = h << 8
        h = h | b
    #print (hex(h) )
    return h
    
def get_val(h, bitmask, r_shift ):
    val = (h&bitmask) >>r_shift
    return val


# In[5]:

#w = create_word(bin_data[1,0:3])


# In[6]:

#vhex(get_val(w,0xFFFFF,0) )


# In[7]:

def extract_column(data, begin_byte, end_byte,pattern, right_shift):
    warr = map(create_word,data[:,begin_byte:end_byte])
    r = [get_val(w,pattern,right_shift) for  w in warr]

    return r


# In[8]:

#def exp_code(hdata):


# In[9]:

def APD1Top(data):
    return extract_column(data,0,3,0xFFFFF,0)
#vhex(APD1Top(bin_data))


# In[10]:

def APD2Top(data):
    return extract_column(data,2,5,0xFFFFF0,4)
#vhex(APD2Top(bin_data))


# In[11]:

def APD1Bot(data):
    return extract_column(data,5,8,0xFFFFF,0)
#vhex(APD1Bot(bin_data))


# In[12]:

def APD2Bot(data):
    return extract_column(data,7,10,0xFFFFF0,4)
#vhex(APD2Bot(bin_data))


# In[13]:

def coinc(data):
    return extract_column(data,10,13,0xFFFF,0)
#vhex(coinc(bin_data))


# In[14]:

def APD_DAC1(data):
    return extract_column(data,12,15,0xFFF,0)
#vhex(APD_DAC1(bin_data))


# In[15]:

def APD_DAC2(data):
    return extract_column(data,12,15,0xFFF000,12)
#vhex(APD_DAC2(bin_data))


# In[16]:

def thermistors_x_5(data):
    return data[:,16:21]

#vhex(thermistors_x_5(bin_data) )


# In[17]:

def Laser_DAC(data):
    return extract_column(data,21,23,0xFFF,0)
#vhex(Laser_DAC(bin_data))


# In[18]:

def LCPR_cap_pf(data):
    return extract_column(data,23,25,(0xFFF<<2),2)
#vhex(LCPR_cap_pf(bin_data))


# In[19]:

def LCPR_ref_i(data):
    return extract_column(data,23,25,0x3,0)
##vhex(LCPR_ref_i(bin_data))


# In[20]:

def LCPR_1(data):
    return extract_column(data,25,27,0xFFFF,0)
#vhex(LCPR_1(bin_data))


# In[21]:

def LCPR_2(data):
    return extract_column(data,27,29,0xFFFF,0)
#vhex(LCPR_2(bin_data))


# In[22]:

def LEPD_current(data,index):
    MSB8 = data[:,29+index].tolist()
    LSB2 = [ ((x >> (index*2)) & 3) for x in  data[:,29+4] ]
    
    return [x*4+y for (x,y) in zip (MSB8,LSB2)]
        
    

#vhex(LEPD_current(data,3))


# In[23]:

#def LEPD_total(data):
#    return extract_column(data,29,33,(0x3FF<<22),22)
#vhex(LEPD_total(bin_data))


# In[24]:

#def LEPD_dX(data):
#    return extract_column(data,29,33,(0x7FF<<11),11)
#vhex(LEPD_dX(bin_data))


# In[25]:

#def LEPD_dY(data):
#    return extract_column(data,29,33,(0x7FF),0)
#vhex(LEPD_dY(bin_data))


# In[26]:

def get_index(data):
    return extract_column(data,34,36,(0xFFFF),0)
#vhex(get_index(bin_data))


# In[32]:

def process(infile,outfile):
    print("loading:",infile)
    bin_data =  load_data(infile)
    COLUMN_NAMES = ["APDTop1","APDTop2","APDBot1","APDBot2",
                "Coincidence","APD_DAC1","APD_DAC2","T1",
                "T2","T3","T4","T5","Laser_DAC","LCPR_cap_pf",
                "LCPR_ref_i","LCPR_1","LCPR_2","LEPDc_0",
                "LEPDc_1","LEPDc_2","LEPDc_3","Index"]
    df = pd.DataFrame(columns=COLUMN_NAMES)
    
    ind_list = get_index(bin_data)
    heater_begin = 14
    heater_end = ind_list[heater_begin:].index(0) + heater_begin
    
    data = bin_data[heater_end:]
    #data = bin_data
    df["APDTop1"] = APD1Top(data)
    df["APDTop2"] = APD2Top(data)
    df["APDBot1"] = APD1Bot(data)
    df["APDBot2"] = APD2Bot(data)
    df["Coincidence"] = coinc(data)
    df["APD_DAC1"] = APD_DAC1(data)
    df["APD_DAC2"] = APD_DAC2(data)
    T = thermistors_x_5(data)
    df["T1"] = T[:,0].astype(int) *4
    df["T2"] = T[:,1].astype(int) *4
    df["T3"] = T[:,2].astype(int) *4
    df["T4"] = T[:,3].astype(int) *4
    df["T5"] = T[:,4].astype(int) *4
    df["Laser_DAC"] = Laser_DAC(data)
    df["LCPR_cap_pf"] = LCPR_cap_pf(data)
    df["LCPR_ref_i"] = LCPR_ref_i(data)
    df["LCPR_1"] = LCPR_1(data)
    df["LCPR_2"] = LCPR_2(data)
    
    df["LEPDc_0"] = LEPD_current(data,0)
    df["LEPDc_1"] = LEPD_current(data,1)
    df["LEPDc_2"] = LEPD_current(data,2)
    df["LEPDc_3"] = LEPD_current(data,3)
    
    #df["LEPD_total"] = LEPD_total(data)
    #df["LEPD_dX"] = LEPD_dX(data)
    #df["LEPD_dY"] = LEPD_dY(data)
    df["Index"] = get_index(data)
    df = df.drop_duplicates() # 
    df = df[df.Index !=65535  ]
    
    df.to_csv(outfile)
    print("output written to:",outfile)


# In[33]:

def get_heating_data(infile, outfile): #("data/heater-test/S12_1_n","out_S12.csv")
    bin_data = load_data(infile)
    #df = pd.DataFrame(columns=COLUMN_NAMES)
    data = bin_data
    ind_list = get_index(data)
    heater_begin = 14
    heater_end = ind_list[heater_begin:].index(0) + heater_begin
    
    hdata = data[heater_begin:heater_end].astype(dtype='uint16') *4
    
    np.savetxt(outfile, hdata, delimiter=",")
    #print(hdata)
    
    #print (heater_begin,heater_end)
    #print( ind_list [heater_end])
    #print (ind_list)
    


# In[34]:

def decode_profile_data(p):
    d = {}
    
    d['obc_exp_code'] = p[1]
    d['e_heat_high'] = p[2]
    
    d['heatHigh_timeout'] = create_word(p[4:2:-1])
    d['TEMP_SetPt'] = create_word(p[6:4:-1])
    d['DarkCountMode_TimeOut'] = create_word(p[8:6:-1])
    d['LCPR_cap_ref_index'] = p[9]
    d['LD_Cons_Current_Mode'] = create_word(p[11:9:-1])
    d['Experiment_Time']  = create_word(p[13:11:-1])
    d['QRNG_mode'] = p[14]  # implement check for qrng mdode vs. qrng profile
    
    
        
    
    #d['LCPR_cap_ref_index'] = p[31]  #  repeat? 
    d['LCPR_step_size'] = p[31]
    d['Count_send_interval'] = p[32]
    d['OPAMP1_DC_Offset'] = create_word(p[34:32:-1])
    d['OPAMP2_DC_Offset'] = create_word(p[36:34:-1])
    
    for key in d :
        d[key] = int(d[key])
    
    
    d['LCPR_1_Buf'] = [0,0,0,0]
    d['LCPR_2_Buf'] = [0,0,0,0]
    
    for i in range(0,4):
        d['LCPR_1_Buf'][i] = int(create_word(p[(16+2*i):(14+2*i):-1]))
        d['LCPR_2_Buf'][i] = int(create_word(p[(8+16+2*i):(8+14+2*i):-1]))
    

    
    return d
    
    


# In[35]:

def get_profile_data(infile,outfile):
    profile_dd = {} #profile data dictionary
    bin_data = load_data(infile)
    #df = pd.DataFrame(columns=COLUMN_NAMES)
    pp = np.append(bin_data[0,:],bin_data[1,0:3]) #previous profile
    #print (pp)
    dpp = decode_profile_data(pp)
    #print (dpp)
    profile_dd["previous_profile"] = dpp
    cp = np.append(bin_data[7,:],bin_data[8,0:3]) #current profile
    dcp = decode_profile_data(cp)
    #print (dcp)
    profile_dd["current_profile"] = dcp
    with open(outfile,"w") as fp:
        json.dump(profile_dd, fp,indent=4, sort_keys=True)

    
#get_profile_data("/home/xueliang/git/CSP-Codebase-v2.9.1-master/S1_30_n", "prof_s130.json")


# In[36]:

#process("/home/xueliang/git/CSP-Codebase-v2.9.1-master/S1_30_n","out_S1_30_n.csv")
process("/home/xueliang/git/CSP-Codebase-v2.9.1-master/QRN_3","out_QRN.csv")
#process("out.bin","out_dummy.csv")
#get_heating_data("data/S4_1_n","heat_S41.csv")


# In[ ]:


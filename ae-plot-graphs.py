#ae-plot-EC-HE-CR-TC-TL-FC.py
'''
# ae-txt-summary.py
# created by mahemys; 2019.08.14
# !perfect, but works!
# MIT; no license; free to use!
# update 2019.08.14; initial review
# update 2019.09.01; optimise
# 
#------------------------------------------------------------
# read acoustic emission ID2RawFile.txt initial summary file and plot charts
#------------------------------------------------------------
# 1 >> EnergyChannel      >> ID2RawFile.txt
# 2 >> HistoricEnergyTime >> ID2RawFile.txt
# 3 >> Correlation        >> ID2RawFile.txt
# 4 >> ASLTimeChan        >> ID2RawFile.txt
# 5 >> ASLTimeLine        >> ID2RawFile.txt
# 6 >> ASLTimeLine_2Part  >> ID2RawFile.txt
# 7 >> FrequencyCentroid  >> ID2RawFile.txt
#------------------------------------------------------------
EnergyChannel.png
- Energy vs Channel
- ASL(dB) vs Channel

FrequencyCentroid.png
- Frequency Centroid (kHz)

HistoricEnergyTime.png
- Energy vs Time(Sec)
- Amplitude (db) vs Time(Sec)

ASLTimeChan.png
- ASL(dB) vs Time(Sec)
- ASL(dB) vs Channel

ASLTimeLine.png
- ASL Time Line per Channel view

ASLTimeLine_2Part.png
- ASL Time Line 2 Part view

Correlation.png
- Energy vs Amplitude(dB) vs Hits
- Duration vs Amplitude(dB) vs Hits
#------------------------------------------------------------
'''

import gc
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from datetime import datetime

dt_start = datetime.now()
print(dt_start, 'start...')

try:
    #TextFilePath, TextFileName
    File_dir = os.path.dirname(__file__)
    TextFileName = 'Tank_Category.txt'
    TextFilePath = os.path.join(File_dir, TextFileName)
    #Tank_Category.txt
    ta,tb,tc,td,te,tf,tg,th,ti,tj,tk,tl,tm,tn,to,tp,tq,tr,ts,tt = np.loadtxt(TextFilePath, delimiter=',', unpack=True, dtype='str')
except:
    print('Exception:', TextFileName)
    pass

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(20,10))

try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass

try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
ENERGY VS CHANNEL'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=10, color='b')
except:
    print('Exception: #suptitle')
    pass

try:
    import pandas as pd
    
    #read file in chunks, append and create df, exclude non datastring
    chunklist = []
    chunksize = 100000
    for chunk in  pd.read_csv('ID2RawFile.txt', sep=',', header=None, skiprows=1, skip_blank_lines=True, low_memory=False, chunksize=chunksize):
        chunklist.append(chunk)
    df = pd.concat(chunklist, axis= 0).dropna()
    del chunklist
    #add header to df
    header_array =  ['Hit','Channel','DayTime','Energy','Duration','Amplitude','ASL','FRQC']
    df.columns = header_array
    #print(df.info())
    print(df.head())
    print(df.shape)
    
    if 'Channel' in df.columns:
        #CH is present in column
        #df = df.astype(float)
        
        #print('col_list, col_max...')
        col_list = list(df)                         #column list
        col_max  = len(df.columns)                  #column count
        print('col_list        ', col_list)
        print('col_max         ', col_max)
        
        CH_min = df.min(axis=0)['Channel']          #column CH min
        CH_max = df.max(axis=0)['Channel']          #column CH max
        #CH always integer
        CH_min = int(CH_min)
        CH_max = int(CH_max)
        #print('CH_min          ', CH_min)
        #print('CH_max          ', CH_max)
        #CH always starts from 1
        if CH_min > 1:
            CH_min = 1
        
        #find missing channel using difference of two lists...
        CH_unique = df['Channel'].unique().tolist()
        print('CH_unique       ', len(CH_unique), CH_unique)
        
        CH_count_total   = CH_max
        CH_count_present = len(CH_unique)
        CH_count_missing = (CH_count_total - CH_count_present)
        print('CH_count_total  ', CH_count_total)
        print('CH_count_present', CH_count_present)
        print('CH_count_missing', CH_count_missing)
        print('wait... find shape, sum for each channel')
    
    #create multiple df for each channel...
    df_CH      = {}
    
    #find shape, sum for each channel using for loop...
    for i in range(CH_min, (CH_max + 1), 1):
        #print('rows with CH['+str(i)+']...')
        df_CH[i] = df[df['Channel'] == i]                   #rows with CH_1...
        #print(df_CH[i])
        #print(df_CH[i].info())
        #print(df_CH[i].head())
        
        col = df_CH[i].iloc[:, 3:col_max]                   #Energy to last column
        #print(col)
        
        #if channel is missing, create df, append and pass values as nan, CH as i
        if not i in CH_unique:
            data = pd.DataFrame(index=range(0,1), columns=df.columns)
            df_CH[i] = df_CH[i].append(data)
            #df_CH[i]['Channel'] = df_CH[i].fillna(value=0, inplace=True)
            df_CH[i]['Channel'] = df_CH[i]['Channel'].fillna(i)
            #print(df_CH[i].head())
        
    #SensorNumber, TotalHits, TotalEnergy, TotalAmplitude, TotalASL
    #Hit,Channel,DayTime,Energy,Duration,Amplitude,ASL,FRQC
    CH_SensorNumber     = []
    CH_TotalHits        = []
    CH_TotalEnergy      = []
    CH_TotalAmplitude   = []
    CH_TotalASL         = []
    
    for i in range(CH_min, (CH_max + 1), 1):
        if i in CH_unique:
            #print('CH_exists ', i)
            CH_TotalHits.append(df_CH[i]['Hit'].shape[0])
            CH_TotalEnergy.append(df_CH[i]['Energy'].sum())
            CH_TotalAmplitude.append(df_CH[i]['Amplitude'].sum())
            CH_TotalASL.append(df_CH[i]['ASL'].sum())
        else:
            print('CH_missing', i)
            CH_TotalHits.append(0)
            CH_TotalEnergy.append(0)
            CH_TotalAmplitude.append(0)
            CH_TotalASL.append(0)
        CH_SensorNumber.append(i)
    #print('CH_SensorNumber  ', CH_SensorNumber)
    #print('CH_TotalHits     ', CH_TotalHits)
    #print('CH_TotalEnergy   ', CH_TotalEnergy)
    #print('CH_TotalAmplitude', CH_TotalAmplitude)
    #print('CH_TotalASL      ', CH_TotalASL)
except:
    print('Exception: #read file in chunks')
    pass

try:
    #list to array, Sensor_Data...
    #sa,ss,st,su,sv
    #sa #SensorNumber
    #ss #TotalHits
    #st #TotalEnergy
    #su #TotalAmplitude
    #sv #TotalASL
    sa = np.array(CH_SensorNumber)
    ss = np.array(CH_TotalHits)
    st = np.array(CH_TotalEnergy)
    su = np.array(CH_TotalAmplitude)
    sv = np.array(CH_TotalASL)
    #print('SensorNumber     ', sa)
    #print('TotalHits        ', ss)
    #print('TotalEnergy      ', st)
    #print('TotalAmplitude   ', su)
    #print('TotalASL         ', sv)
except:
    print('Exception: #list to array, Sensor_Data...')
    pass

try:
    #list to array, ID2RawFile...
    #Hit,Channel,DayTime,Energy,Duration,Amplitude,ASL,FRQC
    #a,b,c,d,e,f,g,h
    print('list to array, ID2RawFile...')
    a = np.array(df['Hit'])
    b = np.array(df['Channel'])
    c = np.array(df['DayTime'])
    d = np.array(df['Energy'])
    e = np.array(df['Duration'])
    f = np.array(df['Amplitude'])
    g = np.array(df['ASL'])
    h = np.array(df['FRQC'])
    print('a = {}\nb = {}\nc = {}\nd = {}\ne = {}\nf = {}\ng = {}\nh = {}'\
          .format(len(a), len(b), len(c), len(d), len(e), len(f), len(g), len(h)))
except:
    print('Exception: #list to array, ID2RawFile...')
    pass

try:
    print('drop df...')
    df.drop(df.index, inplace=True)
    print(df.head())

    for i in range(CH_min, (CH_max + 1), 1):
        df_CH[i].drop(df_CH[i].index, inplace=True)
        #print(df_CH[i].head())
except:
    print('Exception: #drop df...')
    pass

try:
    print('gc.collect...')
    gc.collect()
except:
    print('Exception: #gc.collect...')
    pass


try:
    MulVal = 0.2 #default
    #Bar thickness depending on Channels max(sa)
    if (max(sa)) <= 5:#Less than or equal to 5
        MulVal = 0.1
        #print(max(sa), MulVal)
    elif (max(sa)) <= 10:#Less than or equal to 10
        MulVal = 0.2
        #print(max(sa), MulVal)        
    elif (max(sa)) <= 20:#Less than or equal to 20
        MulVal = 0.25
        #print(max(sa), MulVal)
    elif (max(sa)) > 20:#More than 20
        MulVal = 0.3
        #print(max(sa), MulVal)
except:
    print('Exception: #Bar thickness')
    pass

#Bar >> X-Channels >> Y-Energy
plt.subplot(2, 1, 1) #Top Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Threshold
    values = st #Total Energy
    #colors = ['b', 'c', 'y', 'r']
    colors = ['b', 'c', 'g', 'y', 'r']
    split = st.max() / len(colors)
    threshold1 = split * 1
    threshold2 = split * 2
    threshold3 = split * 3
    threshold4 = split * 4
    threshold5 = split * 5
    
    #Split 5 colors
    below_threshold1 = np.minimum(values, threshold1)
    ZF1 = below_threshold1
    
    below_threshold2 = np.minimum(values - below_threshold1, threshold2 - threshold1)
    ZF2 = below_threshold2
    
    below_threshold3 = np.minimum(values - below_threshold1 - below_threshold2, threshold3 - threshold2)
    ZF3 = below_threshold3
    
    below_threshold4 = np.minimum(values - below_threshold1 - below_threshold2 - below_threshold3, threshold4 - threshold3)
    ZF4 = below_threshold4

    below_threshold5 = np.minimum(values - below_threshold1 - below_threshold2 - below_threshold3 - below_threshold4, threshold5 - threshold4)
    ZF5 = below_threshold5
    
    #Plot >> Bar, Red
    #plt.bar(sa, st, color='r', label='Energy', width = 0.3, alpha=0.25)
    plt.bar(sa, below_threshold1, color=colors[0], width = MulVal, alpha=1)
    plt.bar(sa, below_threshold2, color=colors[1], width = MulVal, alpha=1, bottom=threshold1)
    plt.bar(sa, below_threshold3, color=colors[2], width = MulVal, alpha=1, bottom=threshold2)
    plt.bar(sa, below_threshold4, color=colors[3], width = MulVal, alpha=1, bottom=threshold3)
    plt.bar(sa, below_threshold5, color=colors[4], width = MulVal, alpha=1, bottom=threshold4)
    plt.xticks(np.arange(min(sa), max(sa)+1, 1.0)) #Force Ticks Increment Value
except:
    print('Exception: #Top Half Plot')
    pass

try:
    #Details
    #plt.xlabel('Channels')
    plt.ylabel('Energy')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('Energy vs Channel <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(sa), np.amax(sa)))
except:
    print('Exception: #Title')
    pass



#Color bar
try:
    ax2 = fig.add_axes([0.91, 0.11, 0.01, 0.77])#Top to Bottom position >> x,y,width,height
    #ax2 = fig.add_axes([0.91, 0.25, 0.01, 0.5])#Middle position >> x,y,width,height
    cmap = mpl.colors.ListedColormap(['b', 'c', 'g', 'y', 'r'])
    bounds = [0, 20, 40, 60, 80, 100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm)
    cb2.set_label('Percentage (%)')#rotation=90
except:
    print('Exception: #Color bar')
    pass


#Scatter >> X-Channels >> Y-ASL(dB)
plt.subplot(2, 1, 2) #Bottom Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)


try:
    #Threshold 5 colors
    values = sv #Total ASL
    #colors = ['b', 'c', 'y', 'r']
    colors = ['b', 'c', 'g', 'y', 'r']
    split = sv.max() / len(colors)
    threshold1 = split * 1
    threshold2 = split * 2
    threshold3 = split * 3
    threshold4 = split * 4
    threshold5 = split * 5
     
    #Split
    below_threshold1 = np.minimum(values, threshold1)
    ZF1 = below_threshold1
    
    below_threshold2 = np.minimum(values - below_threshold1, threshold2 - threshold1)
    ZF2 = below_threshold2
    
    below_threshold3 = np.minimum(values - below_threshold1 - below_threshold2, threshold3 - threshold2)
    ZF3 = below_threshold3
    
    below_threshold4 = np.minimum(values - below_threshold1 - below_threshold2 - below_threshold3, threshold4 - threshold3)
    ZF4 = below_threshold4
    
    below_threshold5 = np.minimum(values - below_threshold1 - below_threshold2 - below_threshold3 - below_threshold4, threshold5 - threshold4)
    ZF5 = below_threshold5
    
    #Plot >> Bar, Red
    #plt.bar(sa, st, color='r', label='Energy', width = 0.3, alpha=0.25)
    plt.bar(sa, below_threshold1, color=colors[0], width = MulVal, alpha=1)
    plt.bar(sa, below_threshold2, color=colors[1], width = MulVal, alpha=1, bottom=threshold1)
    plt.bar(sa, below_threshold3, color=colors[2], width = MulVal, alpha=1, bottom=threshold2)
    plt.bar(sa, below_threshold4, color=colors[3], width = MulVal, alpha=1, bottom=threshold3)
    plt.bar(sa, below_threshold5, color=colors[4], width = MulVal, alpha=1, bottom=threshold4)
    plt.xticks(np.arange(min(sa), max(sa)+1, 1.0)) #Force Ticks Increment Value
except:
    print('Exception: #Bottom Half Plot')
    pass


try:
    #Details
    plt.xlabel('Channels')
    plt.ylabel('ASL(dB)')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('ASL(dB) vs Channel <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(sa), np.amax(sa)))
except:
    print('Exception: #Title')
    pass


try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'EnergyChannel.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
    print('Complete: #Save image', File_name)
except:
    print('Exception: #Save image', File_name)
    pass


#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('ENERGY VS CHANNEL')

#plt.show()
plt.close('all')


dt_stop = datetime.now()
dt_diff_1 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_1))
dt_start = datetime.now()
print(dt_start, 'start...')



#HistoricEnergyTime
#HISTORIC ENERGY VS TIME
#Test-Historic_1
#Test-Historic_1.pyw

#HISTORIC_1.pyw
#2D-EnergyAmpTime_Plot
#HISTORIC
#Energy vs Time(sec) <All Channels>
#Amplitude(dB) vs Time(sec) <All Channels>

import os
import matplotlib.pyplot as plt
import numpy as np

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(20,10))

try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass


try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
HISTORIC ENERGY VS TIME'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=10, color='b') 
except:
    print('Exception: #suptitle')
    pass

#Bar >> X-Time(sec) >> Y-Energy
plt.subplot(2, 1, 1) #Top Half Plot

try:
    #Plot >> Bar, Red
    #plt.bar(c, d, color='r', label='Energy', width = 5, alpha=0.5)

    #Plot >> Scatter, Red
    #plot = plt.scatter(c, d, color='r', marker='s', s=10, edgecolor='none', alpha=1)

    #Plot >> Scatter, color
    plot = plt.scatter(c, d, c=b, cmap='hsv', marker='s', s=10, edgecolor='none', alpha=1)
    plt.colorbar(plot, label='Channels')
except:
    print('Exception: #Plot >> Scatter, color')
    pass


#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Details
    #plt.xlabel('Time(sec)')
    plt.ylabel('Energy')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('Energy vs Time(sec) <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
except:
    print('Exception: #Title')
    pass


#Scatter >> X-Time(sec) >> Y-Amplitude(dB)
plt.subplot(2, 1, 2) #Bottom Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Plot >> c=Time, f=Amplitude, b=Channels
    #plot = plt.scatter(c, f, color='r', label='Amplitude(dB)', marker='s', s=10, edgecolor='none', alpha=1)
    plot = plt.scatter(c, f, c=b, cmap='hsv', marker='s', s=10, edgecolor='none', alpha=1)
    plt.colorbar(plot, label='Channels')
    plt.yticks(np.arange(40, 105, 5)) #Force Ticks Increment Value
except:
    print('Exception: #Bottom Half Plot')
    pass


try:
    #Details
    plt.xlabel('Time(sec)')
    plt.ylabel('Amplitude(dB)')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('Amplitude(dB) vs Time(sec) <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
except:
    print('Exception: #Title')
    pass


try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'HistoricEnergyTime.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
    print('Complete: #Save image', File_name)
except:
    print('Exception: #Save image', File_name)
    pass


#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('HISTORIC ENERGY VS TIME')

#plt.show()
plt.close('all')


dt_stop = datetime.now()
dt_diff_2 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_2))
dt_start = datetime.now()
print(dt_start, 'start...')


''
#Correlation
#CORRELATION
#Test-Correlation
#Test-Correlation.pyw

#CORRELATION.pyw
#2D-DurEnerAmpHits_Plot
#CORRELATION PLOT
#Energy vs Amplitude(dB) vs Hits <All Channels>
#Duration(µs) vs Amplitude(dB) vs Hits <All Channels>

import os
import matplotlib.pyplot as plt
import numpy as np

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(20,10))

''
try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass


try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
CORRELATION'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=10, color='b')
except:
    print('Exception: #suptitle')
    pass

# Hits >> Line Number

#Scatter >> X-Amplitude(dB) >> Y-Energy
plt.subplot(1, 2, 1) #Left Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Plot >> Energy vs Amp
    #plt.scatter(f, d, color='r', label='Energy', marker='s', s=10, alpha=0.5)
    plot = plt.scatter(f, d, c=a, cmap='hsv', marker='s', s=15, edgecolor='none', alpha=1)
    plt.colorbar(plot, label='Hits')
    plt.xticks(np.arange(40, 105, 5)) #Force Ticks Increment Value
    plt.yscale('log')
    plt.ylim(pow(10,0))
except:
    print('Exception: #Left Half Plot')
    pass

try:
    #Details
    plt.xlabel('Amplitude(dB)')
    plt.ylabel('Energy')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('Energy vs Amplitude(dB) vs Hits <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
except:
    print('Exception: #Title')
    pass


#Scatter >> X-Amplitude(dB) >> Y-Duration(µs)
plt.subplot(1, 2, 2) #Right Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Plot >> Dur vs Amp
    #plt.scatter(e, f, color='r', label='Duration(µs)', marker='s', s=10, alpha=0.5)
    plot = plt.scatter(f, e, c=a, cmap='hsv', marker='s', s=15, edgecolor='none', alpha=1)
    plt.colorbar(plot, label='Hits')
    plt.xticks(np.arange(40, 105, 5)) #Force Ticks Increment Value
    plt.yscale('log')
    plt.ylim(pow(10,0))
except:
    print('Exception: #Right Half Plot')
    pass

try:    
    #Details
    plt.xlabel('Amplitude(dB)')
    plt.ylabel('Duration(µs)')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('Duration(µs) vs Amplitude(dB) vs Hits <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
except:
    print('Exception: #Title')
    pass

try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'Correlation.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
    print('Complete: #Save image', File_name)
except:
    print('Exception: #Save image', File_name)
    pass


#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('CORRELATION')

#plt.show()
plt.close('all')


dt_stop = datetime.now()
dt_diff_3 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_3))
dt_start = datetime.now()
print(dt_start, 'start...')



#ASLTimeChan
#ASL VS TIME & CHAN
#Test-Historic_2
#Test-Historic_2.pyw

#HISTORIC_2.pyw
#2D-DurAslTime_Plot
#HISTORIC - DUR ASL TIME
#ASL(dB) vs Time(sec) <All Channels>
#Duration(µs) vs Time(sec) <All Channels>

import os
import matplotlib.pyplot as plt
import numpy as np

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(20,10))

''
try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass

try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
ASL VS TIME & CHAN'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=10, color='b') 
except:
    print('Exception: #suptitle')
    pass

#Bar >> X-Time(sec) >> Y-ASL(dB)
plt.subplot(2, 1, 1) #Top Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Plot
    #plt.bar(c, g, color='r', label='ASL(dB)', width=5, alpha=0.5)
    #plt.scatter(c, g, color='r', label='ASL(dB)', marker='s', s=10, edgecolor='none', alpha=1)
    plot = plt.scatter(c, g, c=b, cmap='hsv', marker='s', s=10, edgecolor='none', alpha=1)
    plt.colorbar(plot, label='Channels')
except:
    print('Exception: #Top Half Plot')
    pass

try:
    #Details
    #plt.xlabel('Time(sec)')
    plt.ylabel('ASL(dB)')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('ASL(dB) vs Time(sec) <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
    #plt.title('<{:.0f}-{:.0f}>'.format(np.amin(f), np.amax(f)))
except:
    print('Exception: #Title')
    pass


#Scatter >> X-Time(sec) >> Y-Duration(µs)
plt.subplot(2, 1, 2) #Bottom Half Plot

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #Plot
    #plt.scatter(c, e, color='r', label='Duration(µs)', marker='s', s=10, edgecolor='none', alpha=1)
    plot = plt.scatter(b, g, c=f, cmap='hsv', marker='s', s=10, edgecolor='none', alpha=1)
    plt.colorbar(plot, label='Amplitude')
    plt.xticks(np.arange(min(b), max(b)+1, 1.0)) #Force Ticks Increment Value
    #plt.yscale('log')
except:
    print('Exception: #Bottom Half Plot')
    pass

try:
    #Details
    plt.xlabel('Channels')
    plt.ylabel('ASL(dB)')
    #plt.legend(loc='best')#Shows label, Best Location
    plt.title('ASL(dB) vs Channel <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
except:
    print('Exception: #Title')
    pass

try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'ASLTimeChan.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
    print('Complete: #Save image', File_name)
except:
    print('Exception: #Save image', File_name)
    pass

#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('ASL VS TIME & CHAN')

#plt.show()
plt.close('all')


dt_stop = datetime.now()
dt_diff_4 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_4))
dt_start = datetime.now()
print(dt_start, 'start...')


#ASLTimeLine
#ASL VS TIME LINE
#Test-AslPerChannel
#Test-AslPerChannel.pyw

#ASLPERCHANNEL.pyw
#2D-AslTime_Plot
#ASL PER CHANNEL - ASL TIME
#ASL(dB) per Channel vs Time(sec) <All Channels>

import os
import matplotlib.pyplot as plt
import numpy as np

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(27,18))

try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass

try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
ASL VS TIME LINE'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=16, color='b')#FontSize
except:
    print('Exception: #suptitle')
    pass

#pandas dataframe
import pandas as pd
import numpy as np

colors = ['magenta', 'orange', 'y', 'c', 'lime', 'teal', 'cyan', 'gold', 'purple', 'violet', \
          'indigo', 'brown', 'red', 'green', 'blue', 'black', 'lightblue', 'tan', 'pink'] # 19 colors

try:
    #Check Channels are even or odd, add 1 if odd >> as it is read from raw data.
    #replace max(b) with Channels
    Channels = int(max(b))
    if Channels % 2 == 0:
        Channels = Channels + 0
        #print('Even # ', Channels)
    else:
        Channels = Channels + 1
        #print('Odd # ', Channels)
except:
    print('Exception: #Channels >> Even or Odd')
    pass

try:
    #Half >> Left >> 1 to 9
    for j in range(1, int(Channels/2)+1):  #channel #splint by 2 sections
        #print('ch', j)
        for k in range(j, j+1):#int(max(sa)/2)+1):#channel 1,2,3,4....
            plt.subplot(Channels/2, 2, j)
            #pass read values to dataframe >> B = Channel, C = DayTime, G = ASL
            df = pd.DataFrame({'B': b, 'C': c, 'G': g})
            #print(df)
    
            B_1 = df.loc[df['B'] == j]
            #print(B_1)
    
            df = pd.DataFrame(B_1, columns=['C', 'G'])
            cc = pd.DataFrame(B_1, columns=['C'])#pass data daytime
            gg = pd.DataFrame(B_1, columns=['G'])#pass data asl
            #Plot >> c=Time, g=Asl, b=Channels
            plt.plot(cc, gg, label='Channel %s' %(j), linewidth = 1.0, linestyle = '-', color=colors[j-1], alpha=1)
        #Grid
        plt.yticks(np.arange(15, 100, 20)) #Force Ticks Increment Value
        #plt.minorticks_on()
        plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
        plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.25)
        #Details
        plt.legend(loc='best')#Shows label, Best Location
except:
    print('Exception: #Half >> Left >> 1 to 9')
    pass

try:
    #Half >> Right >> 10 to 18
    for j in range(int(Channels/2)+1, int(Channels)+1):#channel #splint by 2 sections
        #print('ch', j)
        for k in range(j, j+1):#int(max(sa)/2)+1):#channel 10,11,12,13....
            plt.subplot(Channels/2, 2, j)# - int(max(sa)/2))
            #pass read values to dataframe >> B = Channel, C = DayTime, G = ASL
            df = pd.DataFrame({'B': b, 'C': c, 'G': g})
            #print(df)
    
            B_1 = df.loc[df['B'] == j]
            #print(B_1)
    
            df = pd.DataFrame(B_1, columns=['C', 'G'])
            cc = pd.DataFrame(B_1, columns=['C'])#pass data daytime
            gg = pd.DataFrame(B_1, columns=['G'])#pass data asl
            #Plot >> c=Time, g=Asl, b=Channels
            plt.plot(cc, gg, label='Channel %s' %(j), linewidth = 1.0, linestyle = '-',color=colors[(j-1)-int(Channels/2)], alpha=1)
        #Grid
        plt.yticks(np.arange(15, 100, 20)) #Force Ticks Increment Value
        #plt.minorticks_on()
        plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
        plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.25)
        #Details
        plt.legend(loc='best')#Shows label, Best Location
except:
    print('Exception: #Half >> Right >> 10 to 18')
    pass

try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'ASLTimeLine.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
    print('Complete: #Save image', File_name)
except:
    print('Exception: #Save image', File_name)
    pass

#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('ASL VS TIME LINE')

#plt.show()
plt.close('all')


dt_stop = datetime.now()
dt_diff_5 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_5))
dt_start = datetime.now()
print(dt_start, 'start...')


#ASLTimeLine_2Part
#ASLTimeLine
#ASL VS TIME LINE
#Test-AslPerChannel
#Test-AslPerChannel.pyw

#ASLPERCHANNEL.pyw
#2D-AslTime_Plot
#ASL PER CHANNEL - ASL TIME
#ASL(dB) per Channel vs Time(sec) <All Channels>

import os
import matplotlib.pyplot as plt
import numpy as np

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(20,10))

try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass

try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
ASL VS TIME LINE - 2 PART'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=10, color='b')#FontSize
except:
    print('Exception: #suptitle')
    pass

#pandas dataframe
import pandas as pd
import numpy as np

colors = ['magenta', 'orange', 'y', 'c', 'lime', 'teal', 'cyan', 'gold', 'purple', 'violet', \
          'indigo', 'brown', 'red', 'green', 'blue', 'black', 'lightblue', 'tan', 'pink'] # 19 colors

try:
    #Check Channels are even or odd, add 1 if odd >> as it is read from raw data.
    #replace max(b) with Channels
    Channels = int(max(b))
    if Channels % 2 == 0:
        Channels = Channels + 0
        #print('Even # ', Channels)
    else:
        Channels = Channels + 1
        #print('Odd # ', Channels)
except:
    print('Exception: #Channels >> Even or Odd')
    pass

try:
    plt.subplot(2, 1, 1) #Top Half Plot
    #Half >> Left >> 1 to 9
    for j in range(1, int(Channels/2)+1):  #channel #split by 2 sections
        #print('ch', j)
        for k in range(j, j+1):#int(max(sa)/2)+1):#channel 1,2,3,4....
            #plt.subplot(max(b)/2, 2, j)
            #pass read values to dataframe >> B = Channel, C = DayTime, G = ASL
            df = pd.DataFrame({'B': b, 'C': c, 'G': g})
            #print(df)
    
            B_1 = df.loc[df['B'] == j]
            #print(B_1)
    
            df = pd.DataFrame(B_1, columns=['C', 'G'])
            cc = pd.DataFrame(B_1, columns=['C'])#pass data daytime
            gg = pd.DataFrame(B_1, columns=['G'])#pass data asl
            #Plot >> c=Time, g=Asl, b=Channels
            plt.plot(cc, gg, label='Channel %s' %(j), linewidth = 1.0, linestyle = '-', color=colors[j-1], alpha=1)
        #Grid
        plt.yticks(np.arange(15, 100, 10)) #Force Ticks Increment Value
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
        plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.25)
        #Details
        plt.legend(loc='best')#Shows label, Best Location
except:
    print('Exception: #Half >> Left >> 1 to 9')
    pass

try:
    plt.subplot(2, 1, 2) #Bottom Half Plot
    #Half >> Right >> 10 to 18
    for j in range(int(Channels/2)+1, int(Channels)+1):#channel #split by 2 sections
        #print('ch', j)
        for k in range(j, j+1):#int(max(sa)/2)+1):#channel 10,11,12,13....
            #plt.subplot(max(b)/2, 2, j)# - int(max(sa)/2))
            #pass read values to dataframe >> B = Channel, C = DayTime, G = ASL
            df = pd.DataFrame({'B': b, 'C': c, 'G': g})
            #print(df)
    
            B_1 = df.loc[df['B'] == j]
            #print(B_1)
    
            df = pd.DataFrame(B_1, columns=['C', 'G'])
            cc = pd.DataFrame(B_1, columns=['C'])#pass data daytime
            gg = pd.DataFrame(B_1, columns=['G'])#pass data asl
            #Plot >> c=Time, g=Asl, b=Channels
            plt.plot(cc, gg, label='Channel %s' %(j), linewidth = 1.0, linestyle = '-',color=colors[(j-1)-int(Channels/2)], alpha=1)
        #Grid
        plt.yticks(np.arange(15, 100, 10)) #Force Ticks Increment Value
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
        plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.25)
        #Details
        plt.legend(loc='best')#Shows label, Best Location
except:
    print('Exception: #Half >> Right >> 10 to 18')
    pass

try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'ASLTimeLine_2Part.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
    print('Complete: #Save image', File_name)
except:
    print('Exception: #Save image', File_name)
    pass

#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('ASL VS TIME LINE')

#plt.show()
plt.close('all')


dt_stop = datetime.now()
dt_diff_6 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_6))
dt_start = datetime.now()
print(dt_start, 'start...')


#Python_Test-FrequencyCentroid

#FrequencyCentroid
#AMPLITUDE VS FREQUENCY CENTROID

#2D-Histogram
#FREQUENCY CENTROID
#Frequency Centroid(kHz) <All Channels>

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
#import matplotlib.mlab as mlab #outdated, use scipy
import scipy.stats as stats

#a = a #0 Hit
#b = b #1 Channel
#c = f #5 Amplitude
#d = h #7 FRQC

#Figure Size >> Set Plot Window Size >> 10,8 >> No need for dpi save scaling...
fig = plt.figure(figsize=(16,9))

try:
    if ts[0] == 'False':
        internals = 'No'
    else:
        internals = str('Yes, ' + tt[0] + '%')
except:
    print('Exception:', 'Internals string for title')
pass

try:
    fig.suptitle('[Report # %s, Date: %s] [FileName: %s] [TestDate: %s] [Material: %s] [Channels: %s] \n\
[TankSerial # %s] [OperatorName: %s] [Location: %s] [FillLevel: %s] [Weather: %s] [Contents: %s] [Tank Diameter: %s %s, Height: %s %s] \n\
[Tank %s, Category: %s, Priority: %s] [Tank %s, Category: %s, Priority: %s] [Internals in Tank: %s] \n \
FREQUENCY CENTROID'\
%(td[0],te[0],tf[0],tg[0],th[0],tn[0],
  ti[0],tj[0],tk[0],tl[0],tm[0], to[0],tp[0],tr[0],tq[0],tr[0],
  ta[0],tb[0],tc[0], ta[1],tb[1],tc[1], internals), fontsize=10, color='b') 
except:
    print('Exception: #suptitle')
    pass

#Grid
plt.minorticks_on()
plt.grid(b=True, which='major', color='k', linestyle=':', linewidth=0.5, alpha=0.25)
plt.grid(b=True, which='minor', color='gray', linestyle=':', linewidth=0.5, alpha=0.2)

try:
    #The probability density function
    #
    #2d histogram >> normal...
    #hist = plt.hist2d(h, f, bins=len(h), norm=colors.LogNorm())
    #hist = plt.hist2d(h, f, bins=(min(h), max(h)), norm=colors.LogNorm())
    ''
    #plot histogram
    #the histogram of the data
    #h=d                     #pass values
    h.sort()                #first sort values
    hmin = int(np.min(h))   #min of distribution
    hmax = int(np.max(h))   #max of distribution
    hmean = int(np.mean(h)) #mean of distribution
    hstd = int(np.std(h))   #standard deviation of distribution
    print('Freq. min %s, max %s, mean %s, std %s' %(hmin, hmax, hmean, hstd))
    #print('Hits  min %s, max %s, mean %s, std %s' %(int(np.min(a)), int(np.max(a)), int(np.mean(a)), int(np.std(a))))
    
    n_bins = int(hmax)
    print(n_bins)
    
    # N is the count in each bin, bins is the lower-limit of the bin    
    N, bins, patches = plt.hist(h, int(n_bins), density=1, facecolor='orange', alpha=0.75)
    #print(bins)
    ''
    #color color lines!
    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()
    #print(fracs)
    
    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())
    
    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    
    #add ideal curve line >> as per sensor
    mui = 30            # ideally near 30kHz for low frequency sensors
    sigma = hstd        # standard deviation of distribution
    yi = stats.norm.pdf(h, mui, sigma)
    plt.plot(h, yi, 'g--', linewidth=2.0, label='Ideal ')        
    
    #add a 'best fit' line >> average or mean
    mub = hmean         # ideally near 30kHz for low frequency sensors
    sigma = hstd        # standard deviation of distribution
    fit = stats.norm.pdf(h, mub, sigma)
    plt.plot(h, fit, 'r--', linewidth=2.0, label='Mean ')
    '''
    #add curve line >> peak
    mup = hmean         # Average or mean of  FRQC
    sigma = 60          # standard deviation of distribution
    yp = stats.norm.pdf(h, mup, sigma)
    plt.plot(h, yp, 'b--', linewidth=1.5, label='Current ')
    '''
    #draw a line at peak
    x,y = [[hmean,hmean],[max(fit),0]] #values for line
    plt.plot(x, y, 'ok--', linewidth=1.0, label='kHz ')
    
    #add a text
    x,y = [[hmean,hmean],[max(fit),0]] #values for line
    plt.text(x[0], y[0]*1.01, ' Min = %s, Max = %s \n Mean = %s, StdDev = %s ' %(hmin,hmax,hmean,hstd), fontsize=12, color='k')
except:
    print('Exception: #Plot histogram')
    pass

try:
    if max(h) >= 100:#More than 100
        plt.xticks(np.arange(0, max(h)+50, 50)) #Force Ticks Increment Value
    else:
        plt.xticks(np.arange(0, max(h)+2, 2)) #Force Ticks Increment Value
    #Details
    plt.xlabel('Freq. Centroid (kHz)')
    plt.yticks([]) #No Ticksplt.xlabel('Freq. Centroid (kHz)')
    plt.legend(loc='best')#Shows label, Best Location
    plt.title('Freq. Centroid (kHz) <All Channels>''<{:.0f}-{:.0f}>'.format(np.amin(b), np.amax(b)))
except:
    print('Exception: #Title')
    pass

try:
    #FilePath, Folder, FileName
    File_path = os.path.abspath(__file__)
    File_dir = os.path.dirname(__file__)
    Images_dir = os.path.join(File_dir, 'Images')
    #Create Folder if not found
    if not os.path.isdir(Images_dir):
        os.makedirs(Images_dir)
    File_name = 'FrequencyCentroid.png'
    File_path_image = os.path.join(Images_dir, File_name)
    #Save image
    plt.savefig(File_path_image, bbox_inches="tight")
except:
    print('Exception: #Save image', File_name)
    pass

#Set Window Title (Default Figure 1)
fig.canvas.set_window_title('FREQUENCY CENTROID')

#plt.show()
plt.close('all')

dt_stop = datetime.now()
dt_diff_7 = dt_stop - dt_start
print('Time taken {}'.format(dt_diff_7))
print(dt_stop, 'all tasks complete...')

print('Time taken {}'.format(dt_diff_1))
print('Time taken {}'.format(dt_diff_2))
print('Time taken {}'.format(dt_diff_3))
print('Time taken {}'.format(dt_diff_4))
print('Time taken {}'.format(dt_diff_5))
print('Time taken {}'.format(dt_diff_6))
print('Time taken {}'.format(dt_diff_7))
dt_total = dt_diff_1 + dt_diff_2 + dt_diff_3 + dt_diff_4 + dt_diff_5 + dt_diff_6 + dt_diff_7
print('Total Time {}'.format(dt_total))

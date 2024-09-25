#ae txt data file summary
'''
# ae-txt-summary.py
# created by mahemys; 2019.05.04
# !perfect, but works!
# MIT; no license; free to use!
# update 2019.05.04; initial review
# update 2020.04.23; optimise
# 
#------------------------------------------------------------
# read acoustic emission txt data files and generate initial summary
#------------------------------------------------------------
# Mistras and Vallen *txt data files support
# Mistras *txt data files support complete
# Vallen  *txt data files support pending...
# support for trimmed ascii files, properly formated lines
# support for non trimmed ascii files, handled in exclude
# read huge file in chunks
# use 64-bit for huge files
# vallen data files contains \x00, discard file
# ID2RawFile.txt; save to text file
# 
#------------------------------------------------------------
'''

# importing tkinter and tkinter.ttk and all their functions and classes
import os
import platform
from tkinter import *
from tkinter import ttk         #grid, row, col
#from tkinter.ttk import *      #pack, progressbar
from tkinter.filedialog import askopenfile
from datetime import datetime

#open file in read mode
def open_file():
    dt_start = datetime.now()
    print(dt_start, 'select txt file to process...')
    
    files = [('Text Document', '*.txt')]
    file = askopenfile(mode ='r', filetypes = files, defaultextension = files)
    
    if file is not None:
        dt_start     = datetime.now()
        file_path    = file.name
        file_size    = os.path.getsize(file_path)
        file_size_mb = file_size / 1024 ** 2
        print(dt_start, 'start...')
        print('file selected...  {} '.format(file_path))
        print('file size.......  {:,.2f} MB ({:,} bytes)'.format(file_size_mb, file_size))
        
        file_name_ext = os.path.basename(file_path)
        file_name     = os.path.splitext(file_name_ext)[0]
        file_ext      = os.path.splitext(file_name_ext)[1]
        print('file name.......  {} '.format(file_name_ext))
        
        #read file, count lines...
        file_readlines = open(file_path).readlines()
        file_linecount = len(file_readlines)
        print('file line count   {:,}'.format(file_linecount))
        
        if is_64bits == False:
            if file_linecount > 2000000:
                print('file exceeds 32-bit limit... Open file in 64-bit mode...')
                return
    else:
        print(datetime.now(), 'no file selected...')
    
    #Variables...
    vallen_identifier  = 'Id\t'
    mistras_identifier = ' ID DDD HH:MM:SS.mmmuuun      PARA1  CH  '
    vallen_datastring  = ['Ht', 'LE', 'Ev']
    mistras_datastring = '  1'
    vallen_version     = False
    mistras_version    = False
    line_number        = 0
    header_string      = ''
    header_array       = []
    valid_file         = False
    
    if file is not None:
        #find identifier, line number...
        print('wait... find identifier, line number...')
        for cnt, line in enumerate(file_readlines):
            if line is not None and vallen_identifier in line:
                print("Line {}: {}".format(cnt, line.strip()))
                print("Vallen version... Line {}".format(cnt))
                vallen_version  = True
                line_number = cnt
                header_string = line.strip()
                break
            elif line is not None and mistras_identifier in line:
                print("Line {}: {}".format(cnt, line.strip()))
                print("Mistras version... Line {}".format(cnt))
                mistras_version = True
                line_number = cnt
                header_string = line.strip()
                break
        
        if vallen_version == False and mistras_version == False:
            valid_file = False
            print("Vallen {}, Mistras {}".format(vallen_version, mistras_version))
        else:
            valid_file = True
            print("Vallen {}, Mistras {}".format(vallen_version, mistras_version))
            if not len(header_string) == 0:
                print('header length \t', len(header_string))
                #remove non ascii
                print('header string \t', header_string)
                new_string = re.sub(r'[^\x00-\x7F]+',' ', header_string)
                print('header ascii \t', new_string)
                header_array = new_string.split()
                print('header array \t', header_array)
            else:
                print('header length \t', len(header_string))
    
    #pandas read csv
    import pandas as pd
    
    if file is not None and valid_file == True:
        print('reading file... {}'.format(file_path))
        if vallen_version == True:
            # Vallen  *txt data files support pending....
            
            print("Vallen version  {}".format(vallen_version))
            #skipping lines that starts with a certain string
            exclude = [i for i, line in enumerate(open(file_path)) if not line.startswith(tuple(vallen_datastring))]
            print('exclude...      ', len(exclude))
            
            #read file in chunks, append and create df, exclude non datastring
            chunklist = []
            chunksize = 100000
            for chunk in  pd.read_csv(file_path, delimiter='\t', header=None, skiprows=exclude[0:], skip_blank_lines=True, low_memory=False, chunksize=chunksize):
                chunklist.append(chunk)
            df = pd.concat(chunklist, axis= 0).dropna()
            del chunklist
            #add header to df
            df.columns = header_array
            #print(df.info())
            print(df.head())
            print(df.shape)
            
            #use sep for multiple delimeters
            #header is at line 0
            #df = pd.read_csv(file_path, delimiter='\t', header=None, skiprows=exclude[0:], skip_blank_lines=True, low_memory=False).dropna()
            #df = pd.read_csv(file_path, delimiter='\t', skiprows=line_number, skip_blank_lines=True).dropna()
            #print(df)
        elif mistras_version == True:
            # Mistras *txt data files support complete...
            
            print("Mistras version  {}".format(mistras_version))
            #skipping lines that starts with a certain string
            exclude = [i for i, line in enumerate(open(file_path)) if not line.startswith(mistras_datastring)]
            print('exclude...      ', len(exclude))
            
            #read file in chunks, append and create df, exclude non datastring
            chunklist = []
            chunksize = 100000
            for chunk in  pd.read_csv(file_path, sep='\s+', header=None, skiprows=exclude[0:], skip_blank_lines=True, low_memory=False, chunksize=chunksize):
                chunklist.append(chunk)
            df = pd.concat(chunklist, axis= 0).dropna()
            del chunklist
            #add header to df
            df.columns = header_array
            #print(df.info())
            print(df.head())
            print(df.shape)
            
            def convert_to_seconds(time_in_some_format):
                try:
                    time_string  = str(time_in_some_format)
                    time_split   = time_string.split(':')
                    time_hour    = int(time_split[0])
                    time_mins    = int(time_split[1])
                    time_secs    = float(time_split[2])
                    time_in_secs = (time_hour * 3600) + (time_mins * 60) + time_secs
                    return float("{:.7f}".format(time_in_secs))
                except:
                    pass
            
            #rename [HH:MM:SS.mmmuuun] to [DayTime], convert [DayTime] to seconds, drop [DDD]...
            #since we drop [DDD], [PARA1] is now col[2]
            df.rename(columns={'HH:MM:SS.mmmuuun' : 'DayTime'}, inplace=True)
            print('wait... convert_to_seconds')
            df['DayTime'] = df['DayTime'].apply(convert_to_seconds)
            df['DayTime'] = df['DayTime'] + (df['DDD'] * 3600 * 24)
            df.drop('DDD', axis=1, inplace=True)
            
            #print(df.info())
            print(df.head())
            print(df.shape)
            
            #use sep for multiple delimeters
            #header is at line 0 since we skiprows 8
            #df = pd.read_csv(file_path, delimiter=None, header=None, skiprows=exclude[0:], skip_blank_lines=True).dropna()
            #df = pd.read_csv(file_path, sep='\s+', header=None, skiprows=exclude[0:], skip_blank_lines=True, low_memory=False).dropna()
            #df = pd.read_csv(file_path, sep='\s+', header=0, skiprows=line_number-1, skip_blank_lines=True, low_memory=False).dropna()
            #print(df)
            #print(df.info())
            #print(df.info(memory_usage='deep'))
            #print('wait...')
            #print(df.head())
            #print(df.shape)         #Return a tuple representing the dimensionality of the DataFrame.
            #print(df.describe())    #Generate descriptive statistics that summarize the central tendency, dispersion and shape of a dataset’s distribution, excluding NaN values.
            #df_t = df.describe()    #pass df to new df to transpose.
            #print(df_t.transpose()) #Transpose index and columns.
            
            #ID2RawFile.txt >> save df to text file using csv...
            #header format  >> #Hit,Channel,DayTime,Energy,Duration,Amplitude,ASL,FRQC

            df_txt           = df
            text_filename_df = 'ID2RawFile.txt'
            df_txt_column    = '#Hit,Channel,DayTime,Energy,Duration,Amplitude,ASL,FRQC'
            print(df_txt_column)
            
            if 'FRQ-C' in df_txt.columns or 'C-FRQ' in df_txt.columns:
                print(df_txt.columns.values)
            else:
                #create column for FRQC...
                df_txt['FRQ-C'] = df_txt.apply(lambda row: 0, axis = 1)
            
            #create column for Hits...
            df_txt.insert(loc = 0, column = 'Hit', value = range(1, (len(df_txt) + 1)))
            print(df_txt.head())
            print(df_txt.shape)
            
            #df from select columns...
            if not 'ASL' in header_array:
                df_txt.insert(loc = 0, column = 'ASL', value = 0)
            
            df_txt_new = df_txt[['Hit', 'CH', 'DayTime', 'ENER', 'DURATION', 'AMP', 'ASL', 'FRQ-C']]
            df_txt = df_txt_new
            print(df_txt.head())
            print(df_txt.shape)
            
            #save df to text file using csv...
            df_txt.to_csv(text_filename_df, index = None, header=False)
            print('save df to text file...', text_filename_df)
            #insert header into first line...
            with open(text_filename_df, 'r') as original: data = original.read()
            with open(text_filename_df, 'w') as modified: modified.write(df_txt_column + '\n' + data)
            print('save to text file complete...', text_filename_df)
            
        for dtype in ['float','int','object']:
            selected_dtype = df.select_dtypes(include=[dtype])
            mean_usage_b = selected_dtype.memory_usage(deep=True).mean()
            mean_usage_mb = mean_usage_b / 1024 ** 2
            print("Average memory usage for {} columns: {:03.2f} MB".format(dtype, mean_usage_mb))
            
    if file is not None and valid_file == True:
        if 'CH' in df.columns:
            #CH is present in column
            #df = df.astype(float)
            
            #print('col_list, col_max...')
            col_list = list(df)                         #column list
            col_max  = len(df.columns)                  #column count
            print('col_list        ', col_list)
            print('col_max         ', col_max)
            
            CH_min = df.min(axis=0)['CH']               #column CH min
            CH_max = df.max(axis=0)['CH']               #column CH max
            #CH always integer
            CH_min = int(CH_min)
            CH_max = int(CH_max)
            print('CH_min          ', CH_min)
            print('CH_max          ', CH_max)
            #CH always starts from 1
            if CH_min > 1:
                CH_min = 1
            
            #find missing channel using difference of two lists...
            CH_unique = df.CH.unique().tolist()
            print('CH_unique       ', len(CH_unique), CH_unique)
            
            CH_count_total   = CH_max
            CH_count_present = len(CH_unique)
            CH_count_missing = (CH_count_total - CH_count_present)
            print('CH_count_total  ', CH_count_total)
            print('CH_count_present', CH_count_present)
            print('CH_count_missing', CH_count_missing)
            print('wait... find min, max, mean, stddev for each channel')
            
            #print('max value of each row...')
            #print(df.max(axis=1))                      #max value of each row
            
            #print('min value of each column...')
            #df_min = df.min(axis = 0, skipna = True)    #min value of each column...
            #print(df_min)
            
            #print('max value of each column...')
            #df_max = df.max(axis = 0, skipna = True)    #max value of each column...
            #print(df_max)
            
            #print('mean value each column...')
            #col = df.loc[: , "PARA1":"ASL"]
            #col = df.iloc[:, 2:col_max]
            #df_mean = col.mean(axis = 0, skipna = True) #mean value of each column...
            #print(df_mean)
            
            #print('std value each column...')
            #col = df.loc[: , "PARA1":"ASL"]
            #col = df.iloc[:, 2:col_max]
            #df_std = col.std(axis = 0, skipna = True)   #mean value of each column...
            #print(df_std)
            
            #print('max value of CH each row...')
            #df_CH_max = df.loc[df['CH'].idxmax()]      #max value of CH each row...
            #print(df_CH_max)
            
            #print('index of each row containing CH max...')
            #df_CH_max = df[['CH']][df.CH == df.CH.max()] #index of each row containing CH max...
            #print(df_CH_max)
            
            #create multiple df for each channel...
            df_CH      = {}
            df_CH_min  = {}
            df_CH_max  = {}
            df_CH_mean = {}
            df_CH_std  = {}
            df_CH_chan = {}
            s_ch_min   = {}
            s_ch_max   = {}
            s_ch_mean  = {}
            s_ch_std   = {}
            s_ch_chan  = {}
            s_ch_concat= {}
            
            #find min, max, mean, stddev for each channel using for loop...
            for i in range(CH_min, (CH_max + 1), 1):
                #print('rows with CH['+str(i)+']...')
                df_CH[i] = df[df.CH == i]                           #rows with CH_1...
                #print(df_CH[i])
                #print(df_CH[i].info())
                #print(df_CH[i].head())
                
                #if channel is missing, create df, append and pass values as nan, CH as i
                if not i in CH_unique:
                    data = pd.DataFrame(index=range(0,1), columns=df.columns)
                    df_CH[i] = df_CH[i].append(data)
                    #df_CH[i].CH = df_CH[i].fillna(value=0, inplace=True)
                    df_CH[i].CH = df_CH[i].CH.fillna(i)
                    #print(df_CH[i].head())
                
                #col = df_CH[i].loc[: , "PARA1":"ASL"]               #Para to last column
                col = df_CH[i].iloc[:, 2:col_max]                   #Para to last column
                #print(col)
                
                #print('\n min value of CH['+str(i)+'] each column...')
                df_CH_min[i] = col.min(axis = 0, skipna = True)    #min value of each column...
                df_CH_min[i] = df_CH_min[i].fillna(0)
                #print(df_CH_min[i])
                
                #print('\n max value of CH['+str(i)+'] each column...')
                df_CH_max[i] = col.max(axis = 0, skipna = True)    #max value of each column...
                df_CH_max[i] = df_CH_max[i].fillna(0)
                #print(df_CH_max[i])
                
                #print('\n mean value CH['+str(i)+'] each column...')
                df_CH_mean[i] = col.mean(axis = 0, skipna = True)   #mean value of each column...
                df_CH_mean[i] = df_CH_mean[i].fillna(0)
                #print(df_CH_mean[i])
                
                #print('\n std value CH['+str(i)+'] each column...')
                df_CH_std[i] = col.std(axis = 0, skipna = True)     #std value of each column...
                df_CH_std[i] = df_CH_std[i].fillna(0)
                #print(df_CH_std[i])
                
                #print('\n chan value CH['+str(i)+'] each column...')
                df_CH_chan[i] = col.min(axis = 0, skipna = True)    #chan value of each column...
                df_CH_chan[i] = df_CH_chan[i].replace(col, i)       #replace all values with chan
                df_CH_chan[i] = df_CH_chan[i].fillna(0)
                #print(df_CH_chan[i])
                
                #create df series for min max mean std...
                s_ch_min[i] = pd.Series(df_CH_min[i], name = 'Minimum')#CH['+str(i)+']')
                s_ch_min[i] = s_ch_min[i].map('{:15.4f}'.format)
                #print(s_ch_min[i])
                
                s_ch_max[i] = pd.Series(df_CH_max[i], name = 'Maximum')#CH['+str(i)+']')
                s_ch_max[i] = s_ch_max[i].map('{:15.4f}'.format)
                #print(s_ch_max[i])
                
                s_ch_mean[i] = pd.Series(df_CH_mean[i], name = 'Average')#CH['+str(i)+']')
                s_ch_mean[i] = s_ch_mean[i].map('{:15.4f}'.format)
                #print(s_ch_mean[i])
                
                s_ch_std[i] = pd.Series(df_CH_std[i], name = 'StdDev')#CH['+str(i)+']')
                s_ch_std[i] = s_ch_std[i].map('{:15.4f}'.format)
                #print(s_ch_std[i])
                
                s_ch_chan[i] = pd.Series(df_CH_chan[i], name = 'Chan')#CH['+str(i)+']')
                s_ch_chan[i] = s_ch_chan[i].map('{:5.0f}'.format)
                #print(s_ch_chan[i])
                
                s_ch_concat[i] = pd.concat([s_ch_chan[i], s_ch_min[i], s_ch_max[i], s_ch_mean[i], s_ch_std[i]], axis=1, sort=False)
                s_ch_concat[i] = s_ch_concat[i].drop(['CH'])
                #print(s_ch_concat[i].to_string())
                
                if i == 1:
                    #first one with header...
                    print('HIT DRIVEN DATA:')
                    print(s_ch_concat[i].to_string(header=True))
                else:
                    print(s_ch_concat[i].to_string(header=False))
            
            #save summary to text file
            text_file_name = "Summary.txt"
            #text_file_name = "Summary_" + file_name + ".txt"
            text_file = open(text_file_name, "w")
            text_file.write('File selected         : {}'.format(file_path.replace("/", "\\")) + '\n')
            text_file.write('File size             : {:,.2f} MB ({:,} bytes)'.format(file_size_mb, file_size) + '\n')
            text_file.write('\n')
            text_file.write('Total AEHits          : {}'.format(df.shape[0]) + '\n')
            text_file.write('Total Channel Count   : {}'.format(CH_count_total) + '\n')
            text_file.write('Total Channel Missing : {}'.format(CH_count_missing) + '\n')
            
            #Channel and AEHits
            for i in range(CH_min, (CH_max + 1), 1):
                if i == 1:
                    #first one with header...
                    print('Channel         AEHits')
                    text_file.write('\n')
                    text_file.write('Channel         AEHits' + '\n')
                if i in CH_unique:
                    print('{:7}{:15}'.format(i, df_CH[i].shape[0]))
                    text_file.write('{:7}{:15}'.format(i, df_CH[i].shape[0]) + '\n')
                else:
                    print('{:7}{:15}'.format(i, 0))
                    text_file.write('{:7}{:15}'.format(i, 0) + '\n')
            
            #HIT DRIVEN DATA
            for i in range(CH_min, (CH_max + 1), 1):
                if i == 1:
                    #first one with header...
                    text_file.write('\n')
                    text_file.write('HIT DRIVEN DATA:' + '\n')
                    text_file.write(s_ch_concat[i].to_string(header=True) + '\n')
                else:
                    text_file.write(s_ch_concat[i].to_string(header=False) + '\n')
            
            #find missing channel...
            CH_list_min_max = []
            CH_missing_bool = []
            CH_missing_list = []
            CH_present_list = []
            CH_hits_per_Ch  = []
            
            for i in range(CH_min, (CH_max + 1), 1):
                if i in CH_unique:
                    print('CH_exists ', i)
                    CH_missing_bool.append(False)
                    CH_hits_per_Ch.append(df_CH[i].shape[0])
                else:
                    print('CH_missing', i)
                    CH_missing_bool.append(True)
                    CH_hits_per_Ch.append(0)
                CH_list_min_max.append(i)
            
            print('CH_hits_per_Ch  {:3d} {}'.format(len(CH_hits_per_Ch), CH_hits_per_Ch))
            print('CH_list_min_max {:3d} {}'.format(len(CH_list_min_max), CH_list_min_max))
            print('CH_missing_bool {:3d} {}'.format(len(CH_missing_bool), CH_missing_bool))
            
            #find missing channel using for loop...
            for j in range(CH_min - 1, (CH_max), 1):
                if CH_missing_bool[j] == True:
                    CH_missing_list.append(j + 1)
                else:
                    CH_present_list.append(j + 1)
            print('CH_present_list {:3d} {}'.format(len(CH_present_list), CH_present_list))
            print('CH_missing_list {:3d} {}'.format(len(CH_missing_list), CH_missing_list))
            
            #find missing channel using difference of two lists...
            CH_list_unique = df.CH.unique().tolist()
            CH_list_unique = [int(i) for i in CH_list_unique]
            print('CH_list_unique  {:3d} {}'.format(len(CH_list_unique), CH_list_unique))
            
            list_A = CH_list_min_max    #[10, 15, 20, 25, 30, 35, 40]
            list_B = CH_list_unique     #[2, 4, 3]
            CH_list_diff = list(set(list_A) - set(list_B))
            print('CH_list_diff    {:3d} {}'.format(len(CH_list_diff), CH_list_diff))
            
            text_file.write('\n')
            text_file.write('Channel wise Hits    {:3d} {}'.format(len(CH_hits_per_Ch), CH_hits_per_Ch) + '\n')
            text_file.write('Channel ideal list   {:3d} {}'.format(len(CH_list_min_max), CH_list_min_max) + '\n')
            #text_file.write('Channel missing bool {:3d} {}'.format(len(CH_missing_bool), CH_missing_bool) + '\n')
            text_file.write('Channel present list {:3d} {}'.format(len(CH_present_list), CH_present_list) + '\n')
            text_file.write('Channel missing list {:3d} {}'.format(len(CH_missing_list), CH_missing_list) + '\n')
            text_file.write('Channel unique list  {:3d} {}'.format(len(CH_list_unique), CH_list_unique) + '\n')
            text_file.write('Channel difference   {:3d} {}'.format(len(CH_list_diff), CH_list_diff) + '\n')
            #text_file.close()
            
            #add Ch and Hits to dict...
            CH_hits_dict = dict(zip(CH_list_min_max, CH_hits_per_Ch))
            print('CH_hits_dict dict   {}'.format(str(CH_hits_dict)))
            print('CH_hits_dict keys   {}'.format(list(CH_hits_dict.keys())))
            print('CH_hits_dict values {}'.format(list(CH_hits_dict.values())))
            
            dt_stop = datetime.now()
            dt_diff = dt_stop - dt_start
            
            text_file.write('\n')
            text_file.write('Time Start : {}'.format(dt_start) + '\n')
            text_file.write('Time Stop  : {}'.format(dt_stop)  + '\n')
            text_file.write('Time Taken : {}'.format(dt_diff)  + '\n')
            text_file.close()
            
            print(dt_stop, 'all tasks complete...')
            print('Time taken {}'.format(dt_diff))
            

if __name__ == '__main__':
    #GUI...
    script_name = os.path.basename(__file__)
    root = Tk()
    root.geometry('300x100')
    root.title(script_name)
    
    lbl_1 = Label(root, text="Select txt file to process...")
    lbl_1.grid(row=0, column=0, padx=5, pady=5)
    
    btn_1 = Button(root, text='Open', height=1, width=15, command=lambda:open_file())
    btn_1.grid(row=0, column=1, padx=5, pady=5)
    
    is_64bits = sys.maxsize > 2**32
    if is_64bits:
        print('Python 64-bit')
    else:
        print('Python 32-bit')
    print(script_name)
    
    root.mainloop()

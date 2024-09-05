#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 19:08:24 2023

@author: suncica
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
#%matplotlib qt

os.chdir("/home/suncica/Documents/portfolio")  # set directory on ubuntu

data_from_csv = pd.read_csv('Example_Data.csv', low_memory=False) # load the data
#data_from_csv.head() # overview of data
#data_from_csv.shape # size of 'table

############################################################################################################
#################### funtion cleaning the NaNs #############################################################
############################################################################################################
def clean_data(input_list):
    DF_list = list()              #output LIST of data frames
    header = data_from_csv.columns                 #list of columns' names
    for i in range(len(input_list)):
        DF_list.append(data_from_csv[['Time[s]']+[col for col in header if input_list[i] in col]].dropna())
    return DF_list
############################################################################################################


#test function above:
selected_c = ['Column_1','Column_2','SlaveResp']
dfs = clean_data(selected_c)
#dfs

# select 'SlaveResp::' dataset
slave_resp = dfs[2] 


# rename the headers for simplicity
slave_resp.rename(columns={'Time[s]' : 'time',
                           'SlaveResp::SlaveRespB0': 'b0',
                           'SlaveResp::SlaveRespB1': 'b1',
                           'SlaveResp::SlaveRespB2' : 'b2',
                           'SlaveResp::SlaveRespB3' : 'b3',
                           'SlaveResp::SlaveRespB4' : 'b4',
                           'SlaveResp::SlaveRespB5' : 'b5',
                           'SlaveResp::SlaveRespB6' : 'b6',
                           'SlaveResp::SlaveRespB7' : 'b7'},
                  inplace=True)
slave_resp.reset_index(drop=True, inplace=True)
# show first 5 rows in slave_resp
# slave_resp.head()
    

############################################################################################################
############################### Data processing in 'Slave_resp' ############################################
############################################################################################################
slave_resp = slave_resp.iloc[:2001,:]      #take a subset for the code development

slave_resp = slave_resp.assign(  Temp_1=None, 
                                 Temp_2=None,
                                 Temp_3=None,
                                 Temp_4=None, 
                                 Temp_5=None, 
                                 Temp_6=None, 
                                 Cur_1=None,
                                 Cur_2=None,
                                 Cur_3=None,
                                 )

#initialize new subdataframes
columns50 = ['time','Temp_1', 'Temp_2', 'Temp_3', 'Temp_4']
columns51 = ['time', 'Temp_5', 'Temp_6']
columns42 = ['time', 'Cur_1', 'Cur_2']
columns46 = ['time', 'Cur_3']


df50 = pd.DataFrame(columns=columns50)
df51 = pd.DataFrame(columns=columns51)
df42 = pd.DataFrame(columns=columns42)
df46 = pd.DataFrame(columns=columns46)

df50 = df50.set_index('time')
df51 = df51.set_index('time')
df42 = df42.set_index('time')
df46 = df46.set_index('time')


for i, row in enumerate(slave_resp.itertuples(), 0): 
    if row.b1 == 16:  
        if row.b5 == 0:
            slave_resp.at[row.Index, 'Temp_1']=row.b6 - 40
            slave_resp.at[row.Index, 'Temp_2']=row.b7 - 40
            slave_resp.at[row.Index, 'Temp_3']=slave_resp.b2.iloc[i+1] - 40
            slave_resp.at[row.Index, 'Temp_4']=slave_resp.b3.iloc[i+1] - 40
            df_temp = pd.DataFrame([[slave_resp.at[row.Index, 'time'],row.b6 - 40, row.b7 - 40, slave_resp.b2.iloc[i+1] - 40, slave_resp.b3.iloc[i+1] - 40]], columns=columns50)
            df50 = pd.concat([df50, df_temp])
        elif row.b5 == 1: 
            n11 = hex(int(row.b6))
            n12 = hex(int(row.b7))
            conc12 = int(n11[2:]+n12[2:],16)
            slave_resp.at[row.Index, 'Temp_5'] = conc12
            n13 = hex(int(slave_resp.b2.iloc[i+1] ))
            n14 = hex(int(slave_resp.b3.iloc[i+1] ))
            conc13 = int(n13[2:]+n14[2:],16)
            slave_resp.at[row.Index, 'Temp_6'] = conc13
            df_temp = pd.DataFrame([[slave_resp.at[row.Index, 'time'], conc12, conc13]], columns=columns51)
            df51 = pd.concat([df51, df_temp])
    else:
        if row.b4 == 2:
            slave_resp.at[row.Index, 'Cur_1'] = row.b5*0.1
            slave_resp.at[row.Index, 'Cur_2'] = row.b6*0.1 
            df_temp = pd.DataFrame([[slave_resp.at[row.Index, 'time'], row.b5*0.1, row.b6*0.1]], columns=columns42)
            df42 = pd.concat([df42, df_temp])
        elif row.b4 == 6:
            slave_resp.at[row.Index, 'Cur_3'] = row.b5*25
            df_temp = pd.DataFrame([[slave_resp.at[row.Index, 'time'], row.b5*0.25]], columns=columns46)
            df46 = pd.concat([df46, df_temp])




#print(df0.head(), df0.size)
#df0.to_csv('df0.csv', index=False)
#print(list(df0.columns))
#slave_resp.drop(['b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7'], axis=1, inplace=True) 




# tests         
#print(slave_resp.b4.unique())
#slave_resp[['time','Temp_1']].dropna()
#slave_resp[['time','Temp_2']].dropna()
#slave_resp[['time','Temp_3']].dropna()
#slave_resp[['time','Temp_4']].dropna()
#slave_resp[['time','Temp_5']].dropna()
#slave_resp[['time','Temp_6']].dropna()
#slave_resp.columns[slave_resp1.eq(1).any()]


#####################################################################################################
#################### funtion writing to *.csv #######################################################
#####################################################################################################
def write_data(input_list_dfs, output_file):
    [df for df in input_list_dfs if df.reset_index(drop=True, inplace=True)]
    temp_df= pd.concat(input_list_dfs, axis=1, keys=None)
    temp_df.to_csv(output_file, index=False) #writes cleaned data to csv
#####################################################################################################

#reorder the columns in new subdataframes
df50 = df50[columns50]
df51 = df51[columns51]
df42 = df42[columns42]
df46 = df46[columns46]

#generate the output .csv file 
final_dfs = [df50, df51,  df42, df46]
write_data(final_dfs, 'sys_test_processed_data.csv')

######################################################################################################
############################## PLOTTING ##############################################################
######################################################################################################

# =============================================================================
# plot_data = slave_resp[['time','Temp_1']].dropna()
# plot_data = plot_data.join(data_from_csv['Column_1'])
# 
# plt.scatter(data_from_csv['Time[s]'],data_from_csv['Column_1'])
# plt.scatter(plot_data['time'], plot_data['Temp_1'])
# plt.show()
# 
# =============================================================================

    

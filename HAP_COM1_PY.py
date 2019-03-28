import pandas as pd
import numpy as np

def read_wvmmatch(read_dir_ , sideband):
    X2=['01','02','03','04','05','06','07','08','09','10','11','12','15']
    X= ['02','03','04','05','06','07','08','09','10','11','12','15'] #receptor number of start H0 

    H1=pd.read_csv(read_dir_+'wvmmatched_H01'+sideband+'.txt', index_col=0)

    H1['recep']='01'  #H00 doesn't use since it's not working now
    H1=H1[H1['trx'].diff()!=0] #remove some Trx data
    H1=H1.reset_index(drop=True)

    for i in np.arange(12):
        HX=pd.read_csv(read_dir_+'wvmmatched_H'+ X[i] + sideband+ '.txt', index_col=0)
        HX=HX[HX['trx'].diff()!=0] #remove some Trx data
        HX=HX.reset_index(drop=True)
        HX['recep']=X[i]
        H1=H1.append(HX)
    data=H1.reset_index(drop=True)
    data['sideband']=sideband
    return(data)

def read_merged(read_dir_ , sideband):
    X= ['02','03','04','05','06','07','08','09','10','11','12','15'] #receptor number start 0
    names=['utdate', 'obsnum', 'subsysnr', 'lofreq', 'iffreq', 'rffreq', 'trx', 'tsys']

    H1=pd.read_csv(read_dir_+'merged_H01_' + sideband + '.txt', header=None, names=names, sep=" ")

    H1['recep']='01'  #H00 doesn't use since it's not working now
    H1=H1[H1['trx'].diff()!=0] #remove some Trx data
    H1=H1.reset_index(drop=True)

    for i in np.arange(12):
        HX=pd.read_csv(read_dir_+'merged_H'+ X[i] + '_'+ sideband +'.txt',header=None, names=names, sep=" ")

        HX['recep']=X[i]
        H1=H1.append(HX)
    data=H1.reset_index(drop=True)
    data['sideband']=sideband
    return(data)


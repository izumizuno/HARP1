import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D
import math
from scipy.interpolate import *
#%matplotlib inline


#--------function
def twobin_ht_func(data, binsep, nbin_freq, out_dir, sideband):
    out_name_freq='sep'+str(nbin_freq)
    out_name_trx='bin'+str(np.diff(binsep)[1])
    #nbin_freq=70 # bin number for hist of lo frequency
    #binsep=np.arange(0,1050,50) #set the bin for trx histogram

    fig=plt.figure()
    ax = fig.add_subplot(211)
    ht_=ax.hist(data.lofreq,bins=nbin_freq, color='red')
    ax2 = fig.add_subplot(212)
    ax2.scatter(data.lofreq,data.trx, color='red', s=1)
    plt.savefig(out_dir+out_name_freq+sideband+'.png')

    #set bin for frequency
    count_lof=ht_[0]
    separation=ht_[1]
    sep_diff=np.diff(separation)
    center=separation[:-1]+sep_diff/2

    ht_lof=pd.DataFrame({'h_lo':center,
             'count':ht_[0]})
    
    nbin_trx=len(binsep)-1 
    histX=pd.DataFrame({'h_lo':np.zeros(nbin_freq*nbin_trx),
             'h_trx':np.zeros(nbin_freq*nbin_trx),
            'count':np.zeros(nbin_freq*nbin_trx),
                   'percent':np.zeros(nbin_freq*nbin_trx)})
    
    for i in np.arange(nbin_freq):
        if  count_lof[i]!=0:
            h_data=data.loc[(data['lofreq']>=separation[i]) & (data['lofreq']<separation[i+1]),'trx']
            fig=plt.figure()
            ax=fig.add_subplot(221)
            h_result=ax.hist(h_data,bins=binsep)

            ax2 = fig.add_subplot(212)
            ax2.scatter(data.lofreq,data.trx, color='red', s=1)

            start=i*nbin_trx
            end=i*nbin_trx+(nbin_trx-1)
            histX.loc[start:end,'count']=h_result[0]
            histX.loc[start:end,'percent']=h_result[0]/count_lof[i]
            histX.loc[start:end,'h_trx']=h_result[1][:-1]+np.diff(h_result[1])/2
            histX.loc[start:end,'h_lo']=center[i]
    ht_lo_trx=histX[histX['count']!=0]
    fig=plt.figure()
    ax=fig.add_subplot(111)
    sc=ax.scatter(x=ht_lo_trx['h_lo'], y=ht_lo_trx['h_trx'], c=ht_lo_trx['percent'],s=8)
    plt.colorbar(sc)
    plt.savefig(out_dir+out_name_trx+sideband+'.png')
    return(ht_lof, ht_lo_trx)


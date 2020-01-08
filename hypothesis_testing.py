import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.stats as stats
from datetime import datetime,timedelta

from data_pipeline import dly_process



def calculate_p_val(obs_series,obs_val):
    rv = stats.norm(obs_series.mean(),obs_series.std(ddof=1)) # use parameterized normal distribution
    return rv.sf(obs_val)


def series_select(df_in,dt,obs_el):
    dt = pd.to_datetime(dt) # expect compatible dt string like YYYYMMDD
    
    # just pull out dayofyear range +- 3 days
    # no special treatment for leap years
    if dt.dayofyear > 3 and dt.dayofyear < 362:
        dt0 = dt + pd.offsets.Day(-3)
        dt1 = dt + pd.offsets.Day(3)
        return df[(df.index.dayofyear >= dt0.dayofyear) & (df.index.dayofyear <= dt1.dayofyear)][obs_el]
    
    # handle boundary conditions at beginning of year
    elif dt.dayofyear <=3:
        dt0 = dt + pd.offsets.Day(-3)
        dt1 = dt + pd.offsets.Day(3)
        s0 = df[(df.index.dayofyear >= 1) & (df.index.dayofyear <= dt1.dayofyear)][obs_el]
        s1 = df[(df.index.dayofyear >= dt0.dayofyear) & (df.index.dayofyear <= 366)][obs_el]
        s = s0.append(s1).sort_index()
        return s

    # handle boundary conditions at end of year
    elif dt.dayofyear >=362:
        dt0 = dt + pd.offsets.Day(-3)
        dt1 = dt + pd.offsets.Day(3)
        s0 = df[(df.index.dayofyear >= dt0.dayofyear) & (df.index.dayofyear <= 366)][obs_el]
        s1 = df[(df.index.dayofyear >= 1) & (df.index.dayofyear <= dt1.dayofyear)][obs_el]
        s = s0.append(s1).sort_index()
        return


def gen_plot(fig,loc,date):
    #fig,ax = plt.subplots(figsize=(10,8))
    ax = fig.subplots()
    #n = 10
    #ax.plot(range(n), [random() for i in range(n)])
    
    dly_file = 'data/USW00094728.dly'

    #df = dly_process(dly_file)

    dt1 = '20200406'
    #Tmax_week = series_select(df,dt1,'TMAX') * 0.1

    # use ref series only up to 1980
    #Tmax_week_REF = Tmax_week[:'1980']


    #p_val = calculate_p_val(Tmax_week_REF,15)
    #print(p_val)

    #Tmax_week_REF.hist(ax=ax,density=True,bins=25)
    #Tmax_week['1981':].hist(ax=ax,alpha=0.5,density=True,bins=25)

    b = np.arange(600)*0.1-20 # all temps -20 to 40
    #g = stats.norm(Tmax_week_REF.mean(),Tmax_week_REF.std())
    g = stats.norm(0,5)
    ax.plot(b,g.pdf(b))
    ax.set_title(loc+' '+date)
    #plt.show()





import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.stats as stats
from datetime import datetime,timedelta
from geopy.distance import great_circle
import geopandas as gpd

from data_pipeline import dly_process



class ttestProduct():

    def __init__(self, loc, date):

        self.loc = loc
        self.date = pd.to_datetime(date,yearfirst=True) # expect compatible dt string like YYYYMMDD
        
        shapely_geo = gpd.tools.geocode(self.loc).iloc[0]
        latlon = (shapely_geo.geometry.y,shapely_geo.geometry.x)
        
        self.station = self.select_nearest_station(latlon)
        station_id = self.station.ID
        
        dly_file_force = 'data/USW00094728.dly'
        self.dly_file = 'data/ghcnd_hcn/'+station_id+'.dly'

        self.df = dly_process(self.dly_file)
        self.Tmax_week = self.series_select(self.df,self.date,'TMAX') * 0.1

    def select_nearest_station(self,latlon):
        df_hcn = pd.read_pickle('data/df_hcn_stations.pkl')
        hcn_latlon = list(zip(df_hcn.LATITUDE,df_hcn.LONGITUDE))
        distances = [great_circle(latlon,p).km for p in hcn_latlon]
        
        return df_hcn.iloc[distances.index(min(distances))]

    def calculate_p_val(self,obs_series,obs_val):
        rv = stats.norm(obs_series.mean(),obs_series.std(ddof=1)) # use parameterized normal distribution
        return rv.sf(obs_val)


    def series_select(self,df,dt,obs_el):
        
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


    def gen_plot(self,fig):
        
        ax = fig.subplots()
        
        # use ref series only up to 1980
        Tmax_week_REF = self.Tmax_week[:'1980']
        Tmax_week_recent = self.Tmax_week['1981':]

        value_on_date = self.Tmax_week[self.date]
        
        p_val = self.calculate_p_val(Tmax_week_REF,value_on_date)

        ax.hist(Tmax_week_REF.values,density=True,bins=25)
        ax.hist(Tmax_week_recent.values,density=True,bins=25,histtype='step')
        
        b = np.arange(600)*0.1-20 # all temps -20 to 40
        g = stats.norm(Tmax_week_REF.mean(),Tmax_week_REF.std())
        # estimate parameters from sample
        #ae, loce, scalee = stats.skewnorm.fit(Tmax_week_REF.values)
        #print(ae,loce,scalee)
        ax.plot(b,g.pdf(b),lw=0.5)
        ax.set_title('High Temperatures in {'+self.station.NAME+', '+self.station.STATE+'} on week of '+self.date.strftime('%m-%d'))
        ax.axvline(x=value_on_date,c='r',lw=2)
        ax.text(40,.1,f'P value: {p_val:5.3}',ha='right')

        label_ha = 'left' if p_val < 0.5 else 'right' 

        ax.text(value_on_date,.1,self.date.strftime(' %Y '),ha=label_ha)
        
        ax.set_ylim(0,.12)
        ax.set_xlabel('°C')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.stats as stats
import geopandas as gpd
from geopy.distance import great_circle

from data_pipeline import dly_process

class weatherRecord():

    def __init__(self, loc, date):
        self.loc = loc # loc is a string that can be parsed by geocode
        self.date = pd.to_datetime(date,yearfirst=True) # expect compatible dt string like YYYY-MM-DD
        
        # initialize latlon to Denver, CO prior to geocode try/except block
        latlon = (39.7392365108763, -104.990217201602)
        try:
            shapely_geo = gpd.tools.geocode(self.loc).iloc[0] # uses service to find location
            latlon = (shapely_geo.geometry.y,shapely_geo.geometry.x)
        except:
            self.loc = 'Denver, CO'
            print('Error geocode - default to Denver')
        

        self.station = self.select_nearest_station(latlon)
        station_id = self.station.ID
        print(station_id)
        #dly_file = 'data/USW00094728.dly' # for testing purposes
        dly_file = 'data/ghcnd_hcn/'+station_id+'.dly'

        self.df = dly_process(dly_file)

        if not self.date in self.df.index:
            print('Error - Date out of range')
            self.date = self.df.index[-1] # set to last available day

        self.Tmax_week = self.series_select(self.df,self.date,'TMAX') * 0.1

    def select_nearest_station(self,latlon):
        df_hcn = pd.read_pickle('data/df_hcn_stations.pkl')
        hcn_latlon = list(zip(df_hcn.LATITUDE,df_hcn.LONGITUDE))
        distances = [great_circle(latlon,p).km for p in hcn_latlon]
        
        return df_hcn.iloc[distances.index(min(distances))]

    def calculate_p_val(self,obs_series,obs_val):
        rv = stats.norm(obs_series.mean(),obs_series.std(ddof=1)) # use parameterized normal distribution
        return rv.sf(obs_val)

    def smear_raw_temps(self,t):
        r = (np.random.rand(t.size)-0.5)*2
        return t+r

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
        
        b = np.arange(61)*1-20
        ax.hist(self.smear_raw_temps(Tmax_week_REF.values),density=True,bins=b,alpha=.5,color='b')
        ax.hist(self.smear_raw_temps(Tmax_week_recent.values),density=True,bins=b,histtype='step',lw=2,color='r')
        
        x = np.arange(600)*0.1-20 # all temps -20 to 40

        y = Tmax_week_REF.values
        y = y[~np.isnan(y)]  
        ae, loce, scalee = stats.skewnorm.fit(y) 
        print(ae)
        sn = stats.skewnorm(ae, loce, scalee)
        n = stats.norm(Tmax_week_REF.mean(),Tmax_week_REF.std())
        p_val = sn.sf(value_on_date)
        ax.plot(x,sn.pdf(x),lw=1,c='b')
        ax.plot(x,n.pdf(x),lw=0.5,c='g')
        #print(sg.sf(30),g.sf(30))
        
        zero,ymax = ax.get_ylim()

        ax.set_title('High Temperatures in '+self.station.NAME+', '+self.station.STATE+' on week of '+self.date.strftime('%b-%d'))
        ax.axvline(x=value_on_date,c='k',lw=2)
        

        annot_x = -20 if value_on_date > 20 else 40
        annot_ha = 'left' if value_on_date > 20 else 'right'
        label_ha = 'left' if p_val < 0.5 else 'right' 

        ax.text(annot_x,.01,f'P_value: {p_val:5.3}',ha=annot_ha)
        ax.text(annot_x,.02,self.date.strftime('%Y')+f': {value_on_date}°',ha=annot_ha)
        
        
        
        #ax.set_ylim(0,.15)
        ax.set_xlabel('°C')
    
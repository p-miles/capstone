import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.stats as stats
import geopandas as gpd
from geopy.distance import great_circle

from data_pipeline import dly_process


class WeatherRecord():

    def __init__(self, loc, date):
        self.loc = loc  # loc is a string that can be parsed by geocode
        # expect compatible dt string like YYYY-MM-DD
        self.date = pd.to_datetime(date, yearfirst=True)

        # Geocode web service sometimes failes so use try/except block
        try:
            shapely_geo = gpd.tools.geocode(self.loc).iloc[0]
            latlon = (shapely_geo.geometry.y, shapely_geo.geometry.x)
        except:
            self.loc = 'Denver, CO'
            latlon = (39.7392365108763, -104.990217201602)
            print('Error geocode - default to Denver')

        self.df_hcn = pd.read_pickle('data/df_hcn_stations.pkl')
        self.station = self.select_nearest_station(latlon)

        #print(self.station.NAME, ' ', self.station.STATE)

        dly_file = 'data/ghcnd_hcn/'+self.station.ID+'.dly'
        if not os.path.exists(dly_file):
            # default file to use when full dataset unavailable
            dly_file = 'data/USW00094728.dly'
            self.station = self.df_hcn[self.df_hcn.ID == 'USW00094728'].iloc[0]

        # create pandas dataframe, ref data_pipeline.py
        self.df = dly_process(dly_file)

        # error handling for date range
        if self.date not in self.df.index:
            print('Error: Date out of range.  Default to last day in record')
            self.date = self.df.index[-1]  # set to last available day

        # select temperature data for analysis
        self.Tmax_week = self.series_select(self.date, 'TMAX') * 0.1

        # attributes for plotting initialized in this method
        self.p_val = self.hypothesis_testing()

    def select_nearest_station(self, latlon):
        hcn_latlon = list(zip(self.df_hcn.LATITUDE, self.df_hcn.LONGITUDE))
        distances = [great_circle(latlon, p).km for p in hcn_latlon]

        return self.df_hcn.iloc[distances.index(min(distances))]

    def series_select(self, dt, obs_el):
        # just pull out dayofyear range +- 3 days
        # no special treatment for leap years
        if dt.dayofyear > 3 and dt.dayofyear < 363:
            dt0 = dt + pd.offsets.Day(-3)
            dt1 = dt + pd.offsets.Day(3)
            return self.df[(self.df.index.dayofyear >= dt0.dayofyear) & (self.df.index.dayofyear <= dt1.dayofyear)][obs_el]

        # handle boundary conditions at beginning of year
        elif dt.dayofyear <= 3:
            dt0 = dt + pd.offsets.Day(-3)
            dt1 = dt + pd.offsets.Day(3)
            s0 = self.df[(self.df.index.dayofyear >= 1)
                         & (self.df.index.dayofyear <= dt1.dayofyear)][obs_el]
            s1 = self.df[(self.df.index.dayofyear >= dt0.dayofyear)
                         & (self.df.index.dayofyear <= 366)][obs_el]
            s = s0.append(s1).sort_index()
            return s

        # handle boundary conditions at end of year
        elif dt.dayofyear >= 363:
            dt0 = dt + pd.offsets.Day(-3)
            dt1 = dt + pd.offsets.Day(3)
            if dt1.dayofyear == 366:
                dt1 = dt1 + pd.offsets.Day(1)  # fix for leap year

            s0 = self.df[(self.df.index.dayofyear >= dt0.dayofyear)
                         & (self.df.index.dayofyear <= 366)][obs_el]
            s1 = self.df[(self.df.index.dayofyear >= 1)
                         & (self.df.index.dayofyear <= dt1.dayofyear)][obs_el]
            s = s0.append(s1).sort_index()
            return s

    def fit_skewnorm(self, data):

        data = data[~np.isnan(data)]  # fit function cannot handle NaN values
        a_fit, loc_fit, scale_fit = stats.skewnorm.fit(data)
        sn = stats.skewnorm(a_fit, loc_fit, scale_fit)
        return sn

    def hypothesis_testing(self):
        # slice max temp data
        self.Tmax_week_REF = self.Tmax_week[:'1980']
        self.Tmax_week_recent = self.Tmax_week['1981':]
        self.Tmax_on_date = self.Tmax_week[self.date]

        # fit a skew normal distribution to the reference data
        self.ref_dist = self.fit_skewnorm(self.Tmax_week_REF.values)
        p_val = self.ref_dist.sf(self.Tmax_on_date)

        return p_val

    def gen_plot(self, fig):

        ax = fig.subplots()
        # plot histograms, cannot use pandas functionality for web app
        bins = np.arange(31)*2-20
        ax.hist(self.Tmax_week_REF.values, density=True, bins=bins,
                alpha=.5, color='b', label=r'$T_{max}$ before 1980')
        ax.hist(self.Tmax_week_recent.values, density=True, bins=bins,
                histtype='step', lw=2, color='r', label=r'$T_{max}$ after 1980')

        # plot fitted ref distribution
        x = np.arange(600)*0.1-20  # all temps -20 to 40
        ax.plot(x, self.ref_dist.pdf(x), lw=2, c='b', label='REF PDF (fitted)')

        ax.axvline(x=self.Tmax_on_date, c='k', lw=2)

        # plot annotations
        ax.set_title(self.station.NAME+', ' + self.station.STATE +
                     ' on week of '+self.date.strftime('%b-%d'))

        annot_x = -20 if self.Tmax_on_date > 10 else 40
        annot_ha = 'left' if self.Tmax_on_date > 10 else 'right'

        ax.text(annot_x, .01, f'p-value: {self.p_val:5.3}', ha=annot_ha)
        ax.text(annot_x, .02, self.date.strftime(
            '%Y')+f': {self.Tmax_on_date:.1f}°', ha=annot_ha)

        ax.set_xlabel('Daily High Temperature °C')
        ax.legend()

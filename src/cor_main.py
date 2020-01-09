import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import scipy.stats as stats
from datetime import datetime,timedelta
from geopy.distance import great_circle
import geopandas as gpd

import climate_or_weather as cor

wr = cor.weatherRecord('New York Central Park','2019-07-21')

# y = tt.Tmax_week.values
# y = y[~np.isnan(y)]  
# ae, loce, scalee = stats.skewnorm.fit(y)   

# shapely_geo = gpd.tools.geocode('Denver, CO').iloc[0]
# latlon = (shapely_geo.geometry.y,shapely_geo.geometry.x)


# fig,ax=plt.subplots()
# ax.hist(tt.Tmax_week.values,bins=25,density=True)

# x = np.arange(600)*.1 - 10
# p = stats.skewnorm.pdf(x,ae, loce, scalee)
# ax.plot(x,p)
# plt.show()
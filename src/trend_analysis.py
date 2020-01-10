import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib

from climate_or_weather import WeatherRecord

matplotlib.rcParams.update({'font.size': 18})

loc = 'Denver, CO'
#loc = 'San Antonio, TX'
wr = WeatherRecord(loc, '2019-01-03')

year_dates = pd.date_range(start='2019-01-01', end='2019-12-31')

# --- CALCULATE DISTRIBUTION PARAMS EACH DAY OF YEAR ----
sn_params = []
for ts in year_dates:
    Tmax1_week = wr.series_select(ts, 'TMAX') * 0.1
    data_ref = Tmax1_week[:'1980'].values
    data_ref = data_ref[~np.isnan(data_ref)]
    a_fit, loc_fit, scale_fit = stats.skewnorm.fit(data_ref)
    sn_params.append((a_fit, loc_fit, scale_fit))

# ---- CALCULATE PVAL FOR EVERY DAY 1980-2020 -----
test_dates = pd.date_range(start='1980-01-01', end='2019-12-31')
p_vals = np.zeros(test_dates.size) + 0.5  # initialize p values to 0.5

for i, ts in enumerate(test_dates):
    if ts.dayofyear > 365:
        continue

    if ts not in wr.df.index:
        continue

    snp = sn_params[ts.dayofyear-1]
    sn = stats.skewnorm(snp[0], snp[1], snp[2])

    ts_temp = wr.df['TMAX'].loc[ts]*0.1

    p_vals[i] = sn.sf(ts_temp)

# np.save('pval.npy',p_vals)
#p_vals = np.load('pval.npy')

# --- GROUP BY YEAR ---
alpha = .02  # threshold for hypothesis test

years = np.arange(40) + 1980
p_high = np.zeros(40)
p_low = np.zeros(40)

for i, y in enumerate(years):
    p_vals_y = p_vals[test_dates.year == y]  # .values
    p_high[i] = np.where(p_vals_y < alpha)[0].size
    p_low[i] = np.where(p_vals_y > 1-alpha)[0].size


# ----- PLOT BAR CHART -----
fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(years, p_high, color='r')
ax.bar(years, -p_low, color='b')
ax.text(1992, 25, 'Hot Days (p_val < .02)')
ax.text(1992, -15, 'Cold Days (p_val > .98)')
ax.set_xlabel('Year')
ax.set_ylabel('# Days / Year')
ax.set_title('Hypothesis Testing every day 1980-2019 for '+loc)
plt.show()

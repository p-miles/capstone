import os
import pandas as pd

# Fixed width format - see readme
w_fwf = [12, 9, 10, 7, 3, 31, 4, 4, 6]
col_names = ['ID', 'LATITUDE', 'LONGITUDE',
             'ELEVATION', 'STATE', 'NAME', 'GSN', 'HCN', 'WMO']

df = pd.read_fwf('data/ghcnd-stations.txt', widths=w_fwf, names=col_names)

crn_stations = df['HCN'] == 'CRN'
usc_stations = df['ID'].str.startswith('USC')
usw_stations = df['ID'].str.startswith('USW')
df[(usc_stations | usw_stations) & crn_stations]


files = os.listdir('data/ghcnd_hcn')
stations = files.copy()

for i, file in enumerate(files):
    stations[i] = file.split('.')[0]

df = df[df.ID.isin(stations)]
df.to_pickle('data/df_hcn_stations.pkl')

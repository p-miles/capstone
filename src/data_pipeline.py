'''
Given a .dly file from NOAA GHCN database
Read the fixed-width formatted data into a pandas dataframe

Each line is a month of observations of a particular type 
(like temp or precip) which is not a user-friendly format.

Output will be a dataframe with datetime indices and column
names with observation code (i.e. TMAX, PRCP).
Most observations will be filled with NaN values because
historical data from long ago was typically only five core 
elements.

See data/readme.txt for full description.
'''

import numpy as np
import pandas as pd

def dly_process(dly_file):

    # Fixed width format - see readme
    w_fwf = [11,4,2,4]+[5,3]*31
    col_names = ['ID','YEAR','MONTH','ELEMENT']
    for i in range(31):
        col_names.extend([f'{i+1}',f'FLAG{i+1}'])

    df = pd.read_fwf(dly_file,widths=w_fwf,names=col_names)

    del df['ID'] # remove repetitive station identifier

    # eliminate flag columns, not concerned with data origin or quality
    vcol = [col for col in df.columns if 'FLAG' not in col]
    df = df.loc[:,vcol]

    # handle missing data with NaN
    df.replace(-9999, np.nan,inplace=True)


    # establish multiindex with existing rows before stack
    df.set_index(['ELEMENT','YEAR','MONTH'],inplace=True)
    # stack to rotate day-of-month columns into rows
    s = df.stack() # result is a series not a dataframe
    s.index.rename(['ELEMENT','YEAR','MONTH','DAY'],inplace=True)

    # use multi-index values to crudely convert to datetime format for greater flexibility
    y = s.index.get_level_values('YEAR')
    m = s.index.get_level_values('MONTH')
    d = s.index.get_level_values('DAY')

    dt = pd.to_datetime(y*10000+m*100+d.astype(int),format='%Y%m%d',errors='coerce')

    # set new multi-index with element and date
    s.index = [s.index.get_level_values('ELEMENT'),dt]
    s.index.rename(['ELEMENT','DATE'],inplace=True)
    df = s.to_frame(name='VALUE')

    # finally use pivot_table to put elements (i.e. TMAX, TMIN ) in columns
    df.reset_index()
    df = df.pivot_table(index='DATE',columns='ELEMENT',values = 'VALUE',fill_value = np.nan)

    return df
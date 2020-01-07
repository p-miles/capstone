import numpy as np
import pandas as pd

'''
ID            1-11   Character
YEAR         12-15   Integer
MONTH        16-17   Integer
ELEMENT      18-21   Character
VALUE1       22-26   Integer
MFLAG1       27-27   Character
QFLAG1       28-28   Character
SFLAG1       29-29   Character
VALUE2       30-34   Integer
MFLAG2       35-35   Character
QFLAG2       36-36   Character
SFLAG2       37-37   Character
  .           .          .
  .           .          .
  .           .          .
VALUE31    262-266   Integer
MFLAG31    267-267   Character
QFLAG31    268-268   Character
SFLAG31    269-269   Character
'''

w_fwf = [11,4,2,4]+[5,3]*31
n_fwf = ['ID','YEAR','MONTH','ELEMENT']
for i in range(31):
    n_fwf.extend([f'{i+1}',f'FLAG{i+1}'])

df = pd.read_fwf('data/USW00094728.dly',widths=w_fwf,names=n_fwf)

del df['ID'] # remove repetitive station identifier

# eliminate flag columns
vcol = [col for col in df.columns if 'FLAG' not in col]
df = df.loc[:,vcol]

# handle missing data natively
df.replace(-9999, np.nan)


# establish multiindex
df.set_index(['ELEMENT','YEAR','MONTH'],inplace=True)
s = df.stack()
s.index.rename(['ELEMENT','YEAR','MONTH','DAY'],inplace=True)

y = s.index.get_level_values('YEAR')
m = s.index.get_level_values('MONTH')
d = s.index.get_level_values('DAY')

dt = pd.to_datetime(y*10000+m*100+d.astype(int),format='%Y%m%d',errors='coerce')
s.index = [s.index.get_level_values('ELEMENT'),dt]
s.index.rename(['ELEMENT','DATE'],inplace=True)
df = s.to_frame(name='VALUE')
df.reset_index()
df1 = df.pivot_table(index='DATE',columns='ELEMENT',values = 'VALUE',fill_value = np.nan)

print(df1.columns)
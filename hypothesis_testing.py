
import pandas as pd
import matplotlib.pyplot as plt
import dly_ingest

dly_file = 'data/USW00094728.dly'

df = dly_ingest(dly_file)

TMAX1 = df.loc[df1.index.month == 1]['TMAX'] * 0.1

fig,ax = plt.subplots(figsize=(10,8))
TMAX1[:'1980'].hist(ax=ax,density=True,bins=np.arange(18)*2-15)
TMAX1['1981':].hist(ax=ax,alpha=0.5,density=True,bins=np.arange(18)*2-15)
plt.show()
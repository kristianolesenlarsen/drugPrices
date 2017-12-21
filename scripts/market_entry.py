import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime
import math
import numpy as np


from scripts import funcs



plt.style.use('bmh')
df = pd.read_csv('raw_data.csv')



# gather all the dates
df2 = funcs.gather(df, 'time', 'price', [c for c in df.columns if c.isdigit()])

# spread the prices
df3 = funcs.spread(df2, 'Variabel', 'price')

# create time variables
df3['time'] = pd.to_datetime(df3['time'])
df3['date'] = df3['time'].apply(lambda x: datetime.date(x.year, x.month, x.day))
df3['rep'] = df3['aup']/df3['aip']

df3['t'] = funcs.dummy(df3['aip'])
df3['t'] = df3.groupby('ATC_kode', group_keys = False).apply(lambda x: x.t.cumsum())


for t,g in df3.groupby('ATC_kode'):
         plt.plot(g.t, g.rep, alpha = 0.3)

plt.savefig('test.png', dpi = 1000)
plt.show()


for t,g in df3.groupby(['Firma']):
         plt.scatter(g.t, g.rep, alpha = 0.1, s = g.rep)
         plt.scatter(g.t, g.rep, alpha = 0.1, s = g.rep)

plt.savefig('test2.png', dpi = 1000)
plt.show()

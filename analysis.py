import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates

plt.style.use('bmh')
df = pd.read_csv('raw_data.csv')



# define spread and gather functions like in R
def gather(df, key, value, cols):
    """ Mimic the tidyr::gather function
    """
    id_vars = [col for col in df.columns if col not in cols]
    return pd.melt(df, id_vars, cols, key, value)

def spread(df, key, value):
    """ mimic the tidyr::spread function
    """
    keep_cols = [col for col in df.columns if col not in [key, value]]
    return df.pivot_table(index = keep_cols, columns = key, values = value).reset_index().rename_axis(None, axis=1)


# gather all the dates
df2 = gather(df, 'time', 'price', [c for c in df.columns if c.isdigit()])

# spread the prices
df3 = spread(df2, 'Variabel', 'price')

# create time variables
df3['time'] = pd.to_datetime(df3['time'])
df3['date'] = df3['time'].apply(lambda x: datetime.date(x.year, x.month, x.day))

# PLOT SIMPLE AVERAGES
# this simply replicates the work also done in descriptive.R
plt.plot(df3.groupby('date')['aip'].mean().reset_index()['date'],
         df3.groupby('date')['aip'].mean().reset_index()['aip'],
         label = 'AIP')
plt.plot(df3.groupby('date')['aup'].mean().reset_index()['date'],
         df3.groupby('date')['aup'].mean().reset_index()['aup'],
         label = "AUP")
plt.title('Medicine prices over time\n')
plt.legend(loc = 3)
plt.ylabel('Price (DKK)')
plt.xlabel('Year')
plt.savefig('img/averages.png')
plt.show()

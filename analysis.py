import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates
import datetime
import math
import numpy as np
from sklearn import linear_model as lm


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


# rework this to handle panel data!
def diff(col, index, D):
    """ return a dataframe with nth differenced vectors
    args:
        col: a column to difference
        L: list or int indicating which differences to return
    """
    out = {'index': index,
           'value': col}

    # this just ensures L is a list
    if type(D) == int:
        D = [D]

    for diff in D:
        diffed = [i - di for i, di in zip(col[diff:], col[:-diff])]
        # insert NaN's in the beginning of the column
        for i in range(len(diffed),len(col)):
            diffed.insert(0, np.nan)
        # add the lag to out dict
        out['L' + str(diff)] = diffed

    return pd.DataFrame(out)


def lag(col, index, L):
    """ return a dataframe with nth lagged vectors
    args:
        col: a column to lag
        L: list or int indicating which lags to return
    """
    out = {'index': index,
           'value': col}

    # this just ensures L is a list
    if type(L) == int:
        L = [L]

    for lag in L:
        lagged = col.tolist()[:-lag]

        for i in range(len(lagged), len(col)):
            lagged.insert(0, np.nan)

        out['L' + str(lag)] = lagged

    return pd.DataFrame(out)


# gather all the dates
df2 = gather(df, 'time', 'price', [c for c in df.columns if c.isdigit()])

# spread the prices
df3 = spread(df2, 'Variabel', 'price')

# create time variables
df3['time'] = pd.to_datetime(df3['time'])
df3['date'] = df3['time'].apply(lambda x: datetime.date(x.year, x.month, x.day))


# these operations create a dataset of first differenced AIP prices
df41 = df3.groupby('date')['aip'].mean().reset_index()

dfdiff = diff(df41['aip'], df41['date'], range(1,10))
dflag = lag(dfdiff['L1'], dfdiff['index'], range(1,10))[10:]



# PLOT SIMPLE AVERAGES
# this simply replicates the work also done in descriptive.R

def plot_simple():
    fig = plt.figure(1)
    plt.rc('text', usetex = True)

    ax1 = plt.subplot2grid((3,1), (0,0), rowspan = 2)
    ax2 = plt.subplot2grid((3,1), (2,0), rowspan = 1, sharex = ax1)
    ax1.set_title(r'Medicine prices over time')

    ax2.plot(
        dflag['index'],
        dflag['L1'],
        label = r'$\Delta$AUP'
    )

    ax1.set_ylabel(r'DKK')

    ax2.plot(dflag['index'],
            [np.mean(dflag['L1']) for i in dflag['index']],
            color = 'r',
            linestyle = ':')

    ax1.plot(df3.groupby('date')['aip'].mean().reset_index()['date'],
             df3.groupby('date')['aip'].mean().reset_index()['aip'],
             label = r'AIP')
    ax1.plot(df3.groupby('date')['aup'].mean().reset_index()['date'],
             df3.groupby('date')['aup'].mean().reset_index()['aup'],
             label = r'AUP')

    # remove x axis marks for large figure
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1.legend(loc = 4)
    ax2.legend(loc = 2)

    fig.tight_layout()
    plt.savefig('averages.png')
    plt.show()

plot_simple()

# Plot profit margin of the pharmacies
df3['relPrice'] = df3['aup']/df3['aip']

plt.plot(df3.groupby('date')['relPrice'].mean().reset_index()['date'],
         df3.groupby('date')['relPrice'].mean().reset_index()['relPrice'],
         label = "AUP/AIP")
plt.title("Profit margin")
plt.xlabel('Year')
plt.ylabel('margin [100ths]')
plt.legend(loc = 3)
plt.show()


# plot prices against each other
df3['log_aip'] = df3['aip'].apply(lambda x: math.log(x))
df3['log_aup'] = df3['aup'].apply(lambda x: math.log(x))

plt.scatter(df3.groupby('date')['log_aup'].mean().reset_index()['log_aup'],
         df3.groupby('date')['log_aip'].mean().reset_index()['log_aip'],
         edgecolors = 'b',
         facecolors = "None")

plt.show()

import pandas as pd
import math
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



def dummy(series):
    out = []
    for idx, val in enumerate(series):
        if math.isnan(val):
            out.append(0)
        else:
             out.append(1)
    return out

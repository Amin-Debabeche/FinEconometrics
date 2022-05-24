### Fast Fourier Transform on Sentiment Analyses

from scipy.fftpack import fft, ifft


def fourier(df, n_dimensions):
    for n in n_dimensions:
        n = round(n)
        tmp_ = fft(df['compound'].values)
        tmp_[n:-n] = 0
        df['fourier_'+str(n)] = ifft(tmp_)
    return df


l = len(Twitter_preprocessed_data)
Twitter_preprocessed_data = fourier(Twitter_preprocessed_data, np.linspace(round(l*0.1), round(l*0.9), 5))

Twitter_preprocessed_data.to_pickle(DATA_DIR+'/clean/Global_df')

def merged_df(df, df_tickers, column='compound', freq='D', var=1.1):
    final_df = pd.DataFrame()

    df['final_compound'] = df.score**var * df[column]
    final_df['final_compound'] = df.groupby(
        df['created_utc'].dt.to_period(freq)).final_compound.mean()
    final_df.index = final_df.index.to_timestamp()
    final_df = pd.merge(final_df, df_tickers, left_index=True, right_index=True)     # .dropna(subset=["final_compound"], inplace=True)

    return final_df

final_df = merged_df(Twitter_preprocessed_data, bitcoin price)

final_df.to_pickle(DATA_DIR+f'/clean/Final_df')

### Splitting

from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(gap=0, max_train_size=0.8, n_splits=3, test_size=0.1)

X = final_df.final_compound
y = final_df.SPY #for SPY
# plt.hist(y.value_counts(normalize=True, bins=20))

for train_index, test_index in tscv.split(X):

    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

import pandas as pd
import glob

#print(glob.glob("/home/jovyan/*"))
#allFiles = glob.glob("/home/jovyan/work/data/all_0000000000*")
allFiles = glob.glob("data/all_0000000000*")

print(allFiles)
data = pd.DataFrame()
list_ = []
for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)
data = pd.concat(list_)

def filter_train_type(df=[],
                      train_types=[],
                      sum_types = False,
                      sum_columns=['train_count', 'delay', 'total_delay'],
                      aggs={'pressure': 'max',
                            'max_temperature': 'max',
                            'min_temperature': 'min',
                            'mean_temperature': 'mean',
                            'mean_dewpoint': 'mean',
                            'mean_humidity': 'mean',
                            'mean_winddirection': 'mean',
                            'mean_windspeed': 'mean',
                            'max_windspeedms': 'max',
                            'max_windgust': 'max',
                            'max_precipitation1h': 'max',
                            'max_snowdpeth': 'max',
                            'max_n': 'max',
                            'min_vis': 'min',
                            'min_clhb': 'min',
                            'max_precipitation3h': 'max',
                            'max_precipitation6h': 'max'}):
    """
    Filter traintypes from metadata

    train_types     : list
                      list of following options: [0,1,2,3]

                      train_types = {'K': 0,
                                     'L': 1,
                                     'T': 2,
                                     'M': 3}
    sum_types       : bool
                     if True, sum different train types together (default False)

    returns : np array, np array
              labels metadata, labels
    """

    if len(df) == 0:
        return df

    mask = df.loc[:,'train_type'].isin(train_types)
    filt_df = df[(mask)]

    if sum_types:
        d = {}
        for col in sum_columns:
            d[col] = ['sum']
        for col,method in aggs.items():
            d[col] = [method]
        if 'lat' in df:
            d['lat'] = ['max']
        if 'lon' in df:
            d['lon'] = ['max']

        filt_df = filt_df.groupby(['trainstation', 'time'], as_index=False).agg(d)

        filt_df.columns = filt_df.columns.droplevel(1)
        filt_df.drop_duplicates(['trainstation', 'time'], inplace=True)

    return filt_df

data_filt = filter_train_type(data, ['K', 'L'])

data_filt.sort_values(by=['time', 'trainstation'], inplace=True)

data_hki = data.loc[:, data['trainstation'] == 'HKI']
print(data_hki)
data_filt.to_csv('data/hki_all.csv', encoding='utf-8')

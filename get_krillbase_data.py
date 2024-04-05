import pandas as pd
import numpy as np
import os
from datetime import datetime


class Files:
    def __init__(self, kbase_path):
        self.kbase_data = kbase_path + 'krillbase.csv'
        self.dates = kbase_path + 'dates.npy'


class Data:

    def __init__(self, files):
        self.table = pd.read_table(files.kbase_data, sep=',')
        self.density = np.array(self.table.iloc[0:-1, 12])
        self.lat = np.array(self.table.iloc[0:-1, 2])
        self.lon = np.array(self.table.iloc[0:-1, 3])
        self.day_night = np.array(self.table.iloc[0:-1, 5])

        if not os.path.exists(files.dates):
            self.date = self.table.iloc[0:-1, 4]
            self.save_times(files)
            print('Saving times to npy file: ' + files.dates)

        date_file = np.load(files.dates)
        self.day = date_file[:, 0]
        self.month = date_file[:, 1]
        self.year = date_file[:, 2]

    def save_times(self, files):
        date_mat = np.zeros([np.shape(self.date)[0], 3])
        for i in range(0, np.shape(self.date)[0]):
            t_i = datetime.strptime(self.date[i], '%d-%b-%Y')
            date_mat[i, 0] = t_i.day
            date_mat[i, 1] = t_i.month
            date_mat[i, 2] = t_i.year
        np.save(files.dates, date_mat)
        return


class DataTime:

    def __init__(self, data, month_start, month_end, year):
        # Accepts

        id_year = (data.year == year)
        id_month = (data.month >= month_start) & (data.month <= month_end)
        idx = id_month & id_year

        self.density = data.density[idx]
        self.lat = data.lat[idx]
        self.lon = data.lon[idx]
        self.day_night = data.day_night[idx]
        self.day = data.day[idx]
        self.month = data.month[idx]
        self.year = data.year[idx]
        return





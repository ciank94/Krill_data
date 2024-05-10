import pandas as pd
import numpy as np
import os
from datetime import datetime
import geopandas as gpd
import numpy as np
from shapely.ops import nearest_points
from shapely.geometry import Point

class FilesKB:
    def __init__(self, kbase_path):
        self.kbase_data = kbase_path + 'krillbase.csv'
        self.dates = kbase_path + 'dates.npy'
        self.coast = kbase_path + 'CMEMS/' + 'ant_coastline.shp'


class DataKB:

    def __init__(self, files, year_start, year_end):
        self.table = pd.read_table(files.kbase_data, sep=',', encoding='unicode_escape')
        density = np.array(self.table.iloc[0:-1, 25])
        lat = np.array(self.table.iloc[0:-1, 4])
        lon = np.array(self.table.iloc[0:-1, 5])
        day_night = np.array(self.table.iloc[0:-1, 12])
        bath = np.array(self.table.iloc[0:-1, 20])

        if not os.path.exists(files.dates):
            self.date = self.table.iloc[0:-1, 8]
            self.save_times(files)
            print('Saving times to npy file: ' + files.dates)

        date_file = np.load(files.dates)
        day = date_file[:, 0]
        month = date_file[:, 1]
        year = date_file[:, 2]

        # Index data for years and valid data
        id_year = (year >= year_start) & (year <= year_end)
        id_invalid = ~np.isnan(density)
        idx = id_year & id_invalid

        self.day = day[idx]
        self.month = month[idx]
        self.year = year[idx]
        self.density = density[idx]
        self.lat = lat[idx]
        self.lon = lon[idx]
        self.day_night = day_night[idx]
        id_day = self.day_night == 'day'
        id_night = self.day_night == 'night'
        self.day_night[id_day] = 1
        self.day_night[id_night] = 0
        self.bath = bath[idx]
        return

    def save_times(self, files):
        date_mat = np.zeros([np.shape(self.date)[0], 3])
        for i in range(0, np.shape(self.date)[0]):
            t_i = datetime.strptime(self.date[i], '%d/%m/%Y')
            date_mat[i, 0] = t_i.day
            date_mat[i, 1] = t_i.month
            date_mat[i, 2] = t_i.year
        np.save(files.dates, date_mat)
        return







import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os


class Read:
    def __init__(self, folder, file):
        self.folder = folder
        self.file = file
        self.df = pd.read_csv(self.file, sep=',')
        self.vars = self.df.columns
        self.time_file = self.folder + 'time.npy' # Store times in a numpy array
        if not os.path.exists(self.time_file):
            self.get_time()
            print('Saving ' + self.time_file)
        else:
            print(self.time_file + ' exists')
        self.time = np.load(self.time_file)
        self.hour = self.time[:, 0].astype(int)
        self.day = self.time[:, 1].astype(int)
        self.month = self.time[:, 2].astype(int)
        self.year = self.time[:, 3].astype(int)

    def get_time(self):
        time_array = self.df.datetime_haul_start
        shp_t = np.shape(time_array)[0]
        time_store = np.zeros([shp_t, 4])

        for i in range(0, shp_t):
            d1 = datetime.strptime(time_array[i], "%Y-%m-%d %H:%M:%S")
            time_store[i, 0] = d1.hour
            time_store[i, 1] = d1.day
            time_store[i, 2] = d1.month
            time_store[i, 3] = d1.year

        np.save(self.time_file, time_store)
        return

    def subset(self, sub_rule):
        #make subset rule into a dictionary
        if sub_rule == "None":
            df = self.df
            self.get_var_subset(df)
        #if sub_rule == "SG":
         #   r1 = self.df.asd_code == 483

        #if sub_rule == "2014":
         #   r2 = self.time[:, 3] == 2014
          #  df = self.df[r1]

    def get_var_subset(self, df):
        #Pull important variables:
        self.lat = df.latitude_haul_start
        self.lon = df.longitude_haul_start
        self.time = df.datetime_haul_start
        self.weight_kg = df.krill_greenweight_kg
        self.weight_log = np.log10(self.weight_kg)
        self.depth_bottom = df.depth_bottom_haul_start_m
        self.gear_depth = df.depth_gear_haul_start_m
        return

    def save_plot(self, save_name):
        savefile = self.folder + save_name + '.png'
        #plt.title(save_name)
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return

    def summary_plots(self):
        fig, ax = plt.subplots()
        ax.hist(self.year)
        ax.set_xlabel('year')
        range_x = np.arange(np.min(self.year), np.max(self.year), 2)
        plt.xticks(range_x)
        self.save_plot('Fishing_years')

        fig, ax = plt.subplots()
        ax.hist(self.month)
        ax.set_xlabel('month')
        self.save_plot('Fishing_months')

        fig, ax = plt.subplots()
        ax.hist(self.day)
        ax.set_xlabel('day')
        self.save_plot('Fishing_days')

        fig, ax = plt.subplots()
        ax.hist(self.hour)
        ax.set_xlabel('hour')
        self.save_plot('Fishing_hours')

        fig, ax = plt.subplots()
        ax.hist(self.weight_kg)
        ax.set_xlabel('weight_kg')
        self.save_plot('Catch_kg')

        fig, ax = plt.subplots()
        ax.hist(self.weight_log)
        ax.set_xlabel('weight_kg_log10')
        self.save_plot('Catch_kg_log10')

        fig, ax = plt.subplots()
        id1 = self.depth_bottom <= 2000
        ax.hist(self.depth_bottom[id1])
        ax.set_xlabel('bottom_depth')
        self.save_plot('Bottom_depth')

        fig, ax = plt.subplots()
        ax.hist(self.gear_depth)
        ax.set_xlabel('gear_depth')
        self.save_plot('Gear_depth')
        return




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
        self.sub_rule = sub_rule
        if sub_rule == "ALL":
            self.r1 = np.ones(np.shape(self.df)[0]).astype(bool)
            df = self.df
            self.get_var_subset(df)
        elif sub_rule == "SG":
            self.r1 = self.df.asd_code == 483
            df = self.df[self.r1]
            self.get_var_subset(df)
        elif sub_rule == "SO":
            self.r1 = self.df.asd_code == 482
            df = self.df[self.r1]
            self.get_var_subset(df)
        elif sub_rule == "AP":
            self.r1 = self.df.asd_code == 481
            df = self.df[self.r1]
            self.get_var_subset(df)
        else:
            print('Invalid subset rule')


        #if sub_rule == "2014":
         #   r2 = self.time[:, 3] == 2014
          #  df = self.df[r1]

    def get_var_subset(self, df):
        #Pull important variables:
        self.lat = df.latitude_haul_start
        self.lon = df.longitude_haul_start
        self.time_haul = df.datetime_haul_start
        self.weight_kg = df.krill_greenweight_kg
        self.weight_log = np.log10(self.weight_kg)
        self.depth_bottom = df.depth_bottom_haul_start_m
        self.gear_depth = df.depth_gear_haul_start_m
        self.year = self.year[self.r1]
        self.month = self.month[self.r1]
        self.day = self.day[self.r1]
        self.hour = self.hour[self.r1]
        return

    def save_plot(self, save_name):
        savefile = self.folder + save_name + '.png'
        plt.title(self.sub_rule)
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return

    def summary_plots(self):

        plt_n = self.sub_rule + '_'

        fig, ax = plt.subplots()
        ax.hist(self.year)
        ax.set_xlabel('year')
        range_x = np.arange(np.min(self.year), np.max(self.year), 2)
        plt.xticks(range_x)
        self.save_plot(plt_n + 'Fishing_years')

        fig, ax = plt.subplots()
        ax.hist(self.month)
        ax.set_xlabel('month')
        self.save_plot(plt_n + 'Fishing_months')

        fig, ax = plt.subplots()
        ax.hist(self.day)
        ax.set_xlabel('day')
        self.save_plot(plt_n +'Fishing_days')

        fig, ax = plt.subplots()
        ax.hist(self.hour)
        ax.set_xlabel('hour')
        self.save_plot(plt_n +'Fishing_hours')

        fig, ax = plt.subplots()
        ax.hist(self.weight_kg)
        ax.set_xlabel('weight_kg')
        self.save_plot(plt_n +'Catch_kg')

        fig, ax = plt.subplots()
        ax.hist(self.weight_log)
        ax.set_xlabel('weight_kg_log10')
        self.save_plot(plt_n +'Catch_kg_log10')

        fig, ax = plt.subplots()
        id1 = self.depth_bottom <= 2000
        ax.hist(self.depth_bottom[id1])
        ax.set_xlabel('bottom_depth')
        self.save_plot(plt_n +'Bottom_depth')

        fig, ax = plt.subplots()
        ax.hist(self.gear_depth)
        ax.set_xlabel('gear_depth')
        self.save_plot(plt_n +'Gear_depth')
        return

    def summary_catch(self):
        # subset data for each instance
        yrs = np.unique(self.year).astype(int)
        shp_y = np.shape(yrs)[0]
        n_catches = np.zeros(shp_y)
        avg_catch = np.zeros(shp_y)
        std_catch = np.zeros(shp_y)
        for i in range(0, shp_y):
            id_y = self.year == yrs[i]
            w_kg = self.weight_kg[id_y]
            avg_catch[i] = np.mean(w_kg) / 1000
            std_catch[i] = np.std(w_kg) / 1000
            n_catches[i] = np.shape(w_kg)[0]

        axis1_title = 'Number of catch events'
        axis2_title = 'Mean catch (tonnes)'
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        ax2.set_ylabel(axis1_title, color='b', fontsize=13)
        ax1.bar(yrs, n_catches, facecolor='#2ab0ff', edgecolor='#169acf', linewidth=0.5, alpha=0.75)
        ax2.scatter(yrs, avg_catch, c='r', linewidth=5, s=3)
        plt.errorbar(yrs, avg_catch, yerr=std_catch, color="r", alpha=0.5)

        range_x = np.arange(np.min(self.year), np.max(self.year)+1, 2)
        plt.xticks(range_x)


        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        ax2.set_ylabel(axis2_title, color='r', fontsize=13)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax1.set_xlabel('Years', fontsize=13)
        plt.grid(alpha=0.45)  # nice and clean grid
        self.save_plot(save_name=self.sub_rule + '_avg_catches_years')


        months = np.unique(self.month).astype(int)
        shp_m = np.shape(months)[0]
        n_catches = np.zeros(shp_m)
        avg_catch = np.zeros(shp_m)
        std_catch = np.zeros(shp_m)
        for i in range(0, shp_m):
            id_m = self.month == months[i]
            w_kg = self.weight_kg[id_m]
            avg_catch[i] = np.mean(w_kg) / 1000
            std_catch[i] = np.std(w_kg) / 1000
            n_catches[i] = np.shape(w_kg)[0]

        axis1_title = 'Number of catch events'
        axis2_title = 'Mean catch (tonnes)'
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        ax2.set_ylabel(axis1_title, color='b', fontsize=13)
        ax1.bar(months, n_catches, facecolor='#2ab0ff', edgecolor='#169acf', linewidth=0.5, alpha=0.75)
        ax2.scatter(months, avg_catch, c='r', linewidth=5, s=3)
        plt.errorbar(months, avg_catch, yerr=std_catch, color="r", alpha=0.5)

        range_x = np.arange(1, 12+1, 1)
        plt.xticks(range_x)

        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        ax2.set_ylabel(axis2_title, color='r', fontsize=13)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax2.tick_params(axis='y', labelsize=10)
        ax1.set_xlabel('Months', fontsize=13)
        plt.grid(alpha=0.45)  # nice and clean grid

        self.save_plot(save_name=self.sub_rule + '_avg_catches_months')


        #gear depth
        #g_depth = np.unique(self.gear_depth)
        axis1_title = 'Number of catch events'
        fig, ax1 = plt.subplots()
        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        id1 = self.gear_depth <= 400
        ax1.hist(self.gear_depth[id1], facecolor='#2ab0ff', edgecolor='#169acf', alpha=0.75)
        range_x = np.arange(0, 400 + 1, 50)
        plt.xticks(range_x)
        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.set_xlabel('Gear_depth', fontsize=13)
        plt.grid(alpha=0.45)  # nice and clean grid

        self.save_plot(save_name=self.sub_rule + '_avg_catches_gear_depth')

        # gear depth
        # g_depth = np.unique(self.gear_depth)

        axis1_title = 'Number of catch events'
        fig, ax1 = plt.subplots()
        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        id1 = self.depth_bottom <= 2000
        ax1.hist(self.depth_bottom[id1], facecolor='#2ab0ff', edgecolor='#169acf', alpha=0.75)
        range_x = np.arange(0, 2000 + 1, 250)
        plt.xticks(range_x)
        ax1.set_ylabel(axis1_title, color='b', fontsize=13)
        ax1.tick_params(axis='x', labelsize=10)
        ax1.tick_params(axis='y', labelsize=10)
        ax1.set_xlabel('Bottom_depth', fontsize=13)
        plt.grid(alpha=0.45)  # nice and clean grid
        self.save_plot(save_name=self.sub_rule + '_avg_catches_bottom_depth')





        return



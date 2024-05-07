import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def combine_files(folder, summary_f):
    file_list = os.listdir(summary_f)
    shp_f = np.shape(file_list)[0]

    df_list = []
    for i in range(1,shp_f):
        fl_val = file_list[i]
        f_name = summary_f + fl_val
        table = pd.read_csv(f_name, sep=',')
        df_list.append(table)


    # Concatenate all data into one DataFrame
    combo_df = pd.concat(df_list, ignore_index=True)

    # Save the final result to a new CSV file
    save_name = 'summary_file.csv'
    combo_df.to_csv(os.path.join(folder, save_name), index=False)

    print('Saving: ' + folder + save_name)
    return

def read_table(folder):
    file = folder + 'summary_file.csv'
    table = pd.read_csv(file, sep=',')
    times = table.starttime
    time_vals = np.zeros(np.shape(times)[0])
    for i in range(0, np.shape(times)[0]):
        if i == 0:
            time_vals[i] = 0
            t1 = datetime.strptime(times[i], "%Y-%m-%d %H:%M:%S")
        else:
            t2 = datetime.strptime(times[i], "%Y-%m-%d %H:%M:%S")
            t_v = t2 - t1
            time_vals[i] = t_v.seconds
            t1 = t2

    time_vals = time_vals / 60
    time_vals[time_vals > 100] = np.nan
    lats = table.lat
    lons = table.lon
    depth = table.krill_cog_depth
    krill_nasc = table.krill_nasc

    fig, ax = plt.subplots()
    plt.hist(lats)
    save_plot('lats')

    fig, ax = plt.subplots()
    plt.hist(lons)
    save_plot('lons')

    fig, ax = plt.subplots()
    plt.hist(depth)
    save_plot('depth')

    fig, ax = plt.subplots()
    plt.hist(krill_nasc)
    save_plot('krill_nasc')

def save_plot(save_name):
    savefile = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/Akbm/' + save_name + '.png'
    plt.title(save_name)
    print('Saving file: ' + savefile)
    plt.savefig(savefile, dpi=400)
    plt.close()
    return

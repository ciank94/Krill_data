from plot_gfw import Plot
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np


folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/GFWR/'

vessel_name1 = 'SAGA SEA'
file = folder + vessel_name1 + '.csv'
table = pd.read_csv(file, sep=',')
lat1 = table.iloc[:, 0]
lon1 = table.iloc[:, 1]
c1 = np.zeros(np.shape(lon1)[0])

vessel_name2 = 'ANTARCTIC ENDURANCE'
file2 = folder + vessel_name2 + '.csv'
table2 = pd.read_csv(file2, sep=',')
lat2 = table2.iloc[:, 0]
lon2 = table2.iloc[:, 1]
c2 = np.zeros(np.shape(lon2)[0]) + 1
#todo: for the unique values in c1 and c2- plot individual vessels- with a name for each- could compress -
#todo: identifier of vessel from their name;
lat = pd.concat([lat1, lat2])
lon = pd.concat([lon1, lon2])
c_v = np.concatenate([c1, c2])
vessel_names = [vessel_name1, vessel_name2]

region = "SG"
p1 = Plot(region)
p1.plot_points(lon, lat, c_v, vessel_names)
breakpoint()
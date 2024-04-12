from fuse_data import fuse_data
import sklearn

# paths
kbase_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/'
cmems_path = kbase_path + 'CMEMS/'

# Specify cmems data id and range
data_id = "cmems_mod_glo_bgc_my_0.25_P1M-m"  # monthly data
y1 = "1993"  # Start year
y2 = "2016"  # End year

data = fuse_data(cmems_path, kbase_path, data_id, y1, y2)
breakpoint()


# import matplotlib.pyplot as plt

import numpy as np

breakpoint()
x = data.x
y = data.y


from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

from sklearn.datasets import load_iris
tree_clf = DecisionTreeClassifier(max_depth=10)
tree_clf.fit(x, y)
# chl = data_cm.chl[1, 0, :, :]
#
#
#
breakpoint()
# breakpoint()

# lonW=-70
# lonE=-20
# latS=-70
# latN=-50
# coordinates = (lonW, lonE, latS, latN)
# m = Basemap(llcrnrlon=coordinates[0], llcrnrlat=coordinates[2],
#                 urcrnrlon=coordinates[1], urcrnrlat=coordinates[3],
#                 resolution='i')
# m.drawcoastlines(linewidth=.5)
# m.drawmeridians(np.arange(-180., 180., 10.), labels=[False, False, False, True])
# m.drawparallels(np.arange(-90., 90., 4.), labels=[True, False, False, False])
# m.scatter(dataset.lon, dataset.lat, 5, color='r')
#     #m.etopo()
# m.shadedrelief()
# x, y = m(lon1, lat1)
# plt.pcolormesh(x, y, df3[df3>0])
# plt.colorbar(orientation='horizontal')
#
# m.scatter(x, y, 3, marker='o', color='r')
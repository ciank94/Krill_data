from fuse_data import fuse_data
from ml_methods import ML
import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import sklearn

# paths
kbase_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/Krillbase/'
cmems_path = kbase_path + 'CMEMS/'

# Specify cmems data id and range
data_id = "cmems_mod_glo_bgc_my_0.25_P1M-m"  # monthly data
#data_id2 = "cmems_mod_glo_phy_anfc_0.083deg_P1M-m" #monthly data on sea ice etc.
y1 = "1993"  # Start year
y2 = "2016"  # End year

#fuse data sets
data = fuse_data(cmems_path, kbase_path, data_id, y1, y2)

# adjust features
ml = ML(data)
ml.feature_scaling()

# Type of analysis
regressor = "Decision_Tree"
ml.get_regressor(regressor)
#ml.grid_search()
ml.scores()
ml.map_predictions(data, cmems_path)


#breakpoint()

#ml.split_train_test_reg(test_ratio=0.2)







#todo: plot out longitude, latitude, depth, chl and other predictor variables as histograms;
#todo: correlation coefficient for predictor variables, best estimator_importances- RandomForestRegressor
#todo: scatter matrix function: used to find correlations between attributes;
#todo: plots to show: actual vs. predicted; predictor vs. response, map of data for SG (cartopy), and so on;

# Split dataset for training and cross-validate



# tree_reg.fit(ml.x, ml.y)
# plt.scatter(tree_reg.predict(ml.x), ml.y)
# plt.show()
# ml.hist_data()
#
# regressor_name = "Decision_Tree"
# ml.get_classifier(classifier_name)
#
# breakpoint()
#
# ml.feature_scaling()
#
# # split training & test sets:
# ml.split_train_test(0.2)
#
# # define classifier
# #classifier_name = "SGDClassifier"
# classifier_name = "Decision_Tree"
# ml.get_classifier(classifier_name)
#
# # classifier metrics:
# ml.precision_metrics()
# ml.precision_recall_curve()
# ml.map_predictions(data)
# breakpoint()
#
#
# nc_file = nc.Dataset(cmems_path + 'gebco_2023.nc')
# elevation = np.array(nc_file.variables["elevation"]).astype(float)
# elevation[elevation>0] = np.nan
# elevation[elevation<-20000] = np.nan
# lat = nc_file.variables["lat"]
# breakpoint()
#
#
#
#
#
# ml.map_output()

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
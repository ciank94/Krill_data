from fuse_data import fuse_data
from ml_methods import ML
import sklearn

# paths
kbase_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/'
cmems_path = kbase_path + 'CMEMS/'

# Specify cmems data id and range
data_id = "cmems_mod_glo_bgc_my_0.25_P1M-m"  # monthly data
y1 = "1993"  # Start year
y2 = "2016"  # End year

data = fuse_data(cmems_path, kbase_path, data_id, y1, y2)


ml = ML(data)
ml.feature_scaling()
ml.split_train_test(0.2)

from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_curve, precision_score, recall_score
import matplotlib.pyplot as plt
import numpy as np
sgd_clf = SGDClassifier(random_state=35)
sgd_clf.fit(ml.train_x, ml.train_y)
sgd_clf.decision_function([ml.train_x[0, :]])
y_pred = cross_val_predict(sgd_clf, ml.train_x, ml.train_y, cv=10)
con_mat = confusion_matrix(ml.train_y, y_pred)
negative_act = con_mat[0,:]
positive_act = con_mat[1,:]
tn = negative_act[0]
fp = negative_act[1]
fn = positive_act[0]
tp = positive_act[1]
precision = tp/(tp + fp)
recall_tpr = tp/(tp + fn)
specificity_tnr = tn/(tn + fp)
fpr = 1 - specificity_tnr

print(precision, recall_tpr, specificity_tnr, fpr)  # 1 1 1 1
y_scores = cross_val_predict(sgd_clf, ml.train_x, ml.train_y, cv=10, method="decision_function")
precisions, recalls, thresholds = precision_recall_curve(ml.train_y, y_scores)
plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
plt.plot(thresholds, recalls[:-1], "k-", label="Recall")
plt.xlabel("Threshold")
plt.legend(loc="center left")
plt.ylim([0,1])
plt.show()
plt.figure()
plt.plot(recalls, precisions)
plt.show()
print(y_scores)
print(thresholds)
breakpoint()
ml.decision_function(sgd_clf)

y_pred = sgd_clf.predict(ml.test_x)
y_train_pred = sgd_clf.predict(ml.train_x)
n_correct = sum(y_pred == ml.test_y)
confusion_matrix(ml.test_y, y_pred)
confusion_matrix(ml.train_y, y_train_pred)
print(n_correct/len(y_pred))
breakpoint()
cross_val_score(sgd_clf, ml.train_x, ml.train_y, cv = 10, scoring = "accuracy")
breakpoint()


# import matplotlib.pyplot as plt

import numpy as np


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
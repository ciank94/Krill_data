import netCDF4
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, precision_recall_curve
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import mean_squared_error


class ML:

    def __init__(self, data):
        self.final_model = None
        self.regressor = None
        self.regressor_name = None
        self.fitmod = None
        self.test_y = None
        self.test_x = None
        self.train_y = None
        self.train_x = None
        self.classifier = None
        self.classifier_name = None
        self.f_names = data.f_names
        self.results_folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/Krillbase/results/'
        self.cmems_folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/Krillbase/CMEMS/'
        self.x = data.x
        self.y = data.y

        return

    def feature_scaling(self):
        temp_v = np.zeros(np.shape(self.x)[0])
        for i in range(0, np.shape(self.x)[1]):
            id_1 = self.x[:, i] > 1e06
            temp_v[id_1] = np.median(self.x[:, i])
            temp_v[~id_1] = self.x[~id_1, i]
            temp_v = (temp_v - np.mean(temp_v))/np.std(temp_v)
            self.x[:, i] = temp_v
        return

    def get_regressor(self, regressor_name):
        rand_state = 37
        max_tree = 8
        self.regressor_name = regressor_name
        if self.regressor_name == "SGD":
            from sklearn.linear_model import SGDRegressor
            self.regressor = SGDRegressor(random_state=rand_state)
        elif self.regressor_name == "Decision_Tree":
            from sklearn.tree import DecisionTreeRegressor
            self.regressor = DecisionTreeRegressor(random_state=rand_state, max_depth=max_tree)
        elif self.regressor_name == "LinReg":
            from sklearn.linear_model import LinearRegression
            self.regressor = LinearRegression()
        elif self.regressor_name == "RandomForest":
            from sklearn.ensemble import RandomForestRegressor
            self.regressor = RandomForestRegressor()
        else:
            print("Not a valid regressor name")
        return

    def fit_regressor(self):
        self.regressor.fit(self.x, self.y)
        return

    def scores(self):
        self.fit_regressor()
        save_file = self.results_folder + self.regressor_name + '_scores.txt'
        from sklearn.model_selection import cross_val_score
        scores = cross_val_score(self.regressor, self.x, self.y, scoring="neg_mean_squared_error", cv=10)
        tree_rmse_scores = np.sqrt(-scores)
        decimal_p = 2
        with open(save_file, "w") as text_file:
            text_file.writelines('RMSE scores for ' + self.regressor_name + ': ')
            text_file.writelines('\nMean score =  ' + str(np.round(np.mean(tree_rmse_scores), decimal_p)))
            text_file.writelines('\nStandard deviation score =  ' + str(np.round(np.std(tree_rmse_scores), decimal_p)))
            text_file.writelines('\nScores =  ' + str(np.round(tree_rmse_scores, decimal_p)))
            # Close files
        text_file.close()
        return

    def grid_search(self):
        from sklearn.model_selection import GridSearchCV
        param_grid = [{'n_estimators': [3, 10, 30], 'max_features':[2, 4, 6, 8]}]
        grid_search = GridSearchCV(self.regressor, param_grid, cv=5, scoring='neg_mean_squared_error')
        grid_search.fit(self.x, self.y)
        best_params = grid_search.best_params_
        best_estimator = grid_search.best_estimator_
        cvres = grid_search.cv_results_
        feature_importances = grid_search.best_estimator_.feature_importances_
        f_names = self.f_names

        save_file = self.results_folder + self.regressor_name + '_grid_search.txt'
        with open(save_file, "w") as text_file:
            text_file.writelines('RMSE grid scores for ' + self.regressor_name + ': ')
            for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
                text_file.writelines('\n' + str(np.sqrt(-mean_score)) + ': ')
                text_file.writelines(str(params))

            text_file.writelines('\n' + 'Feature importance ' + self.regressor_name + ': ')
            c = -1
            for f in f_names:
                c = c + 1
                text_file.writelines('\n' + str(f) + ': ')
                text_file.writelines(str(feature_importances[c]))
        text_file.close()
        
        self.final_model = grid_search.best_estimator_
        return



    def split_train_test_reg(self, test_ratio):
        # Method from  Hands-On Machine Learning with Scikit-Learn & TensorFlow by Aurelion Geron 2017
        np.random.seed(37)
        shuffled_indices = np.random.permutation(len(self.x))
        test_set_size = int(len(self.x)*test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]
        self.train_x = self.x[train_indices,:]
        self.train_y = self.y[train_indices]
        self.test_x = self.x[test_indices, :]
        self.test_y = self.y[test_indices]
        return

    def get_classifier(self, classifier_name):
        rand_state = 37
        max_tree = 6
        self.classifier_name = classifier_name
        if self.classifier_name == "SGDClassifier":
            from sklearn.linear_model import SGDClassifier
            self.classifier = SGDClassifier(random_state=rand_state)
        elif self.classifier_name == "Decision_Tree":
            from sklearn.tree import DecisionTreeClassifier
            self.classifier = DecisionTreeClassifier(random_state=rand_state, max_depth=max_tree)
        else:
            print("Not a valid classifier name")
        return


    def split_train_test(self, test_ratio):
        # Method from  Hands-On Machine Learning with Scikit-Learn & TensorFlow by Aurelion Geron 2017
        np.random.seed(37)
        shuffled_indices = np.random.permutation(len(self.x))
        test_set_size = int(len(self.x)*test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]
        self.train_x = self.x[train_indices,:]
        self.train_y = np.ravel(self.y[train_indices].astype(int))
        self.test_x = self.x[test_indices, :]
        self.test_y = np.ravel(self.y[test_indices].astype(int))
        return

    def precision_metrics(self):
        self.fitmod = self.classifier.fit(self.x, self.y)
        y_pred = cross_val_predict(self.classifier, self.train_x, self.train_y, cv=10)
        con_mat = confusion_matrix(self.train_y, y_pred)
        negative_act = con_mat[0, :]
        positive_act = con_mat[1, :]
        tn = negative_act[0]
        fp = negative_act[1]
        fn = positive_act[0]
        tp = positive_act[1]
        precision = tp / (tp + fp)
        recall_tpr = tp / (tp + fn)
        specificity_tnr = tn / (tn + fp)
        fpr = 1 - specificity_tnr
        savefile = self.results_folder + self.classifier_name + '_precision_recall.txt'
        decimal_p = 3
        with open(savefile, "w") as text_file:
            text_file.writelines('Accuracy of ' + self.classifier_name + ': ')
            text_file.writelines('\nPrecision =  ' + str(np.round(precision, decimal_p)))
            text_file.writelines('\nRecall =  ' + str(np.round(recall_tpr, decimal_p)))
            text_file.writelines('\nSpecificity =  ' + str(np.round(specificity_tnr, decimal_p)))
            text_file.writelines('\nFalse positive rate =  ' + str(np.round(fpr, decimal_p)))
        # Close files
        text_file.close()
        return


    def decision_function(self, classifier):
        dec_v = np.zeros(np.shape(self.train_x)[0])
        for i in range(0, np.shape(self.train_x)[0]):
            dec_v[i] = classifier.decision_function([self.train_x[i, :]])
        return

    def precision_recall_curve(self):
        if self.classifier_name == "Decision_Tree":
            print("Decision_function not valid for this method")
        else:
            save_name = self.classifier_name + "_precision_recall_curve"
            y_scores = cross_val_predict(self.classifier, self.train_x, self.train_y, cv=10, method="decision_function")
            precisions, recalls, thresholds = precision_recall_curve(self.train_y, y_scores)
            plt.plot(thresholds, precisions[:-1], "b--", label="Precision")
            plt.plot(thresholds, recalls[:-1], "k-", label="Recall")
            plt.xlabel("Threshold")
            plt.legend(loc="center left")
            plt.ylim([0, 1])
            self.save_plot(save_name)
        return

    def hist_data(self):
        axis1_title = 'Frequency'
        axis1_xtitle = 'Log$_{10}$ krill under 1m$^{2}$'
        fig, ax1 = plt.subplots()
        ax1.set_ylabel(axis1_title, color='k', fontsize=13)
        ax1.set_xlabel(axis1_xtitle, color='k', fontsize=13)
        hist1 = ax1.hist(self.y, bins=15, facecolor='#2ab0ff', edgecolor='#169acf', linewidth=0.5)
        self.save_plot(save_name='hist_krillbase')
        return

    def save_plot(self, save_name):
        savefile = self.results_folder + save_name + '.png'
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return

    def map_predictions(self, data, cmems_path):
        time_id = 0
        depth = 0
        self.fit_regressor()

        geb_file = self.cmems_folder + 'gebco_2023.nc'
        nc_file = netCDF4.Dataset(geb_file)
        lat1 = np.array(nc_file['lat'])
        lon1 = np.array(nc_file['lon'])
        elevation_v = np.array(nc_file['elevation'])
        #cmems_bath = cmems_path + 'CMEMS_BGC_bathy.nc'
        #nc_file = netCDF4.Dataset(cmems_bath)


        lat = data.cm.lat
        lon = data.cm.lon
        e_v = np.zeros([np.shape(lat)[0], np.shape(lon)[0]])
        for i in range(0, np.shape(lat)[0]):
            for j in range(0, np.shape(lon)[0]):
                lat_i = lat[i]
                lon_j = lon[j]
                coord_geb_lat_i = np.argmin(np.sqrt((lat_i - lat1) ** 2))
                coord_geb_lon_i = np.argmin(np.sqrt((lon_j - lon1) ** 2))
                e_v[i, j] = elevation_v[coord_geb_lat_i, coord_geb_lon_i]

        e_v[e_v > 0] = np.nan
        e_v = e_v * -1

        chl = np.array(data.cm.chl[time_id, depth, :, :])
        no3 = np.array(data.cm.no3[time_id, depth, :, :])
        #nppv = np.array(data.cm.nppv[time_id, depth, :, :])
        o2 = np.array(data.cm.o2[time_id, depth, :, :])
        #po4 = np.array(data.cm.po4[time_id, depth, :, :])
        si = np.array(data.cm.si[time_id, depth, :, :])
        shp_lat = np.shape(lat)[0]
        shp_lon = np.shape(lon)[0]

        map_v = np.zeros([shp_lat, shp_lon])
        x = np.zeros([shp_lat*shp_lon, np.shape(self.x)[1]])
        counter_val = -1
        lat_store = np.zeros([shp_lat*shp_lon])
        lon_store = np.zeros([shp_lat*shp_lon])
        for i in range(0, shp_lat):
            for j in range(0, shp_lon):
                counter_val = counter_val + 1
                chl_v = chl[i, j]
                no3_v = no3[i, j]
                #nppv_v = nppv[i, j]
                o2_v = o2[i, j]
                #po4_v = po4[i, j]
                si_v = si[i, j]
                e_vv = e_v[i, j]

                x[counter_val, :] = [chl_v, no3_v, o2_v, si_v, e_vv]
                lat_store[counter_val] = lat[i]
                lon_store[counter_val] = lon[j]


        temp_v = np.zeros(np.shape(x)[0])
        for k in range(0, np.shape(x)[1]):
            id_1 = (x[:, k] > 1e06) | (np.isnan(x[:, k]))
            temp_v[id_1] = np.nanmedian(x[:, k])
            temp_v[~id_1] = x[~id_1, k]
            temp_v = (temp_v - np.mean(temp_v)) / np.std(temp_v)
            x[:, k] = temp_v



        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        from cartopy.io import shapereader
        predictions_v = self.regressor.predict(x)
        ax = plt.axes(projection=ccrs.PlateCarree())
        #coast = cfeature.GSHHSFeature(scale="f")
        #ax.add_feature(cfeature.GSHHSFeature('f'))
        #cline = shapereader.Reader(self.cmems_folder + 'ant_coastline.shp')
        #ax.add_geometries(cline.geometries(), ccrs.PlateCarree())
        #ax.add_feature(coast)
        ax.coastlines(resolution='10m')
        x2 = np.reshape(predictions_v, [shp_lat, shp_lon])
        lats = np.array(lat)
        lons = np.array(lon)
        color_m = ax.contourf(lons, lats, x2, levels=np.linspace(-2, 1, 100))
        plt.colorbar(color_m)
        ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        min_lon = -73
        max_lon = -31
        min_lat = -73
        max_lat = -50
        ax.set_extent([min_lon, max_lon, min_lat, max_lat])
        save_name = self.regressor_name + "_mapped_predictions"
        self.save_plot(save_name)

        breakpoint()



        return






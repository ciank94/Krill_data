import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, precision_recall_curve
from sklearn.model_selection import cross_val_predict


class ML:

    def __init__(self, data):
        self.fitmod = None
        self.test_y = None
        self.test_x = None
        self.train_y = None
        self.train_x = None
        self.classifier = None
        self.classifier_name = None
        self.results_folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/results/'
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

    def split_train_test(self, test_ratio):
        # Method from  Hands-On Machine Learning with Scikit-Learn & TensorFlow by Aurelion Geron 2017
        np.random.seed(37)
        shuffled_indices = np.random.permutation(len(self.x))
        test_set_size = int(len(self.x)*test_ratio)
        test_indices = shuffled_indices[:test_set_size]
        train_indices = shuffled_indices[test_set_size:]
        self.train_x = self.x[train_indices,:]
        self.train_y = np.ravel(self.y[train_indices].astype(int))
        self.test_x = self.x[test_indices,:]
        self.test_y = np.ravel(self.y[test_indices].astype(int))
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

    def map_predictions(self, data):
        time_id = 0
        depth = 0
        lat = data.cm.lat
        lon = data.cm.lon
        chl = np.array(data.cm.chl[time_id, depth, :, :])
        no3 = np.array(data.cm.no3[time_id, depth, :, :])
        nppv = np.array(data.cm.nppv[time_id, depth, :, :])
        o2 = np.array(data.cm.o2[time_id, depth, :, :])
        po4 = np.array(data.cm.po4[time_id, depth, :, :])
        si = np.array(data.cm.si[time_id, depth, :, :])
        shp_lat = np.shape(lat)[0]
        shp_lon = np.shape(lon)[0]
        map_v = np.zeros([shp_lat, shp_lon])
        for i in range(0, shp_lat):
            for j in range(0, shp_lon):
                chl_v = chl[i, j]
                no3_v = no3[i, j]
                nppv_v = nppv[i, j]
                o2_v = o2[i, j]
                po4_v = po4[i, j]
                si_v = si[i, j]
                if chl_v > 1e06:
                    map_v[i, j] = np.nan
                else:
                    features_v = np.array([chl_v, no3_v, nppv_v, o2_v, po4_v, si_v]).T
                    #prob_v = self.classifier.predict_proba([features_v])
                    prob_v = self.fitmod.predict([features_v])
                    #map_v[i, j] = prob_v[0, 1]
                    map_v[i, j] = prob_v[0]
        breakpoint()
        return






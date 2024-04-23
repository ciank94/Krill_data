import numpy as np


class ML:

    def __init__(self, data):
        self.test_y = None
        self.test_x = None
        self.train_y = None
        self.train_x = None
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




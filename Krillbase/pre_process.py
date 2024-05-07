import math

import numpy as np


class Fuse:

    def __init__(self, data_cm, data_kb):
        self.f_names = None
        self.cm = data_cm
        self.kb = data_kb
        self.lat_id = None
        self.lon_id = None
        self.x = None
        self.y = None
        self.nearest_id()
        self.get_dataset()
        # data = Data(data_cm, data_kb)
        # lat = -60
        # lon = -60

    def get_dataset(self):
        #todo: find the index of every krill sample in the model dataset: split
        # the function based on whether it's a single year or not
        if self.cm.time[0].year == self.cm.time[-1].year:
            print('fusing one year of data')
            months = self.kb.month.astype(int) - 1
            depth = 0
            lat_id = self.lat_id.astype(int)
            lon_id = self.lon_id.astype(int)
            chl = self.cm.chl[:]
            no3 = self.cm.no3[:]
            chl_vals = chl[months, depth, lat_id, lon_id]
            no3_vals = no3[months, depth, lat_id, lon_id]
            krill_p = self.transform_krill_density()
            self.x = np.array([chl_vals, no3_vals]).T
            self.y = np.array([krill_p]).T
        else:
            print('Fusing ' + str(self.cm.time[-1].year - self.cm.time[0].year) + ' years'  ' of data')
            months = self.kb.month.astype(int) - 1
            years = self.kb.year.astype(int) - self.cm.time[0].year
            time_id = (years*12) + months
            chl = self.cm.chl[:]
            no3 = self.cm.no3[:]
            nppv = self.cm.nppv[:]
            o2 = self.cm.o2[:]
            po4 = self.cm.po4[:]
            si = self.cm.si[:]
            krill_p = self.transform_krill_density()
            depth = 0
            lat_id = self.lat_id.astype(int)
            lon_id = self.lon_id.astype(int)
            v1 = chl[time_id, depth, lat_id, lon_id]
            v2 = no3[time_id, depth, lat_id, lon_id]
            v3 = nppv[time_id, depth, lat_id, lon_id]
            v4 = o2[time_id, depth, lat_id, lon_id]
            v5 = po4[time_id, depth, lat_id, lon_id]
            v6 = si[time_id, depth, lat_id, lon_id]
            v7 = self.kb.bath
            self.f_names = ["chl", "no3", "nppv", "o2", "po4", "si", "bath"]
            self.x = np.array([v1[:], v2[:], v3[:], v4[:], v5[:], v6[:], v7]).T
            self.y = np.ravel(np.array([krill_p]).T)
        return

    def transform_krill_density(self):
        n_obs = np.shape(self.kb.density)[0]
        krill_p = np.zeros(n_obs)
        krill_p[:] = self.kb.density[:]
        krill_p = krill_p + 0.01
        krill_v = np.log10(krill_p)
        # thresh_v = 0.5
        # krill_p[krill_p > thresh_v] = 1
        # krill_p[krill_p <= thresh_v] = 0
        return krill_v

    def nearest_id(self):
        n_obs = np.shape(self.kb.lat)[0]
        self.lat_id = np.zeros([n_obs])
        self.lon_id = np.zeros([n_obs])
        for i in range(0, n_obs):
            dist_lat = (self.kb.lat[i] - self.cm.lat[:]) ** 2
            dist_lon = (self.kb.lon[i] - self.cm.lon[:]) ** 2
            self.lat_id[i] = np.argmin(dist_lat)
            self.lon_id[i] = np.argmin(dist_lon)

        return



        # coord = np.argmin(dist_2)

import numpy as np
class Data:
    def __init__(self, data_cm, data_kb):
        self.cm = data_cm
        self.kb = data_kb
        self.lat_id = None
        self.lon_id = None
        self.X = None
        self.y = None
        self.nearest_id()
        self.get_dataset()
        # data = Data(data_cm, data_kb)
        # lat = -60
        # lon = -60

    def get_dataset(self):
        months = self.kb.month.astype(int) - 1
        depth = 0
        lat_id = self.lat_id.astype(int)
        lon_id = self.lon_id.astype(int)
        chl = self.cm.chl[:]
        no3 = self.cm.no3[:]
        chl_vals = chl[months, depth, lat_id, lon_id]
        no3_vals = no3[months, depth, lat_id, lon_id]
        krill_p = self.transform_krill_density()
        self.X = np.array([chl_vals, no3_vals]).T
        self.y = np.array([krill_p]).T
        return

    def transform_krill_density(self):
        n_obs = np.shape(self.kb.density)[0]
        krill_p = np.zeros(n_obs)
        krill_p[:] = self.kb.density[:]
        krill_p[krill_p > 0.1] = 1
        krill_p[krill_p <= 0.1] = 0
        return krill_p.astype(int)

    def nearest_id(self):
        n_obs = np.shape(self.kb.lat)[0]
        self.lat_id = np.zeros([n_obs])
        self.lon_id = np.zeros([n_obs])
        for i in range(0, n_obs):
            dist_lat = (self.kb.lat[i] - self.cm.lat[:]) ** 2
            dist_lon = (self.kb.lon[i] - self.cm.lon[:]) ** 2
            self.lat_id[i] = np.argmin(dist_lat)
            self.lon_id[i] = np.argmin(dist_lon)



        # coord = np.argmin(dist_2)

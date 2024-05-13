import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


class Plot:
    def __init__(self, region):
        if region == "SG":
            self.min_lon = -40
            self.max_lon = -33
            self.min_lat = -56
            self.max_lat = -53
            self.res = "f"
            self.s = 0.3


        if region == "full":
            self.min_lon = -73
            self.max_lon = -31
            self.min_lat = -73
            self.max_lat = -50

        self.name = region
        self.save_folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/GFWR/results/'

    def plot_points(self, lon, lat, c_v, vessel_names):
        ax = plt.axes(projection=ccrs.PlateCarree())
        coast = cfeature.GSHHSFeature(scale=self.res)
        ax.add_feature(coast)
        c_uniq = np.unique(c_v)
        clrs = ['b', 'r']
        c_t = -1
        for i in c_uniq:
            c_t = c_t + 1
            id_i = c_v == i
            plt.scatter(lon[id_i], lat[id_i], self.s, clrs[c_t])

        ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)
        ax.set_extent([self.min_lon, self.max_lon, self.min_lat, self.max_lat])
        plt_name = self.name + "_points"
        ax.legend(vessel_names)
        self.save_plot(plt_name)
        return

    def save_plot(self, plt_name):
        savefile = self.save_folder + plt_name + '.png'
        plt.title(plt_name)
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return

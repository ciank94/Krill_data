import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable


class Plot:
    def __init__(self, folder, region):
        self.c_max = None
        self.plot1 = None
        self.caxis_title = None
        self.fig = None
        self.ax = None
        self.bin_res = 0.1 # degrees for pcolor bins
        self.c_avg_catch_all = 30
        self.init_region(region)
        self.name = region
        self.save_folder = folder
        self.dens_cmap = plt.get_cmap('OrRd')

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

    def contour_map(self, df):
        self.init_plot()
        dens = df.weight_kg
        lat = df.lat
        lon = df.lon
        dens_f = self.bin_data(dens, lat, lon)
        #dens_f[dens_f>0] = np.log10(dens_f[dens_f>0])
        dens_f[dens_f > 0] = (dens_f[dens_f > 0])/1000
        self.plot_background()
        self.plot1 = plt.pcolor(self.lon_range, self.lat_range, dens_f.T, cmap=self.dens_cmap, transform=ccrs.PlateCarree())
        self.caxis_title = 'Catch (tonnes)'
        self.c_max = self.c_avg_catch_all
        self.add_cbar()
        plt_name = self.name + "_map"
        self.save_plot(plt_name)
        return

    def init_plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection=ccrs.PlateCarree())
        #self.ax = plt.axes(projection=ccrs.PlateCarree())
        return

    def bin_data(self, dens, lat, lon):
        shp_lat = np.shape(lat)[0]

        shp_lon_range = np.shape(self.lon_range)[0]
        shp_lat_range = np.shape(self.lat_range)[0]
        dens_m = np.zeros([shp_lon_range, shp_lat_range])
        n_catches = np.zeros([shp_lon_range, shp_lat_range])
        dens_f = np.zeros([shp_lon_range, shp_lat_range])

        for i in range(0, shp_lat):
            lat_id = np.argmin(np.sqrt((lat[i] - self.lat_range[:]) ** 2))
            lon_id = np.argmin(np.sqrt((lon[i] - self.lon_range[:]) ** 2))
            dens_m[lon_id, lat_id] = dens_m[lon_id, lat_id] + dens[i]
            n_catches[lon_id, lat_id] = n_catches[lon_id, lat_id] + 1

        dens_f[dens_m>0] = dens_m[dens_m>0]/n_catches[dens_m>0]
        return dens_f



    def plot_background(self):
        #plt.axes()
        #coast = cfeature.GSHHSFeature(scale=self.res) if needed;
        #add features: land and coastlines
        land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                                edgecolor='face',
                                                facecolor='lightgrey')
        self.ax.add_feature(land_10m)
        self.ax.coastlines(resolution='10m')

        # set extent and grid lines;
        gl = self.ax.gridlines(draw_labels=True, alpha=0.4)
        gl.top_labels = False
        gl.right_labels = False
        self.ax.set_extent([self.min_lon, self.max_lon, self.min_lat, self.max_lat])
        return

    def add_cbar(self):
        # plt.grid(alpha=0.45)
        #divider = make_axes_locatable(self.ax)
        #ax_cb = divider.new_horizontal(size="3%", pad=0.05, axes_class=plt.Axes)
        #self.fig.add_axes(ax_cb)
        cbar = plt.colorbar(self.plot1, extend = 'both')
        cbar.ax.set_ylabel(self.caxis_title, loc='center', size=9, weight='bold')
        cbar.ax.tick_params(labelsize=10, rotation=0)
        plt.clim(0, self.c_max)
        return

    def save_plot(self, plt_name):
        savefile = self.save_folder + plt_name + '.png'
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return
        # color_m = plt.contourf(lon_range, lat_range, dens_m.T, 15, cmap=self.dens_cmap, transform = ccrs.PlateCarree())#, levels=np.linspace(-2, 1, 100))



    def init_region(self, region):
        if region == "SG":
            self.min_lon = -40
            self.max_lon = -34
            self.min_lat = -57.5
            self.max_lat = -51.5
            self.res = "h"
            self.s = 0.3
            self.lat_range = np.arange(self.min_lat - 10, self.max_lat + 6, self.bin_res)
            self.lon_range = np.arange(self.min_lon - 10, self.max_lon + 6, self.bin_res)

        if region == "AP":
            self.min_lon = -65
            self.max_lon = -52
            self.min_lat = -69
            self.max_lat = -56
            self.res = "h"
            self.s = 0.3
            self.lat_range = np.arange(self.min_lat - 10, self.max_lat + 6, self.bin_res)
            self.lon_range = np.arange(self.min_lon - 10, self.max_lon + 6, self.bin_res)

        if region == "SO":
            self.min_lon = -50
            self.max_lon = -41
            self.min_lat = -65
            self.max_lat = -57
            self.res = "h"
            self.s = 0.3
            self.lat_range = np.arange(self.min_lat - 10, self.max_lat + 6, self.bin_res)
            self.lon_range = np.arange(self.min_lon - 10, self.max_lon + 6, self.bin_res)

        if region == "full":
            self.min_lon = -73
            self.max_lon = -31
            self.min_lat = -90
            self.max_lat = -50

        return








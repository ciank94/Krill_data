import os.path
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import netCDF4 as nc




class Read:

    def __init__(self, sindrift_path):
        # Organise file data
        self.filepath = sindrift_path + 'CMEMS/'
        self.results = sindrift_path + 'results/'
        self.tr_file = self.filepath + 'trajectory1.nc'
        self.nc_file = nc.Dataset(self.tr_file)
        self.bath_file = self.results + 'bath.npy'
        self.bath_file_lon = self.results + 'bath_lon.npy'
        self.bath_file_lat = self.results + 'bath_lat.npy'
        self.bath = np.load(self.bath_file)
        self.bath_lon = np.load(self.bath_file_lon)
        self.bath_lat = np.load(self.bath_file_lat)

        # extract data from trajectory file
        self.lat = self.nc_file['lat']
        self.lon = self.nc_file['lon']
        #self.z = self.nc_file['z']

        # plotting parameters
        self.bath_contours = np.linspace(0, 3000, 10)
        self.bath_cmap = plt.get_cmap('Blues')
        self.depth_colors = np.arange(0, 4500, 200)
        return

    def plot_trajectory(self, region):
        self.init_region(region)
        self.init_plot()
        self.plot_background()

        self.plot_depth()
        self.c_max = 4500
        self.caxis_title = 'Depth (m)'
        self.add_cbar()

        step_v = np.floor(np.shape(self.lon)[0]/1000).astype(int)

        lon_1 = self.lon[0:-1:step_v, :]
        lat_1 = self.lat[0:-1:step_v, :]
        #
        plt.scatter(lon_1, lat_1, s=1, facecolor='gray', edgecolors='gray', alpha=0.5, linewidth=0.5)
        plt.scatter(lon_1[:, 0], lat_1[:, 0], s=20, facecolor='red', edgecolors='k', alpha=0.8, linewidth=0.5)

        plt_name = region + "_worms"
        self.save_plot(plt_name)
        return



    def plot_background(self):
        land_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                                edgecolor='face',
                                                facecolor='lightgrey')
        self.ax.add_feature(land_10m)
        self.ax.coastlines(resolution='10m', linewidth=0.7)
        plt.contour(self.bath_lon, self.bath_lat, self.bath, self.bath_contours, colors='k', alpha=0.2, linewidths=0.7,
                    transform=ccrs.PlateCarree())

        # set extent and grid lines;
        gl = self.ax.gridlines(draw_labels=True, alpha=0.4)
        gl.top_labels = False
        gl.right_labels = False
        self.ax.set_extent([self.min_lon, self.max_lon, self.min_lat, self.max_lat])
        return

    def plot_depth(self):
        #levels= self.depth_colors
        self.plot1 = plt.contourf(self.bath_lon, self.bath_lat, self.bath, levels = self.depth_colors, cmap = self.bath_cmap,
                  transform=ccrs.PlateCarree(), extend='both')
        return


    def init_plot(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection=ccrs.PlateCarree())
        return

    def add_cbar(self):
        cbar = plt.colorbar(self.plot1, extend = 'both')
        cbar.ax.set_ylabel(self.caxis_title, loc='center', size=9, weight='bold')
        cbar.ax.tick_params(labelsize=10, rotation=0)
        plt.clim(0, self.c_max)
        return

    def save_plot(self, plt_name):
        savefile = self.results + plt_name + '.png'
        print('Saving file: ' + savefile)
        plt.savefig(savefile, dpi=400)
        plt.close()
        return

    def init_region(self, region):


        if region == "SG":
            self.min_lon = -40.5
            self.max_lon = -33.8
            self.min_lat = -57.5
            self.max_lat = -51.5


        if region == "AP":
            self.min_lon = -65.3
            self.max_lon = -51
            self.min_lat = -69
            self.max_lat = -56

        if region == "SO":
            self.min_lon = -50
            self.max_lon = -41
            self.min_lat = -65
            self.max_lat = -57

        if region == "full":
            self.min_lon = -65
            self.max_lon = -31
            self.min_lat = -70
            self.max_lat = -50

        return

class sinRead:

    def __init__(self, var):
        self.sinmod_path = 'E:/fromIngrid/'
        f_name_start = 'samplesNSEW_2020'
        f_ext = '.nc'
        self.f_name = self.sinmod_path + f_name_start + var + f_ext
        self.nc_file = nc.Dataset(self.f_name)
        #file_save = 'C:/Users/ciank/PycharmProjects/Krill_data/SINdrift/animation.mp4'
        return



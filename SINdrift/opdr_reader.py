
import netCDF4 as nc

class sinRead:

    def __init__(self, var):
        self.sinmod_path = 'E:/fromIngrid/'
        f_name_start = 'samplesNSEW_2020'
        f_ext = '.nc'
        self.f_name = self.sinmod_path + f_name_start + var + f_ext
        self.nc_file = nc.Dataset(self.f_name)
        #file_save = 'C:/Users/ciank/PycharmProjects/Krill_data/SINdrift/animation.mp4'
        return


class opd_Read:

    def __init__(self, sindrift_path):
        self.filepath = sindrift_path + 'CMEMS/'
        self.results = sindrift_path + 'results/'
        self.tr_file = self.filepath + 'trajectory.nc'
        self.nc_file = nc.Dataset(self.tr_file)

        return

from subprocess import call
import os
import netCDF4 as nc

class Files:

    def __init__(self, var):
        self.path = 'E:/fromIngrid/'
        f_name_start = 'samplesNSEW_2020'
        f_ext = '.nc'
        self.f_name = self.path + f_name_start + var + f_ext
        self.nc_file = nc.Dataset(self.f_name)
        return
import os
import sys
import copernicusmarine as cop
import netCDF4 as nc
from netCDF4 import num2date
from pprint import pprint


class FilesCM:

    def __init__(self, cmems_path, data_id, y1, y2):
        self.min_depth = 0
        self.max_depth = 1
        self.min_lon = -73
        self.max_lon = -31
        self.min_lat = -73
        self.max_lat = -50
        self.data_id = data_id
        self.cmems_path = cmems_path
        self.start_date = y1 + "-01-01T00:00:00"
        self.end_date = y2 + "-12-31T23:59:59"

        if data_id == "cmems_mod_glo_bgc_my_0.25_P1M-m":
            self.var = ["chl", "no3", "nppv", "o2", "po4", "si"]
            self.cmems_data = (self.cmems_path + 'CMEMS_BGC_hindcast_' + self.start_date[:4] +
                               '_' + self.end_date[:4] + '.nc')
        else:
            print('Invalid cmems data id')
            sys.exit()

        if not os.path.exists(self.cmems_data):
            print('Downloading file and naming: ' + self.cmems_data)
            self.download_set()
        else:
            print('Already downloaded dataset with name:  ' + self.cmems_data)

        return

    def download_set(self):

        cop.subset(dataset_id=self.data_id,
                   variables= self.var,
                   start_datetime=self.start_date,
                   end_datetime=self.end_date,
                   minimum_longitude=self.min_lon,
                   maximum_longitude=self.max_lon,
                   minimum_latitude=self.min_lat,
                   maximum_latitude=self.max_lat,
                   minimum_depth=self.min_depth,
                   maximum_depth=self.max_depth,
                   output_filename=self.cmems_data,
                   output_directory=self.cmems_path
                   )
        #cop.login()
        # catalogue = cop.describe(contains=["BGC_001_029"], include_datasets=True)
        # dataset = catalogue['products'][0]['datasets'][0]
        return


class DataCM:

    def __init__(self, files):
        self.nc_file = nc.Dataset(files.cmems_data)
        self.time = num2date(self.nc_file["time"], self.nc_file["time"].units)
        self.depth = self.nc_file["depth"]
        self.lat = self.nc_file["latitude"]
        self.lon = self.nc_file["longitude"]
        try:
            self.chl = self.nc_file["chl"]
        except:
            pass
        try:
            self.no3 = self.nc_file["no3"]
        except:
            pass
        try:
            self.nppv = self.nc_file["nppv"]
        except:
            pass
        try:
            self.o2 = self.nc_file["o2"]
        except:
            pass
        try:
            self.po4 = self.nc_file["po4"]
        except:
            pass
        try:
            self.si = self.nc_file["si"]
        except:
            pass
        return


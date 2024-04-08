import os.path

import copernicusmarine as cop
import netCDF4 as nc
from netCDF4 import num2date
from pprint import pprint


class FilesCM:

    def __init__(self, cmems_path, var, data_id, yr, region, start_date, end_date):
        self.var = var
        self.data_id = data_id
        self.min_depth = 0
        self.max_depth = 5
        self.start_date = start_date
        self.end_date = end_date
        self.cmems_path = cmems_path
        self.cmems_data = self.cmems_path + 'CMEMS_BGC_hindcast_' + yr + '.nc'

        if region == "AP":
            self.min_lon = -73
            self.max_lon = -60
            self.min_lat = -73
            self.max_lat = -44

        if not os.path.exists(self.cmems_data):
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
        nc_file = nc.Dataset(files.cmems_data)
        self.time = num2date(nc_file["time"], nc_file["time"].units)
        self.depth = nc_file["depth"]
        self.lat = nc_file["latitude"]
        self.lon = nc_file["longitude"]
        self.chl = nc_file["chl"]
        return

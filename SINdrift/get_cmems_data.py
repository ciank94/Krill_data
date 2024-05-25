import os
import sys
import copernicusmarine as cop
import netCDF4 as nc
from netCDF4 import num2date
from pprint import pprint


class FilesCM:

    def __init__(self, cmems_path, data_id, y1, y2, download):
        self.case = "norm_"
        self.month_end = None
        self.month_start = None
        self.config_duration()  # Uses case to specify start and end dataes extracted from cmems
        self.min_depth = 40
        self.max_depth = 80
        self.min_lon = -70
        self.max_lon = -31
        self.min_lat = -73
        self.max_lat = -50
        self.data_id = data_id
        self.cmems_path = cmems_path
        self.start_date = y1 + self.month_start
        self.end_date = y2 + self.month_end

        if data_id == "cmems_mod_glo_phy_my_0.083deg_P1D-m":
            self.var = ["uo", "vo"]
            self.cmems_data = (self.cmems_path + 'CMEMS_GLPHYS_D_' + self.case + self.start_date[:4] +
                               '_' + self.end_date[:4] + '.nc')
        elif data_id == "cmems_mod_glo_phy-cur_anfc_0.083deg_P1M-m":
            self.var = ["uo", "vo"]
            self.cmems_data = (self.cmems_path + 'CMEMS_GLO_PHYS_hindcast_monthly_' + self.start_date[:4] +
                               '_' + self.end_date[:4] + '.nc')
        else:
            print('Invalid cmems data id')
            sys.exit()

        if not os.path.exists(self.cmems_data):
        #if download == 1:
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

    def config_duration(self):
        if self.case == "SG_S_":
            print("DOWNLOADING: Case SG_short")
            month_start = "-05-01"
            month_end = "-09-30"
        else:
            print("DOWNLOADING standard file")
            month_start = "-01-01"
            month_end = "-12-31"

        self.month_start = month_start + "T00:00:00"
        self.month_end = month_end + "T23:59:59"
        return



class DataCM:

    def __init__(self, files):
        self.nc_file = nc.Dataset(files.cmems_data)
        self.time = num2date(self.nc_file["time"], self.nc_file["time"].units)
        self.depth = self.nc_file["depth"]
        self.lat = self.nc_file["latitude"]
        self.lon = self.nc_file["longitude"]
        try:
            self.uo = self.nc_file["uo"]
        except:
            pass
        try:
            self.vo = self.nc_file["vo"]
        except:
            pass
        return


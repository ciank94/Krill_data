import numpy as np

from opdr_reader import sinRead
from get_cmems_data import FilesCM, DataCM
from datetime import datetime, timedelta


def read_nc_input(sim_v, path, y1, y2, data_id, download):
    if sim_v == "cmems":
        data_id = data_id
        f = FilesCM(path, data_id, y1, y2, download)  #phys_data = DataCM(f_cmems)
        phys_states = f.cmems_data
    else:
        var = '01'
        f = sinRead(var)
        phys_states = []
        # needs work

    return phys_states


class Case:
    def __init__(self, reader, path, time_step_hours, days):
        self.trajectory_file = None
        self.description = None
        self.lon_init = None
        self.lat_init = None
        self.name = None
        self.scenario = None
        self.n_part = 10000
        self.radius = 10000
        self.z = 50
        self.duration = timedelta(hours=24*days)
        self.time_step = timedelta(hours=time_step_hours)
        self.export_variables = ['lon', 'lat']
        self.path = path
        if time_step_hours < 0:
            self.t_init = reader.end_time
        else:
            self.t_init = reader.start_time
        return

    def get_scenarios(self, key):
        self.name = key
        self.get_config_params()
        self.trajectory_file = self.path + key + '_case_trajectory.nc'
        self.scenario = {'name': self.name,
                         "description": self.description,
                         "lon_init": str(self.lon_init),
                         "lat_init": str(self.lat_init),
                         "t_init": self.t_init,
                         "duration": self.duration,
                         "particles": self.n_part,
                         "radius": self.radius,
                         "trajectory_filename": self.trajectory_file
                         }
        return

    def get_config_params(self):
        if self.name == "APSO":
            lon_min = -70
            lon_max = -40
            step_lon = (-1*(lon_min - lon_max)/np.sqrt(self.n_part))
            lat_min = -68
            lat_max = -57
            step_lat = (-1*(lat_min - lat_max) / np.sqrt(self.n_part))
            lons = np.arange(lon_min, lon_max, step_lon)
            lats = np.arange(lat_min, lat_max, step_lat)
            self.lat_init, self.lon_init = np.meshgrid(lats, lons)
            self.radius = 0
        elif self.name == "SG_NE":
            self.description = "Important fishing ground at NE"
            self.lat_init = -53.8
            self.lon_init = -36

        elif self.name == "SG_NW":
            self.description = "Important fishing ground at NW"
            self.lat_init = -53.75
            self.lon_init = -38.5
        else:
            print('missing key configuration in get_config_params')
        return





import netCDF4 as nc
from configure import read_nc_input, Case
import sys
sys.path.insert(0, 'C:/Users/ciank/PycharmProjects/sinmod/opendrift') # add opendrift local path
path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/SINdrift/CMEMS/'
#path = 'E:/cmems_opendrift/'
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic, reader_global_landmask

# CMEMS folders
y1 = "2000"
y2 = "2000"
data_id = "cmems_mod_glo_phy_my_0.083deg_P1D-m"
sim_v = "cmems"
download = 1

# Simulation settings
time_step_hours = 6  # negative time is backwards stepping of model
duration_days = 120  # look into (time=start_time + i*time_step) for setting the start and end time of simulations;

#key_list = ["SG_NW", "SG_NE"]
key_list = ["SG_NW"]
for key in key_list:
    # Create simulation instance:
    o = OceanDrift(loglevel=20)  # log_level= 0 for full diagnostics, 50 for none

    # Adding reader objects to provide forcing variables
    phys_states = read_nc_input(sim_v, path, y1, y2, data_id, download)
    reader_samples = reader_netCDF_CF_generic.Reader(phys_states)  # read forcing variables
    reader_landmask = reader_global_landmask.Reader()  # high resolution coast for particle beaching etc.
    o.add_reader([reader_landmask, reader_samples])  # add readers to model instance

    # Class for configuring simulation scenario and storing output file;
    case = Case(reader_samples, path, time_step_hours, duration_days)
    case.get_scenarios(key=key)

    # Simulation seeding
    o.disable_vertical_motion()
    o.seed_elements(lon=case.lon_init,
                    lat=case.lat_init,
                    time=case.t_init,
                    number=case.n_part,
                    radius=case.radius)

    # Simulation running
    o.run(duration=case.duration,
          time_step=case.time_step,
          outfile=case.trajectory_file,
          export_variables=case.export_variables)




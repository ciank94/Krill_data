from files import Files
from get_cmems_data import FilesCM, DataCM
from datetime import datetime, timedelta
import sys
sys.path.insert(0, 'C:/Users/ciank/PycharmProjects/sinmod/opendrift') # add opendrift local path
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic as read_nc
from opendrift.readers import reader_global_landmask

y1 = "2000"
y2 = "2001"
cmems_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/SINdrift/CMEMS/'
data_id = "cmems_mod_glo_phy_my_0.083deg_P1D-m"
f_cmems = FilesCM(cmems_path, data_id, y1, y2)
phys_data = DataCM(f_cmems)
# var = '01'
# f = Files(var)


o = OceanDrift()
reader_samples = read_nc.Reader(f_cmems.cmems_data)
o.add_readers_from_list(f_cmems.cmems_data)
# reader_samples = read_nc.Reader(f.f_name)
# o.add_readers_from_list(f.f_name)
o.disable_vertical_motion()
o.seed_elements(lon=-73, lat=-73, time=reader_samples.start_time, number=1000, radius=1000000)

o.run(duration=timedelta(hours=24*60))


#o.animation(filename='animation.mp4')
breakpoint()


# min_lon = -73
# max_lon = -31
# min_lat = -73
# max_lat = -50
# reader_landmask = reader_global_landmask.Reader()  # lonmin, latmin, lonmax, latmax




#Import model for passive tracers

#


#o.add_reader([reader_landmask, reader_samples])



o.seed_elements(lon=min_lon, lat=min_lat, number=100, radius=1000,
                time=reader_samples.start_time)
o.run()
breakpoint()



o.add_readers_from_list(
    [f.f_name])

o.disable_vertical_motion()
o.seed_elements(lon=4.85, lat=60, time=datetime.now(), number=10000, radius=1000)
o.run(duration=timedelta(hours=1))
o.animation()
breakpoint()

print(f.path)
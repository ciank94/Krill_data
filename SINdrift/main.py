from files import Files
from datetime import datetime, timedelta
import sys
sys.path.insert(0, 'C:/Users/ciank/PycharmProjects/sinmod/opendrift') # add opendrift local path
from opendrift.models.oceandrift import OceanDrift
from opendrift.readers import reader_netCDF_CF_generic as read_nc
from opendrift.readers import reader_global_landmask


var = '01'
f = Files(var)
o = OceanDrift()
reader_samples = read_nc.Reader(f.f_name)
o.add_readers_from_list(f.f_name)
o.disable_vertical_motion()
o.seed_elements(lon=-73, lat=-73, time=reader_samples.start_time, number=1000, radius=1000)

o.run()


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
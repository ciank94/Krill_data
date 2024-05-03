from files import Files
from datetime import datetime, timedelta
from opendrift.opendrift.models.oceandrift import OceanDrift
import netCDF4 as nc
import subprocess
var = '01'
f = Files(var)
o = OceanDrift()
o.add_readers_from_list(
    ['https://thredds.met.no/thredds/dodsC/sea/norkyst800m/1h/aggregate_be'])

o.disable_vertical_motion()
o.seed_elements(lon=4.85, lat=60, time=datetime.now(), number=10000, radius=1000)
o.run(duration=timedelta(hours=1))
o.animation()
breakpoint()

print(f.path)
import os.path

from get_krillbase_data import Data, Files, DataTime
from get_cmems_data import FilesCM, DataCM
kbase_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/'
cmems_path = kbase_path + 'CMEMS/'

var = ["chl"]
data_id = "cmems_mod_glo_bgc_my_0.25_P1M-m"  # monthly
region = "AP"
yr = "2015"
start_date = yr + "-01-01T00:00:00"
end_date = yr + "-12-31T23:59:59"
files_cm = FilesCM(cmems_path, var, data_id, yr, region, start_date, end_date)

data_cm = DataCM(files_cm)

breakpoint()

# files = Files(kbase_path)
# data = Data(files)
#
#
# dataset = DataTime(data, month_start=1, month_end=3, year_start=2010, year_end=2016)
# breakpoint()
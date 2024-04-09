from get_krillbase_data import DateTimeKB, FilesKB, DataKB
from get_cmems_data import FilesCM, DataCM
from pre_process import Data
kbase_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/'
cmems_path = kbase_path + 'CMEMS/'

var = ["chl", "no3"]
data_id = "cmems_mod_glo_bgc_my_0.25_P1M-m"  # monthly
region = "AP"
yr = "1993"
start_date = yr + "-01-01T00:00:00"
end_date = yr + "-12-31T23:59:59"
files_cm = FilesCM(cmems_path, var, data_id, yr, region, start_date, end_date)

# Krillbase files
files_kb = FilesKB(kbase_path)

data_cm = DataCM(files_cm)
data_a = DataKB(files_kb)
data_kb = DateTimeKB(data_a, month_start=1, month_end=12, year_start=1993, year_end=1993)
import matplotlib.pyplot as plt


data = Data(data_cm, data_kb)


# chl = data_cm.chl[1, 0, :, :]
#
#
#
breakpoint()
# breakpoint()

# lonW=-70
# lonE=-20
# latS=-70
# latN=-50
# coordinates = (lonW, lonE, latS, latN)
# m = Basemap(llcrnrlon=coordinates[0], llcrnrlat=coordinates[2],
#                 urcrnrlon=coordinates[1], urcrnrlat=coordinates[3],
#                 resolution='i')
# m.drawcoastlines(linewidth=.5)
# m.drawmeridians(np.arange(-180., 180., 10.), labels=[False, False, False, True])
# m.drawparallels(np.arange(-90., 90., 4.), labels=[True, False, False, False])
# m.scatter(dataset.lon, dataset.lat, 5, color='r')
#     #m.etopo()
# m.shadedrelief()
# x, y = m(lon1, lat1)
# plt.pcolormesh(x, y, df3[df3>0])
# plt.colorbar(orientation='horizontal')
#
# m.scatter(x, y, 3, marker='o', color='r')
from get_krillbase_data import Data, Files, DataTime

kbase_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/'

files = Files(kbase_path)
data = Data(files)


data_2010 = DataTime(data, month_start=1, month_end=10, year=2010)
breakpoint()
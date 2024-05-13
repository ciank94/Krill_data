import numpy as np
from explore import explore_data
import pandas as pd
import matplotlib.pyplot as plt
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/'
file = folder + 'catch.csv'
table = pd.read_csv(file, sep=',')
tableb = table[table.asd_code == '483']
breakpoint()
explore_data(table)




import numpy as np
from explore import explore_data
import pandas as pd
import matplotlib.pyplot as plt
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/'
file = folder + 'catch.csv'
table = pd.read_csv(file, sep=',')
explore_data(table)




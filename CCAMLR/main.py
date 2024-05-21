import numpy as np
from reader import Read
from plot_data import Plot
import pandas as pd
import matplotlib.pyplot as plt
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/results/'
file = folder + 'C1_680.csv'
df = Read(folder, file)

#Subset data
df.subset("None")

#summary plots
#catch.summary_plots()

# plot = Plot(folder, "full")
# plot.contour_map(df)
#
# plot = Plot(folder, "AP")
# plot.contour_map(df)
#
# plot = Plot(folder, "SO")
# plot.contour_map(df)

plot = Plot(folder, "AP")
plot.contour_map(df)
breakpoint()


#first thing to do is put important variables in a class structure;





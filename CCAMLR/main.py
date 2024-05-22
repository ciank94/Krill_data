import numpy as np
from reader import Read
from plot_data import Plot
import pandas as pd
import matplotlib.pyplot as plt
from compare_scenarios import compare_regions

folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/results/'
file = folder + 'C1_680.csv'

regions = ["ALL", "SO", "SG", "AP"]
for region_n in regions:
    df = Read(folder, file)
    df.subset(region_n)
    plot = Plot(folder, region_n)
    plot.contour_map(df)

breakpoint()
# compare regions;
compare_regions(folder, file)


breakpoint()
# df = Read(folder, file)
# df.subset("SG")


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

# plot = Plot(folder, "AP")
# plot.contour_map(df)
breakpoint()


#first thing to do is put important variables in a class structure;





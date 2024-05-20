import numpy as np
from reader import Read
import pandas as pd
import matplotlib.pyplot as plt
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/results/'
file = folder + 'C1_680.csv'
catch = Read(folder, file)

#Subset data
catch.subset("None")

#summary plots
catch.summary_plots()
breakpoint()


#first thing to do is put important variables in a class structure;





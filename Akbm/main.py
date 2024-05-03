from pre_process import combine_files
import os
import numpy as np
import pandas as pd
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/Akbm/'
summary_f = folder + 'summaryTablesExamples/'

combine_files(folder, summary_f)

#todo: make summaries for the combined file- how many times are there- the gaps, in time, averages, std etc;
#Todo: then next we go into histograms of different variables- raw and log10 vals;;


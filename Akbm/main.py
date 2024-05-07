from pre_process import combine_files, read_table
import os
import numpy as np
import pandas as pd
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/Akbm/'
summary_f = folder + 'summaryTablesExamples/'

#combine_files(folder, summary_f)

read_table(folder)

#Comments- 10  min resolution- data from trajectory- krill distribution mostly near surface down to 200m, mainly zeros,
# with a power law distribution;



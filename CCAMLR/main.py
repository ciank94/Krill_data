import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/'
file = folder + 'catch.csv'
table = pd.read_csv(file, sep=',')

#t_species = table.taxon_code
#look into what they target vs. what they catch in SG region- what happens when they target specific species in this
#location- compare different subregions- are they more precise in some areas?
t_species = table.target_species_code
table2 = table[t_species=='KRI']
tonnes = np.array(table2.greenweight_caught_tonne)
tonnes[tonnes==0] = 0.000001
t10 = np.log10(tonnes)
m = table2.month
y = table2.year
plt.hist(t10)
plt.show()
breakpoint()

import matplotlib.pyplot as plt
import numpy as np

def explore_data(table):
    t_species = table.taxon_code
    # look into what they target vs. what they catch in SG region- what happens when they target specific species in this
    # location- compare different subregions- are they more precise in some areas?
    # t_species = table.target_species_code
    table2 = table[t_species == 'KRI']
    tonnes = np.array(table2.greenweight_caught_tonne)
    tonnes[tonnes == 0] = 0.000001
    t10 = np.log10(tonnes)
    m = table2.month
    y = table2.year
    code_v = table2.vessel_nationality_code
    plt.hist(t10)

    fig, ax = plt.subplots()
    plt.hist(t10)
    save_plot('Krill_tonnes')

    fig, ax = plt.subplots()
    plt.hist(m)
    save_plot('months')

    fig, ax = plt.subplots()
    plt.hist(y)
    save_plot('years')

    fig, ax = plt.subplots()
    plt.hist(code_v)
    save_plot('nationality')

def save_plot(save_name):
    savefile = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/CCAMLR/' + save_name + '.png'
    plt.title(save_name)
    print('Saving file: ' + savefile)
    plt.savefig(savefile, dpi=400)
    plt.close()
    return

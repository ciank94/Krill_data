import os
import numpy as np
import pandas as pd

def combine_files(folder, summary_f):
    file_list = os.listdir(summary_f)
    shp_f = np.shape(file_list)[0]

    df_list = []
    for i in range(1,shp_f):
        fl_val = file_list[i]
        f_name = summary_f + fl_val
        table = pd.read_csv(f_name, sep=',')
        df_list.append(table)


    # Concatenate all data into one DataFrame
    combo_df = pd.concat(df_list, ignore_index=True)

    # Save the final result to a new CSV file
    save_name = 'summary_file.csv'
    combo_df.to_csv(os.path.join(folder, save_name), index=False)

    print('Saving: ' + folder + save_name)
    return
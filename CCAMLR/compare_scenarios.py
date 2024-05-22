import numpy as np
from reader import Read
from plot_data import Plot
import pandas as pd
import matplotlib.pyplot as plt


def compare_regions(folder, file):
    # Read dataframes from file
    df1 = Read(folder, file)
    df2 = Read(folder, file)
    df3 = Read(folder, file)
    df4 = Read(folder, file)

    df1.subset("SG")
    df2.subset("SO")
    df3.subset("AP")
    df4.subset("ALL")

    df1.summary_catch()
    df2.summary_catch()
    df3.summary_catch()
    df4.summary_catch()

    breakpoint()





    df1.summary_plots()


    df2.summary_plots()


    df3.summary_plots()


    df4.summary_plots()

    # fig, ax = plt.subplots(3, 1)
    # ax[0].hist(df1.year)
    # ax[0].title.set_text(df1.sub_rule)
    # ax[1].hist(df2.year)
    # ax[1].title.set_text(df2.sub_rule)
    # ax[2].hist(df3.year)
    # ax[2].title.set_text(df3.sub_rule)

    # fig, ax = plt.subplots()
    # plt.hist(df1.month)
    # fig, ax = plt.subplots()
    # plt.hist(df2.month)
    # fig, ax = plt.subplots()
    # plt.hist(df3.month)
    # plt.title(df3.sub_rule)
    #
    #
    #
    # breakpoint()


from opdr_reader import Read
sindrift_path = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/SINdrift/'
key_list = ["SG_NW", "SG_NE"]
for key in key_list:
    op = Read(sindrift_path, key)
    op.plot_trajectory("full")
breakpoint()


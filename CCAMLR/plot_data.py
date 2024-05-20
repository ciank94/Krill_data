class Plot:
    def __init__(self, region):
        if region == "SG":
            self.min_lon = -40
            self.max_lon = -33
            self.min_lat = -56
            self.max_lat = -53
            self.res = "f"
            self.s = 0.3


        if region == "full":
            self.min_lon = -73
            self.max_lon = -31
            self.min_lat = -73
            self.max_lat = -50

        self.name = region
        self.save_folder = 'C:/Users/ciank/PycharmProjects/sinmod/Krill_data/GFWR/results/'
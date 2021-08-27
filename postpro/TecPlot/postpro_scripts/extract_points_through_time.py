import numpy as np
import tecplot as tp
import pandas as pd
import time
from tecplot.constant import *


class Point_Extraction:
    def __init__(self, points_file_location, zones_to_search, vars_to_retrieve):
        tp.session.connect()
        self.start = time.time()
        frame = tp.active_frame()
        dataset = frame.dataset

        # load in the XYZ positions here
        # see https://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html
        self.points_file = np.loadtxt(points_file_location)

        # Limit the probe to the zone specified
        self.zones_to_search = list(dataset.zones(zones_to_search))

        # Loop through each zone and collect the probe results
        self.vars_to_retrieve = [dataset.variable(vars_to_retrieve)]  # list

    def df_points(self):
        probed_values = []
        for z in self.zones_to_search:
            res = tp.data.query.probe_on_surface(self.points_file.transpose(),
                                                 zones=[z],
                                                 variables=self.vars_to_retrieve)
                                                 # probe_nearest=ProbeNearest.Node,
                                                 # num_nearest_nodes=10,
                                                 # tolerance=1e-5)
            probed_values.append([z.solution_time] + list(res.data))
        print("Elapsed: ", time.time() - self.start)
        return pd.DataFrame(np.array(probed_values).transpose())

    def df_points_center(self):
        probed_values = []
        for z in self.zones_to_search:
            res = tp.data.query.probe_on_surface(self.points_file.transpose(),
                                                 zones=[z],
                                                 variables=self.vars_to_retrieve,
                                                 probe_nearest=ProbeNearest.Position)
            probed_values.append([z.solution_time] + list(res.data))
        print("Elapsed: ", time.time() - self.start)
        return pd.DataFrame(np.array(probed_values).transpose())


if __name__ == '__main__':
    points_file = r"C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_D1_Coordinates.txt"
    zones_to_search = "blade-passage Step 1 Incr 0"
    vars_to_retrieve = "Magnitude Velocity"
    test_class = Point_Extraction(points_file_location=points_file,
                                  zones_to_search=zones_to_search,
                                  vars_to_retrieve=vars_to_retrieve)
    df_node = test_class.df_points()
    df_center=test_class.df_points_center()
    # df = df.drop([0])
    # df = df.reset_index()
    # df['Mean'] = df.mean(axis=1)



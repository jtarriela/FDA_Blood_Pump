from postpro.TecPlot.postpro_scripts.extract_points_through_time import Point_Extraction as PET
import pandas as pd
import numpy as np

C5_coordinates = {
    'D1': r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_D1_Coordinates.txt',
    'D2': r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_D2_Coordinates.txt',
    'D3': r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_D3_Coordinates.txt',
    'D4': r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_D4_Coordinates.txt',
    'Q1': r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_Q1_Coordinates.txt',
    'Q2': r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\C5_sampling_coordinates\C5_Q2_Coordinates.txt'}
C5_header = ["x-coord", "y-coord", "z-coord"]
C5_pd = {}

zones_to_search = "blade-passage Step 1 Incr 0"
vars_to_retrieve = "Magnitude Velocity"

for i in enumerate(C5_coordinates):
    C5_pd[i[1]] = pd.read_csv(C5_coordinates[i[1]], delim_whitespace=True, header=None)
    C5_pd[i[1]].columns = C5_header
    C5_pd[i[1]]['radial_position'] = np.sqrt(C5_pd[i[1]]['x-coord'] ** 2 + C5_pd[i[1]]['y-coord'] ** 2)
    print(str(i[1]) + " DF Conversion Complete\n")

    points_file = C5_coordinates[i[1]]
    # print(points_file)
    test_class = PET(points_file_location=points_file,
                     zones_to_search=zones_to_search,
                     vars_to_retrieve=vars_to_retrieve)
    df = test_class.df_points()
    print(str(i[1]) + " TecPlot Extraction Complete\n")

    df = df.drop([0])
    df = df.reset_index()
    df['Mean'] = df.mean(axis=1)
    C5_pd[i[1]]["Velocity Magnitude Average"] = df['Mean']

# points_file = "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_D1_Coordinates.txt"
# zones_to_search = "blade-passage Step 1 Incr 0"
# vars_to_retrieve = "Magnitude Velocity"
# test_class = PE(points_file_location=points_file,
#                 zones_to_search=zones_to_search,
#                 vars_to_retrieve=vars_to_retrieve)
# df = test_class.df_points()
#




# TODO: Why is it failing on some slices? out of zone?

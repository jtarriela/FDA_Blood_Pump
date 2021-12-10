import pandas as pd
import numpy as np
import os, glob

#TODO create class to extract line and quadrant data
#TODO local grab list of all files via glob for Q or D

# How to use:
# args:
    # Analysis Type(str) - accepts "Q" or "D" -extracting quadrant or diffuser data
    # Slice Number(int) - Q(1-2), D(1-4)
    # Case(int) - which set of case data parse C1/C4/C5
    # Local path to simulation slice data (str)

#interp()
    # __init__
    # interp_Q interpolation method
    # interp_D interpolation method


class interp():

    def __init__(self, analysis_type, slice_number, case_number, local_dir):
        self.local_dir = local_dir
        exp_file = "C" + str(case_number) + "_" + analysis_type + str(slice_number) + ".csv"
        exp_git_url = "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C{}_sampling_coordinates/C{}_Experimental_Slice_Data/"+exp_file.format(case_number)
        self.experimental_df = pd.read_csv(exp_git_url)


    def interp_Q(self):
        # Create list of interpolation points
        interpolation_points = self.experimental_df['radius'].tolist()
        self.df_interp = pd.DataFrame(interpolation_points)

        # TODO: check self.local_dir string format if only /* or * needed for all filenames in that folder
        filenames = [os.path.basename(x) for x in glob.glob(self.local_dir+"*")]

        # Load df for loop
        for file in filenames:
            sim_df = pd.read_csv(file, header=0, delim_whitespace=True)
            #create radius column
            sim_df['radius'] = np.sqrt(sim_df['x-coordinate'] ** 2 + sim_df['y-coordinate'] ** 2)

            #set index to radius
            sim_df = sim_df.set_index('radius')

            # append simulation df with interpolation points and interpolate linearly
            sim_df = sim_df.reindex(sim_df.index.union(interpolation_points)).sort_index(ascending=True).interpolate(method='index')

            # extract interpolated values into temporary list
            interp_values = []
            for radii in interpolation_points:
                # print(simulation_df['velocity-magnitude'][i])
                interp_values.append(sim_df['velocity-magnitude'][radii])
            self.df_interp[file] = interp_values
            return self.df_interp














if __name__ == "__main__":
    # # Load experimental CSV
    # experimental_df = pd.read_csv(
    #     'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_Q1.csv')
    # # Create list of interpolation points
    # interpolation_points = experimental_df['radius'].tolist()
    #
    # # Load Simulation CSV
    # simulation_df = pd.read_csv('/Users/jdtarriela/Downloads/Q1-c5/Q1/q1-8000', header=0, delim_whitespace=True)
    # # create radius column
    # simulation_df['radius'] = np.sqrt(simulation_df['x-coordinate'] ** 2 + simulation_df['y-coordinate'] ** 2)
    # # set index to radius
    # simulation_df = simulation_df.set_index('radius')
    # # append simulation df with interpolation points and interpolate linearly
    # simulation_df = simulation_df.reindex(simulation_df.index.union(interpolation_points)).sort_index(
    #     ascending=True).interpolate(method='index')
    #
    # # extract interpolated values into temporary list
    # interpolated_values = []
    # for i in interpolation_points:
    #     # print(simulation_df['velocity-magnitude'][i])
    #     interpolated_values.append(simulation_df['velocity-magnitude'][i])
    #
    # # Create dataframe of interpolated points and associated values
    # # TODO how to initialzie dataframe and create new columns in loop
    # # when empty dataframe created when points are indexed as only column
    #
    # df_interp = pd.DataFrame(interpolation_points)
    # df_interp['velocity_1'] = interpolated_values
    # df_interp = df_interp.set_index([0])
    #

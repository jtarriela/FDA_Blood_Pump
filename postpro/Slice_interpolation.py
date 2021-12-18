import pandas as pd
import numpy as np
import os, glob

#TODO create class to extract line and quadrant data
#TODO local grab list of all files via glob for Q or D

# How to use:
# Examples in: if __name__ == "__main__":
# args:
    # Analysis Type(str) - accepts "Q" or "D" -extracting quadrant or diffuser data
    # Slice Number(int) - Q(1-2), D(1-4)
    # Case(int) - which set of case data parse C1/C4/C5
    # Local path to simulation slice data (str)
    # Operating_system =(str) "win" or "osx"

#interp()
    # __init__
    # interp_Q interpolation method
    # interp_D interpolation method



class interp():

    def __init__(self, analysis_type, slice_number, case_number, local_dir,operating_system):
        if operating_system == "win":
            self.local_dir = local_dir + r"\*"
        elif operating_system == "osx":
            self.local_dir = local_dir + r"/*"
        print("Local Directory: "+local_dir)

        exp_file = "C" + str(case_number) + "_" + analysis_type + str(slice_number) + ".csv"
        exp_git_url = "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C{}_sampling_coordinates/C{}_Experimental_Slice_Data/".format(case_number,case_number)+exp_file
        print(exp_git_url)
        self.experimental_df = pd.read_csv(exp_git_url)


    def interp_Q(self):
        # Create list of interpolation points
        interpolation_points = self.experimental_df['radius'].tolist()
        self.df_interp_Q = pd.DataFrame(interpolation_points)

        # TODO: check self.local_dir string format if only /* or * needed for all filenames in that folder
        filenames = [os.path.basename(x) for x in glob.glob(self.local_dir)]
        print(filenames)

        # Load df for loop
        for file in filenames:
            #remove "*" in self.local_dir
            file_path = self.local_dir.rstrip(self.local_dir[-1])
            #reading each file & append file name to file_path
            sim_df = pd.read_csv(file_path+file, header=0, delim_whitespace=True)
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
            self.df_interp_Q[file] = interp_values
        self.df_interp_Q = self.df_interp_Q.set_index([0])
        self.df_interp_Q["average-velocity"] = self.df_interp_Q.mean(axis=1)
        self.df_interpQ= self.df_interp_Q.reset_index(inplace=True)
        return self.df_interp_Q

    def interp_D(self):
        interpolation_points = self.experimental_df['y-coord'].tolist()
        # print(interpolation_points)
        self.df_interp_D = pd.DataFrame(interpolation_points)

        filenames = [os.path.basename(x) for x in glob.glob(self.local_dir)]
        # print(self.local_dir)
        print(filenames)

        for file in filenames:
            #remove "*" in self.local_dir
            file_path = self.local_dir.rstrip(self.local_dir[-1])
            #reading each file & append file name to file_path
            sim_df = pd.read_csv(file_path+file, header=0, delim_whitespace=True)


            sim_df = sim_df.drop(columns=['z-coordinate', 'x-coordinate', 'cellnumber'])

            #set index to z-coordinate
            sim_df = sim_df.set_index('y-coordinate')

            # append simulation df with interpolation points and interpolate linearly
            sim_df = sim_df.reindex(sim_df.index.union(interpolation_points)).sort_index(ascending=True).interpolate(method='index')

            # extract interpolated values into temporary list
            interp_values = []
            for point in interpolation_points:
                # print(simulation_df['velocity-magnitude'][i])
                interp_values.append(sim_df['velocity-magnitude'][point])
            self.df_interp_D[file] = interp_values
        self.df_interp_D = self.df_interp_D.set_index([0])

        self.df_interp_D["average-velocity"] = self.df_interp_D.mean(axis=1)
        self.df_interp_D = self.df_interp_D.dropna()
        # self.df_interp_D = self.df_interp_D.reset_index(inplace=True)
        return self.df_interp_D




if __name__ == "__main__":

    path = r"C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Core\Cond_5-SBES_19M_BP\Velocity_slices\Q2"
    test_interp_class = interp("Q",2,1,path,"win")
    test_interp_q1 = test_interp_class.interp_Q()


    path2 = r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Core\Cond_5-SBES_19M_BP\Velocity_slices\D2'
    test_interp_class = interp("D", 2, 1, path2, "win")
    test_interp_d1 = test_interp_class.interp_D()


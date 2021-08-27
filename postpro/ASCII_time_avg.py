import os, glob
import pandas as pd
import numpy as np


class ascii_averaging:
    def __init__(self, filepaths):
        self.filepaths = filepaths

    def blade_quadrant_ave(self):
        working = [pd.read_csv(file, header=0, delim_whitespace=True)
                   for file in self.filepaths]

        df_appended = pd.DataFrame()
        for i in enumerate(working):
            df_appended = df_appended.append(i[1], ignore_index=True)

        df_appended['radius'] = np.sqrt(df_appended['x-coordinate'] ** 2 + df_appended['y-coordinate'] ** 2)
        resid_col_list = df_appended.columns
        col_list = df_appended.columns[0:].copy()

        df_appended["Bins"] = pd.cut(df_appended['radius'], bins=2000)
        df_appended["bin_centres"] = df_appended["Bins"].apply(lambda x: x.mid)
        df_appended['Counts'] = df_appended.groupby(['Bins'])[col_list[0]].transform('count')
        df_appended['Bin Variance'] = df_appended.groupby(['Bins'])[col_list[0]].transform('var')

        for variable in enumerate(resid_col_list):
            # print(variable)
            if variable[0] == 0:
                # skip first column "Time_step"
                pass
            else:
                # print(variable)
                col_bin_var_mean = variable[1] + "_bin_mean"
                col_bin_std = variable[1] + "_std"
                col_bin_sem = variable[1] + "_sem"
                df_appended[col_bin_var_mean] = df_appended.groupby('Bins')[col_list[variable[0]]].transform('mean')
                df_appended[col_bin_std] = df_appended.groupby('Bins')[col_list[variable[0]]].transform('std')
                df_appended[col_bin_sem] = df_appended.groupby('Bins')[col_list[variable[0]]].transform('sem')

        df_appended = df_appended.drop_duplicates(subset="Bins")
        df_appended = df_appended.reset_index()
        df_appended = df_appended.drop(resid_col_list, axis=1)
        return df_appended

    def diffuser_ave(self):
        df = [pd.read_csv(file, header=0, delim_whitespace=True)
              for file in self.filepaths]

        # Appending Slice data single dataframe
        df_appended = pd.DataFrame()
        for i in enumerate(df):
            # print(i[1])
            df_appended = df_appended.append(i[1], ignore_index=True)

        raw_df_appended = df_appended.copy()

        # df_appended['radius'] = np.sqrt(df_appended['x-coordinate']**2 + df_appended['y-coordinate']**2)

        # Use df.copy(): indexing a DataFrame returns a reference to the initial DataFrame.
        # Thus, changing the subset will change the initial DataFrame.
        # Thus, you'd want to use the copy if you want to make sure the initial DataFrame shouldn't change.
        resid_col_list = df_appended.columns
        col_list = df_appended.columns[0:].copy()

        df_appended["Bins"] = pd.cut(df_appended[col_list[2]], bins=2000)
        df_appended["bin_centres"] = df_appended["Bins"].apply(lambda x: x.mid)
        df_appended['Counts'] = df_appended.groupby(['Bins'])[col_list[0]].transform('count')
        df_appended['Bin Variance'] = df_appended.groupby(['Bins'])[col_list[0]].transform('var')
        for variable in enumerate(resid_col_list):
            # print(variable)
            if variable[0] == 0:
                # skip first column "Time_step"
                pass
            else:
                # print(variable)
                col_bin_var_mean = variable[1] + "_bin_mean"
                col_bin_std = variable[1] + "_std"
                col_bin_sem = variable[1] + "_sem"
                df_appended[col_bin_var_mean] = df_appended.groupby('Bins')[col_list[variable[0]]].transform('mean')
                df_appended[col_bin_std] = df_appended.groupby('Bins')[col_list[variable[0]]].transform('std')
                df_appended[col_bin_sem] = df_appended.groupby('Bins')[col_list[variable[0]]].transform('sem')

        df_appended = df_appended.drop_duplicates(subset="Bins")
        df_appended = df_appended.reset_index()
        df_appended = df_appended.drop(resid_col_list, axis=1)

        # Averages Y position of cells in bins
        # Averages Velocity of cells in bins
        return df_appended

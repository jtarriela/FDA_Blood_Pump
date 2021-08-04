import os, glob, sys
import pandas as pd


#### Change header from 'Time Step' to 'Time_Step'
# Changing the current working directory
dir_path = '/Users/jdtarriela/Desktop/trans_log/5e-5/resid_rev_1-5'
dir_path_2 = '/Users/jdtarriela/Desktop/trans_log/5e-5/resid_rev_6-15'
out_file = '/Users/jdtarriela/Desktop/trans_log/5e-5/resid_1-15.csv'

####################### First Set #############################
os.chdir(dir_path)

# Getting the FileNames of all .csv files in the current dir.
# Ensure first dir has all files to analyze in subsequent datasets
# filenames list propagates through all folders
filenames = [i for i in glob.glob(f"*.out")]

# Loading all the csv files to create a list of data frames
df = [pd.read_csv(file, header=1, sep=" ", doublequote=True)
        for file in filenames]

for i in range(0,len(df)):
    # df[i] = df[i].T                # Transposing Dataframes
    df[i] = df[i].iloc[1:]           # Creating first row as Header
    df[i] = df[i].reset_index(drop=True)

    # Use if simulation stopped before/after save.
    # If simulation resid does not stop on a blade pass
    # df[i] = df[i].drop(df[i].index[1800:]) #drop last x iterations

#
residual_df = pd.DataFrame()
for i in enumerate(df):
    col_to_import = df[i[0]].columns[1]
    print('current column import: ' + col_to_import)
    residual_df['Time_Step'] = df[i[0]]['Time_Step']
    residual_df[col_to_import]=df[i[0]][col_to_import]
####################### Second Set #############################

os.chdir(dir_path_2)
df = [pd.read_csv(file, header=1, sep=" ", doublequote=True)
        for file in filenames]

for i in range(0,len(df)):
    # df[i] = df[i].T                # Transposing Dataframes
    df[i] = df[i].iloc[1:]           # Creating first row as Header
    df[i] = df[i].reset_index(drop=True)


residual_df_2 = df[0].copy()

for i in enumerate(df):
    col_to_import = df[i[0]].columns[1]
    print('current column import' + col_to_import)
    residual_df_2['Time_Step'] = df[i[0]]['Time_Step']
    residual_df_2[col_to_import]=df[i[0]][col_to_import]

####################### Third Set #############################

# os.chdir(dir_path_3)
# df = [pd.read_csv(file, header=1, sep=" ", doublequote=True)
#       for file in filenames]
#
# for i in range(0, len(df)):
#     # df[i] = df[i].T                # Transposing Dataframes
#     df[i] = df[i].iloc[1:]  # Creating first row as Header
#     df[i] = df[i].reset_index(drop=True)
#
# residual_df_3 = df[0].copy()
#
# for i in enumerate(df):
#     col_to_import = df[i[0]].columns[1]
#     residual_df_2['Time_Step'] = df[i[0]]['Time_Step']
#     print(col_to_import)
#     residual_df_2[col_to_import] = df[i[0]][col_to_import]

resid_all = residual_df.append(residual_df_2, ignore_index=True)
# resid_all = residual_df.resid_all(residual_df_3, ignore_index=True)

resid_all.to_csv(path_or_buf=out_file,
                 index=False,
                 sep=' ')

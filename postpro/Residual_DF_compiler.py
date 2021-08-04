import os, glob, sys
import pandas as pd
# Changing the current working directory
dir_path = '/Users/jdtarriela/Desktop/trans_log/1.5e-5/r1/'
dir_path_2 = '/Users/jdtarriela/Desktop/trans_log/1.5e-5/r2/'
out_file = '/Users/jdtarriela/Desktop/trans_log/1.5e-5/resid_all.csv'
os.chdir(dir_path)

# Getting the FileNames of all .csv files in the current dir.
filenames = [i for i in glob.glob(f"*.out")]

# Loading all the csv files to create a list of data frames
df = [pd.read_csv(file, header=1, sep=" ", doublequote=True)
        for file in filenames]

for i in range(0,len(df)):
    # df[i] = df[i].T                # Transposing Dataframes
    df[i] = df[i].iloc[1:]           # Creating first row as Header
    df[i] = df[i].reset_index(drop=True)
    df[i] = df[i].drop(df[i].index[361:]) #drop last x iterations

#
residual_df = pd.DataFrame()
for i in enumerate(df):
    col_to_import = df[i[0]].columns[1]
    residual_df['Time_Step'] = df[i[0]]['Time_Step']
    print(col_to_import)
    residual_df[col_to_import]=df[i[0]][col_to_import]


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
    residual_df_2['Time_Step'] = df[i[0]]['Time_Step']
    print(col_to_import)
    residual_df_2[col_to_import]=df[i[0]][col_to_import]

resid_all = residual_df.append(residual_df_2, ignore_index=True)

resid_all.to_csv(path_or_buf=out_file,
                 index=False,
                 sep=' ')

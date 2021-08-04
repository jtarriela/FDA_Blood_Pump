# https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/eds-hemolysis_1201.out

import pandas as pd

text = r"https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-GW-a_1201.out"
resid_5_link = {'point_gw-A': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-GW-a_1201.out',
                'point_gw-B': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-GW-b_1201.out',
                'point_gw-C': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-GW-c_1201.out',
                'point_gw-D': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-GW-d_1201.out',
                'point_gw-E': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-GW-e_1201.out',
                'point_pressure-A': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-pressure-a_1201.out',
                'point_pressure-B': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-pressure-b_1201.out',
                'point_pressure-C': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-pressure-c_1201.out',
                'point_pressure-D': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-pressure-d_1201.out',
                'point_pressure-E': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-pressure-e_1201.out',
                'point_shear-A': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-shear-a_1201.out',
                'point_shear-B': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-shear-b_1201.out',
                'point_shear-C': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-shear-c_1201.out',
                'point_shear-D': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-shear-d_1201.out',
                'point_shear-E': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-shear-e_1201.out',
                'point_vel-A': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-vel-a_1201.out',
                'point_vel-B': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-vel-b_1201.out',
                'point_vel-C': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-vel-c_1201.out',
                'point_vel-D': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-vel-d_1201.out',
                'point_vel-E': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/point-vel-e_1201.out',
                'pressure-in': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Core/SBES_15M_BP/5e-5/Residuals/pressure-in_1201.out'}


residual_df = pd.DataFrame()
key_count = 0
for key in resid_5_link:

    key_count = key_count+1
    print(key, resid_5_link[key])
    df = pd.read_csv(resid_5_link[key], header=1, sep=" ", doublequote=True)
    df = df.iloc[1:]
    df = df.reset_index(drop=True)

    col_name_ts = df.columns[0]
    col_name_var = df.columns[1]
    residual_df[col_name_ts] = df[col_name_ts]
    residual_df[col_name_var] = df[col_name_var]





# data = pd.read_csv('output_list.txt', header = None)
# data = pd.read_csv('output_list.txt', sep=" ", header=None)
# data.columns = ["a", "b", "c", "etc."]
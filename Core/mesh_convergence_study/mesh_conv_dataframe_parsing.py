import pandas as pd
import numpy as np
import math

class mesh_conv_df_parser():
    def __init__(self, Mass_Flux = None, Max_Velocity = None, Total_Pressure_In = None, Total_Pressure_Out = None, Q1_Velocity = None, Q2_Velocity = None):
        self.mass_flux_link = Mass_Flux
        self.max_vel_link = Max_Velocity
        self.total_p_in_link = Total_Pressure_In
        self.total_p_out_link = Total_Pressure_Out
        self.q1_vel_link = Q1_Velocity
        self.q2_vel_link = Q2_Velocity

    def mass_flux_monitor(self):
        mass_flux_df = pd.read_csv(self.mass_flux_link,
                                   header=1,
                                   skiprows=[2],
                                   delim_whitespace=True)
        return mass_flux_df

    def max_vel_monitor(self):
        max_vel_rotor_df = pd.read_csv(self.max_vel_link,
                                       header=1,
                                       skiprows=[2],
                                       delim_whitespace=True)

        return max_vel_rotor_df

    def total_p_monitor(self):
        total_p_in = pd.read_csv(self.total_p_in_link,
                                 header=1,
                                 skiprows=[2],
                                 delim_whitespace=True)
        total_p_out = pd.read_csv(self.total_p_out_link,
                                  header=1,
                                  skiprows=[2],
                                  delim_whitespace=True)

        density = 1056  # kg/m3
        gravity = 9.81  # m/s2
        total_pressure_df = pd.DataFrame()
        total_pressure_df['Iteration'] = total_p_in["Iteration"]
        total_pressure_df['P_in (Pa)'] = total_p_in["p-in"]
        total_pressure_df['P_out (Pa)'] = total_p_out["p-out"]
        total_pressure_df['P_head (m)'] = (total_pressure_df['P_out (Pa)'] - total_pressure_df['P_in (Pa)']) / (density * gravity)
        total_pressure_df['P_head (mmHg)'] = total_pressure_df['P_head (m)'] * 73.53708129594501
        return total_pressure_df

    def Q1_vel_slice(self):
        Q1_velocity_df = pd.read_csv(self.q1_vel_link, header=1, skiprows=[1], delim_whitespace=True)
        Q1_velocity_df = Q1_velocity_df.rename(columns={'((xy/key/label': 'Position (m)', 'quadrant-1)': 'Velocity Magnitude (m/s)'})
        Q1_velocity_df.dropna(subset=['Velocity Magnitude (m/s)'], inplace=True)
        Q1_velocity_df['Position (m)'] = Q1_velocity_df['Position (m)'].astype(float)
        Q1_velocity_df['Radius (m)'] = np.sqrt((Q1_velocity_df['Position (m)'] ** 2) * 2)
        Q1_velocity_df = Q1_velocity_df.sort_values(by='Radius (m)', ascending=True)
        Q1_velocity_df.drop(Q1_velocity_df[Q1_velocity_df['Radius (m)'] > 0.03].index, inplace=True)
        return Q1_velocity_df

    def Q2_vel_slice(self):
        Q2_velocity_df = pd.read_csv(self.q2_vel_link, header=1, skiprows=[1], delim_whitespace=True)
        Q2_velocity_df = Q2_velocity_df.rename(columns={'((xy/key/label': 'Position (m)', 'quadrant-2)': 'Velocity Magnitude (m/s)'})
        Q2_velocity_df.dropna(subset=['Velocity Magnitude (m/s)'], inplace=True)
        Q2_velocity_df['Position (m)'] = Q2_velocity_df['Position (m)'].astype(float)
        Q2_velocity_df['Radius (m)'] = np.sqrt((Q2_velocity_df['Position (m)'] ** 2) * 2)
        Q2_velocity_df = Q2_velocity_df.sort_values(by='Radius (m)', ascending=True)
        Q2_velocity_df.drop(Q2_velocity_df[Q2_velocity_df['Radius (m)'] > 0.03].index, inplace=True)
        return Q2_velocity_df

    def SMA(self, df, window_size,col_name, df_iteration_truncation = None):

        if df_iteration_truncation is not None:
            sma_df = df
            sma_df.drop(sma_df[sma_df['Iteration'] > df_iteration_truncation].index, inplace=True)
        else:
            sma_df = df # nothing else is supposed to happen
        col_list = sma_df.columns[0:].copy()
        # col_list.get_loc('col_name')

        sma_df[col_name+'_SMA'] = sma_df.iloc[:, col_list.get_loc(col_name)].rolling(window=window_size).mean()
        # self.SMA_data['pandas_SMA'] = self.SMA_data.iloc[:, 1].rolling(window=self.SMA_points).mean()
        return sma_df


if __name__ == "__main__":
    dataset_link_dict = {
        'Mass_Flux': "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/mesh_convergence_study/Core/mesh_convergence_study/Convergence%20Data/Residual%20Data/Coarse/mass-flux.out",
        'Max_Velocity': "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/mesh_convergence_study/Core/mesh_convergence_study/Convergence%20Data/Residual%20Data/Coarse/max-vel-rotor.out",
        'Total_Pressure_In': "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/mesh_convergence_study/Core/mesh_convergence_study/Convergence%20Data/Residual%20Data/Coarse/pressure-in.out",
        'Total_Pressure_Out': "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/mesh_convergence_study/Core/mesh_convergence_study/Convergence%20Data/Residual%20Data/Coarse/pressure-out.out",
        'Q1_Velocity': "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/mesh_convergence_study/Core/mesh_convergence_study/Convergence%20Data/Quantity%20Data/Coarse/vel-q1",
        'Q2_Velocity': "https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/mesh_convergence_study/Core/mesh_convergence_study/Convergence%20Data/Quantity%20Data/Coarse/vel-q2"}

    parser = mesh_conv_df_parser(**dataset_link_dict)

    mass_flux = parser.mass_flux_monitor()
    Q2_vel = parser.Q2_vel_slice()
    Q1_vel = parser.Q1_vel_slice()
    total_p = parser.total_p_monitor()
    max_vel = parser.max_vel_monitor()

    max_vel_SMA = parser.SMA(max_vel, 100, 'max-vel-rotor',5000)
    # col_list = max_vel.columns[0:].copy()

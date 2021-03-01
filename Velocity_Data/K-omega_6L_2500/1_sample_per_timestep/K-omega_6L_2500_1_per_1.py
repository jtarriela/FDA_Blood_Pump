from Velocity_Processor import df_cleaner

def plot_Q1(title,url_list):
    vel_plot_title = title
    df_obj = df_cleaner(url_list, vel_plot_title)
    what = df_obj.compute_radius()
    df_plot = df_obj.velocity_plot()
    return df_plot

if __name__ == "__main__":
    # Quadrant 1 6L 2500 K-Omega
    Experimental_Q1 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    Q1_url_1 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/K-omega_6L_2500/1_sample_per_timestep/Quadrant%201%20Data/VelocityMagnitude-Q-1-k-omg.csv'
    # Q1_url_2 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/K-omega_6L_2500/Quadrant%201%20Data/RMSEVelocityMagnitude-Q-1-k-omg.csv'
    # Q1_url_3 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/K-omega_6L_2500/Quadrant%201%20Data/MeanVelocityMagnitude-Q-1-k-omg.csv'

    # Quadrant 2 6L 2500 K-Omega
    Experimental_Q2 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q2_6L_2500.csv'
    Q2_url_1 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/K-omega_6L_2500/1_sample_per_timestep/Quadrant%202%20Data/VelocityMagnitude-Q-2-k-omg.csv'
    # Q2_url_2 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/K-omega_6L_2500/Quadrant%202%20Data/RMSEVelocityMagnitude-Q-2-k-omg.csv'
    # Q2_url_3 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/K-omega_6L_2500/Quadrant%202%20Data/MeanVelocityMagnitude-Q-2-k-omg.csv'

    # URL Lists
    Q1_url_list = [Experimental_Q1, Q1_url_1]
    Q2_url_list = [Experimental_Q2, Q2_url_1]

    # Quadrant 1 Plot
    Q1_title = "Quadrant 1: 6L 2500RPM K-Omg"
    Q1_plot = plot_Q1(Q1_title, Q1_url_list)

    # Quadrant 2 Plot
    Q2_title = "Quadrant 2: 6L 2500RPM K-Omg"
    Q2_plot = plot_Q1(Q2_title, Q2_url_list)

from Velocity_Processor import df_cleaner
#Source URL here
url_df_1=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\VelocityMagnitude-Q-1-k-omg.csv'
url_df_2=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\RMSEVelocityMagnitude-Q-1-k-omg.csv'
url_df_3=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\MeanVelocityMagnitude-Q-1-k-omg.csv'


url_list = [url_df_1,url_df_2,url_df_3]

for csv in url_list:
    df_obj = df_cleaner(csv)
    df = df_obj.compute_radius()
    df_plot = df_obj.velocity_plot()


# Instantiate class and execute method
# df_obj_1=df_cleaner(url_df_1)
# df_1 = df_obj_1.compute_radius()
# df_1_plot = df_obj_1.velocity_plot()
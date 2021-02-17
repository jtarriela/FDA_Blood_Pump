import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### The intention of this script is to create classes to be called
### to compute velocity plots for different test conditions


 ## number of simultaneous csv's to process

#Source URL here
url_df_1=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\VelocityMagnitude-Q-1-k-omg.csv'
url_df_2=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\RMSEVelocityMagnitude-Q-1-k-omg.csv'
url_df_3=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\MeanVelocityMagnitude-Q-1-k-omg.csv'

# files_to_process=[url_df_1,url_df_2,url_df_3] # modify array with correct vars

# class df_cleaner():
#     def __init__(self, url):
#         self.url = url
#
#     def compute_radius(self):
#         df = pd.read_csv(self.url, index_col=0)
#         df.insert(3, "radius", 0)
#         df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
#         indexNames = df[(df['radius'] > 0.03)].index
#         df.drop(indexNames, inplace=True)
#         return df

class df_cleaner():
    def __init__(self, url):
        self.url = url

    @classmethod
    def compute_radius(cls, self):
        df = pd.read_csv(self.url, index_col=0)
        df.insert(3, "radius", 0)
        df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
        indexNames = df[(df['radius'] > 0.03)].index
        df.drop(indexNames, inplace=True)
        self.df=df

rad = df_cleaner(url_df_1)
df_cleaner.compute_radius(rad)


# def compute_radius(url):
#     df = pd.read_csv(url, index_col=0)
#     df.insert(3, "radius", 0)
#     df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
#     indexNames = df[(df['radius'] > 0.03)].index
#     df.drop(indexNames, inplace=True)
#     return df




# df_1.plot(kind='scatter',x='radius',y=df_1_header_list[4],color='red')
# plt.show()

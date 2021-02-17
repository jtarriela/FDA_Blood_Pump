import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### The intention of this script is to create classes to be called
### to compute velocity plots for different test conditions

url_df_1=r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\VelocityMagnitude-Q-1-k-omg.csv'

df_1 = pd.read_csv(url_df_1, index_col=0)
df_1.insert(3,"radius",0)
df_1['radius']=np.sqrt(df_1['    x-coordinate']**2+df_1['    y-coordinate']**2)
df_1_header_list=list(df_1.columns.values)

indexNames = df_1[ (df_1['radius'] > 0.03)].index
df_1.drop(indexNames , inplace=True)

df_1.plot(kind='scatter',x='radius',y=df_1_header_list[4],color='red')
plt.show()


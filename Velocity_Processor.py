import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### The intention of this script is to create classes to be called
### to compute velocity plots for different test conditions

class df_cleaner:
    def __init__(self, url):
        self.url = url

    def compute_radius(self):
        df = pd.read_csv(self.url, index_col=0)
        df.insert(3, "radius", 0)
        df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
        indexNames = df[(df['radius'] > 0.03)].index
        df.drop(indexNames, inplace=True)
        self.df = df
        return df

    ### Pass DF to velocity_plot() to plot velocity w.in same class
    def velocity_plot(self):
        plot_df = self.df
        df_header_list = list(plot_df.columns.values)
        plot_df.plot(kind='scatter', x='radius', y=df_header_list[4], color='red')
        plt.show()

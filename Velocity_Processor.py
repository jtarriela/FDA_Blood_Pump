import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### The intention of this script is to create classes to be called
### to compute velocity plots for different test conditions


### for some reason file paths strings arenot being parsed through the compute radius object correctly when in a list. it
### send data through in a dictionary and parse?
### https://stackoverflow.com/questions/42654934/need-of-using-r-before-path-name-while-reading-a-csv-file-with-pandas

class df_cleaner:
    def __init__(self, url):
        self.url = url
        self.url_index = np.arange(0,1,len(self.url))
        self.master_df = pd.DataFrame() # init dataframe to append in compute_radius

    # ##### incorporate if else to handle lists of dataframe string locations
    # # def compute_radius(self):
    #     if isinstance(self.url, list):
    #         ### create new sheets in new dataframe or list of dataframes
    #         ### or pull columns into different lists and pass to velocity_plot
    #
    #         for csv in self.url:
    #             df = pd.read_csv(self.url, index_col=0)
    #             df.insert(3, "radius", 0)
    #             df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
    #             indexNames = df[(df['radius'] > 0.03)].index
    #             df.drop(indexNames, inplace=True)
    #             self.df = df


    def compute_radius(self):
        for i in self.url_index:
            df = pd.read_csv(self.url[i], index_col=0)
            df.insert(3, "radius", 0)
            df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
            indexNames = df[(df['radius'] > 0.03)].index
            df.drop(indexNames, inplace=True)
            df.drop([df.columns[0], df.columns[1], df.columns[2]], axis=1, inplace=True)
            self.master_df.append(df)

        return self.master_df

        # df = pd.read_csv(self.url, index_col=0)
        # df.insert(3, "radius", 0)
        # df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
        # indexNames = df[(df['radius'] > 0.03)].index
        # df.drop(indexNames, inplace=True)
        # df.drop([df.columns[0], df.columns[1], df.columns[2]], axis=1, inplace=True)
        # self.df = df
        #
        # return df

    ### Pass DF to velocity_plot() to plot velocity w.in same class
    def velocity_plot(self):
        plot_df = self.df
        df_header_list = list(plot_df.columns.values)
        plot_df.plot(kind='scatter', x='radius', y=df_header_list[4], color='red')
        plt.show()

##class feature testing
if __name__ == "__main__":
    url_df_1 = r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\VelocityMagnitude-Q-1-k-omg.csv'
    url_df_2 = r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\VelocityMagnitude-Q-1-k-omg.csv'
    url_df_3 = r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\Velocity_Data\K-omega_6L_2500\VelocityMagnitude-Q-1-k-omg.csv'

    url_list = {url_df_1, url_df_2, url_df_3}

    for csv in url_list:
        df_obj = df_cleaner(csv)
        df = df_obj.compute_radius()
        # df_plot = df_obj.velocity_plot()

        # df.drop([df.columns[0],df.columns[1],df.columns[2]], axis=1, inplace=True)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


### The intention of this script is to create classes to be called
### to compute velocity plots for different test conditions

class df_cleaner:
    def __init__(self, url, chart_title):
        self.url = url
        self.chart_title = chart_title
        self.url_index = np.arange(0, len(self.url))
        self.master_df_list = [] # init dataframe to append in compute_radius

    def compute_radius(self):
        for i in self.url_index:
            df = pd.read_csv(self.url[i], index_col=0)
            df.insert(3, "radius", 0)
            df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
            indexNames = df[(df['radius'] > 0.03)].index
            df.drop(indexNames, inplace=True)
            df.drop([df.columns[0], df.columns[1], df.columns[2]], axis=1, inplace=True)
            self.master_df_list.append(df)

        return self.master_df_list

    ### Pass DF to velocity_plot() to plot velocity w.in same class
    def velocity_plot(self):
        all_df = pd.concat(self.master_df_list, axis=1) # append empty dataframe with df from df list
        colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
        df_column_names = []

        for i in range(len(all_df.columns)):
            if i%2 == 0 and i < len(all_df.columns)-1:
                # print("even")
                plt.plot(all_df.iloc[:, i], all_df.iloc[:, i + 1], colours[i],marker='o',linestyle='dashed', linewidth=1, markersize=5)
                df_column_names.append(all_df.columns[i+1])
            else:
                pass
        plt.legend(df_column_names)
        plt.ylabel('Velocity (m/s)')
        plt.xlabel('Radius (m)')
        plt.title(self.chart_title)
        figure = plt.figure()

        return figure




##class feature testing

# if __name__ == "__main__":
    # ### Define raw github path and insert into list // lets me work on mac when pushed
    # url_df_1 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    # url_df_2 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    # url_df_3 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    # url_df_4 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    # url_df_5 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    # url_df_6 = 'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/Velocity_Data/Experimental_6L_2500/Q1_6L_2500.csv'
    #
    # #### Function input always list
    # url_list = [url_df_1, url_df_2, url_df_3,url_df_4,url_df_5,url_df_6]
    # ### Insert Chart Title
    # vel_plot_title = "test title"
    #
    # df_obj = df_cleaner(url_list,vel_plot_title)
    # df = df_obj.compute_radius()
    # df_plot = df_obj.velocity_plot()



    # master_df_list = [] # Empty dataframe list
    #
    #
    # for i in index:
    #     df = pd.read_csv(url_list[i], index_col=0)
    #     # master_df.append(df)
    #
    #     df.insert(3, "radius", 0)
    #     df['radius'] = np.sqrt(df['    x-coordinate'] ** 2 + df['    y-coordinate'] ** 2)
    #     indexNames = df[(df['radius'] > 0.03)].index
    #     df.drop(indexNames, inplace=True)
    #     df.drop([df.columns[0], df.columns[1], df.columns[2]], axis=1, inplace=True)
    #
    #     master_df_list.append(df) # append empty list with all dataframes
    #
    # all_df = pd.concat(master_df_list, axis=1) # append empty dataframe with df from df list
    #
    # colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w', 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    # df_column_names = []
    #
    #
    # for i in range(len(all_df.columns)):
    #     if i%2 == 0 and i < len(all_df.columns)-1:
    #         # print("even")
    #         plt.plot(all_df.iloc[:, i], all_df.iloc[:, i + 1], colours[i],marker='o',linestyle='dashed', linewidth=1, markersize=5)
    #         df_column_names.append(all_df.columns[i+1])
    #     else:
    #         pass
    # plt.legend(df_column_names)
    # plt.ylabel('Velocity (m/s)')
    # plt.xlabel('Radius (m)')
    # plt.show()


    # for csv in url_list:
    #     df_obj = df_cleaner(csv)
    #     df = df_obj.compute_radius()
    #     df_plot = df_obj.velocity_plot()
    #
    #     df.drop([df.columns[0],df.columns[1],df.columns[2]], axis=1, inplace=True)

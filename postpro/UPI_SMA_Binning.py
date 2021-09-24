import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
import numpy as np
from scipy import stats
from pytictoc import TicToc
import math
# plt.ion()
class PAA_UPI():

    def __init__(self, df, Bin_size = None, UPI = None, SMA_points = None):
        self.raw_data = df
        self.col_list = data.columns[0:].copy()

        if Bin_size is not None:
            self.number_bins = Bin_size
        if UPI is not None:
            self.UPI = UPI
        if SMA_points is not None:
            self.SMA_points = SMA_points

        # self.fig_1 = plt.figure(1)
        # self.fig_2 = plt.figure(2)
        # self.ax_1 = self.fig_1.gca()
        # self.ax_2 = self.fig_1.gca()
        # Create case handling for invalid input


    def SMA_calc(self):
        self.SMA_data = self.raw_data[[self.col_list[0], self.col_list[1]]].copy()
        self.SMA_data['pandas_SMA'] = self.SMA_data.iloc[:, 1].rolling(window=self.SMA_points).mean()
        return self.SMA_data
        # data['pandas_SMA'] = data.iloc[:, 1].rolling(window=SMA_points).mean()

    def PAA_calc(self):
        # UPI = UPI  # 90% Interval
        # self.number_bins = int(input("Enter initial bin size as int:"))
        # self.UPI = float(input("Enter Upper Confidence Interval (0-1):"))


        self.PAA_data = self.raw_data[[self.col_list[0], "Torque"]].copy()

        self.PAA_data["Bins"] = pd.cut(self.PAA_data[self.col_list[0]], bins=self.number_bins)
        self.PAA_data['Counts'] =  self.PAA_data.groupby(['Bins'])[self.col_list[0]].transform('count')
        self.PAA_data['Bin Variance'] =  self.PAA_data.groupby(['Bins'])[self.col_list[0]].transform('var')

        # Some parse criteria for bins
        # Find mean of bins
        self.PAA_data["Binned Dependant Var Mean"] =  self.PAA_data.groupby('Bins')[self.col_list[1]].transform('mean')
        # This is the Sample Std of bins --- SAMPLE OR POPULATION IS THIS CORRECT???
        self.PAA_data["Binned Dependant Var Sample Std"] =  self.PAA_data.groupby('Bins')[self.col_list[1]].transform('std')
        # remove time/torque col and duplicates
        self.PAA_data["Mean Binned Independent Var"] =  self.PAA_data.groupby('Bins')[self.col_list[0]].transform('mean')
        self.PAA_data =  self.PAA_data.drop_duplicates(subset="Bins")
        self.PAA_data =  self.PAA_data.reset_index()

        # hamiltonian stats magic - UPI = UPPER PREDICTION INTERVAL

        test_array = np.arange(0, self.number_bins)
        for i in test_array:
            # print(i)
            # bin_data["stdModFactor"] = stats.t.ppf(UPI, count-1)*np.sqrt(1+1/count)
            self.PAA_data.loc[i, "stdModFactor"] = stats.t.ppf(self.UPI, self.PAA_data.loc[i, "Counts"] - 1) * \
                                                   np.sqrt(1 + 1 / self.PAA_data.loc[i, "Counts"])
            # modStd = std * stdModFactor
            self.PAA_data.loc[i, "modStd"] = self.PAA_data.loc[i, "Binned Dependant Var Sample Std"] * \
                                             self.PAA_data.loc[i, "stdModFactor"]
            # nn_UPI_df = mean_df['Load (lbf)'] + modStd
            self.PAA_data.loc[i, "Upper Prediction Interval"] = self.PAA_data.loc[i, "Binned Dependant Var Mean"] + \
                                                                       self.PAA_data.loc[i, "modStd"]
        # Plot against raw.

        print("Number of Bins: {}"
              "\nUpper Prediction Interval: {}\n".format(self.number_bins, self.UPI))

        return self.PAA_data

    def iteractive_PAA(self):
        # self.User_in = input("Is data binned properly? [Y] [N]")
        user_in = "no"
        n_pauses = 60
        pause_interval = 60
        while user_in in ['n', 'N', 'no', 'No', 'NO']:

            self.number_bins = int(input("Enter initial bin size as int:"))
            self.UPI = float(input("Enter Upper Confidence Interval (0-1):"))
            self.SMA_points = int(input("Enter range (n-points) for Simple Moving Average as int:"))
            self.SMA_calc()
            self.PAA_calc()

            # self.interactive_plot()
            self.plot()

            plt.draw()
            plt.pause(30)
            # plt.waitforbuttonpress() https://stackoverflow.com/questions/15582956/how-to-pause-a-pylab-figure-until-a-key-is-pressed-or-mouse-is-clicked

            user_in_temp = input("Is data binned properly? [Y] [N]")
            # user_in_temp = input("Is data binned properly? [Y] [N]").upper()

            if user_in_temp in ['y', 'Y', 'yes', 'Yes', 'YES']:
                print("Done")
                user_in = user_in_temp

            elif user_in_temp in ['n', 'N', 'no', 'No', 'NO']:
                user_in = user_in_temp


    def interactive_plot(self):
        x = self.SMA_data[self.col_list[0]]
        y = self.SMA_data[self.col_list[1]]

        self.ax_1.clear()
        plt.xlabel("Time (sec)")
        plt.ylabel("Torque (Nm")
        plt.title("Distal Module: Bailout Torque Curve"
                  "\n ADM Experimental Data")

        self.ax_1.plot(x, y, 'bo', markersize=2.5, label="Experimental Data")
        SMA_legend = "Simple Moving Average" \
                     "\n{} Point Windwow".format(self.SMA_points)
        self.ax_1.plot(x, self.SMA_data["pandas_SMA"], 'r-', linewidth=2, label=SMA_legend)
        self.ax_1.plot(self.PAA_data["Mean Binned Independent Var"], self.PAA_data["Upper Prediction Interval"], 'y-', linewidth=2,
                 label="UPI = {}".format(self.UPI))
        plt.legend(loc="upper right", fontsize='medium', frameon=True, shadow=True)

    def plot(self):

        x = self.SMA_data[self.col_list[0]]
        y = self.SMA_data[self.col_list[1]]

        self.fig1 = plt.figure()
        plt.xlabel("Time (sec)")
        plt.ylabel("Torque (Nm")
        plt.title("Distal Module: Bailout Torque Curve"
                  "\n ADM Experimental Data")
        plt.plot(x, y, 'bo', markersize=2.5, label="Experimental Data")
        SMA_legend = "Simple Moving Average" \
                     "\n{} Point Windwow".format(self.SMA_points)
        plt.plot(x, self.SMA_data["pandas_SMA"], 'r-', linewidth=2, label=SMA_legend)
        plt.plot(self.PAA_data["Mean Binned Independent Var"], self.PAA_data["Upper Prediction Interval"], 'y-', linewidth=2,
                 label="UPI = {}".format(self.UPI))
        plt.legend(loc="upper right", fontsize='medium', frameon=True, shadow=True)
        # plt.pause(20)
        # plt.show()

        # self.fig2 = self.PAA_data.plot.bar(x="Bins", y="Upper Prediction Interval")


if __name__ == "__main__":
    import random
    t = TicToc()  # create instance of class
    t.tic()  # Start timer

    raw_data = pd.read_csv(r"C:\Users\jtarriel\OneDrive - JNJ\Experimental Detent Tester\2021-03-02T14-37-02_EB30PNDR02049024_bailout_actuation_results.csv")
    data = raw_data.drop(columns=["Position"])
    interactive = PAA_UPI(data).iteractive_PAA()
    static_SMA = PAA_UPI(data, 100, 0.99, 50).SMA_calc()
    static_PAA = PAA_UPI(data, 200, 0.99, 50).PAA_calc()



    t.toc()  # Time elapsed since t.tic()
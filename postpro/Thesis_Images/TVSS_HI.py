import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import groupby

def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos+.0005, xpos+.0005], [ypos + .335, ypos],
                      transform=ax.transAxes,
                      color='black',
                      linewidth=.5)
    line.set_clip_on(False)
    ax.add_line(line)


def label_len(my_index, level):
    labels = my_index.get_level_values(level)
    return [(k, sum(1 for i in g)) for k, g in groupby(labels)]


def label_group_bar_table(ax, df):
    ypos = -.335
    scale = 1. / df.index.size
    for level in range(df.index.nlevels)[::-1]:
        pos = 0
        for label, rpos in label_len(df.index, level):
            lxpos = (pos + .5 * rpos) * scale
            ax.text(lxpos, ypos, label, ha='center', transform=ax.transAxes)
            add_line(ax, pos * scale, ypos)
            pos += rpos
        add_line(ax, pos * scale, ypos)
        ypos -= .1

plt.style.use(['science'])
# Style location : C:\Users\Joseph Tarriela\.matplotlib\stylelib
plt.rcParams.update({
    "font.serif": ['Times New Roman'],  # specify font here
    "font.size": 10,
    'figure.figsize': [6, 3]
    })          # specify font size here


tvss_hi = pd.read_csv(r'C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\Thesis_Images\Plot_Data\TVSS_HI.csv',index_col=0)

y = tvss_hi.loc[['GW TVSS']]
x = [.75, 1, 1.25, 1.75, 2, 2.25, 2.75, 3, 3.25, 3.75, 4, 4.25]
x_labels = ['SBES', 'IDDES', 'KW-SST','SBES', 'IDDES', 'KW-SST', 'SBES', 'IDDES', 'KW-SST', 'SBES', 'IDDES', 'KW-SST']

fig = plt.figure()
ax1 = fig.add_subplot(111)
index = tvss_hi.index

ax1.scatter(x, tvss_hi.loc[[index[0]]], c='b', marker="s", s=18, label='GW TVSS')
ax1.scatter(x, tvss_hi.loc[[index[1]]], c='orange', marker=">", s=18, label='HO TVSS')
ax1.scatter(x, tvss_hi.loc[[index[2]]], c='g', marker="d", s=18, label='TZ TVSS')
ax1.scatter(x, tvss_hi.loc[[index[3]]], c='r', marker="+", s=18, label='DP TVSS')


experimental_y = [8.90435E-05, 7.7913E-05, 7.7913E-05, 0.00024646]
error_low = [6.90E-05, 5.88E-05, 4.45E-05, 0.000209423]
error_hi = [1.16E-04, 6.31E-05, 5.19E-05, 0.000197209]

plt.errorbar([1, 2, 3, 4], experimental_y, yerr=[error_low, error_hi], ms=4, fmt='o', c='b', capsize=3)

plt.xticks(x)
ax1.set_xticklabels(x_labels, rotation = 40)

# Replace index names b/c currently lazy and the label_group_bar
# function below pulls index as second categorical instead of list of category
indexNamesArr = tvss_hi.index.values
indexNamesArr[0] ='Condition 1'
indexNamesArr[1] ='Condition 4'
indexNamesArr[2] ='Condition 5'
indexNamesArr[3] ='Condition 6'

label_group_bar_table(ax1, tvss_hi)

# X bottom/top minor ticks
plt.tick_params(
    axis='x',  # changes apply to the x-axis
    which='minor',  # both major and minor ticks are affected
    bottom=False,  # ticks along the bottom edge are off
    top=False,  # ticks along the top edge are off
    labelbottom=False)  # labels along the bottom edge are off
# X Top Major ticks
plt.tick_params(
    axis='x',  # changes apply to the x-axis
    which='major',  # both major and minor ticks are affected
    # bottom=False,      # ticks along the bottom edge are off
    top=False,  # ticks along the top edge are off
    labelbottom=True)  # labels along the bottom edge are off

ax1.set_yscale('log')

plt.legend(loc='best', frameon=True, shadow=False)

plt.ylabel('HI\%')
plt.subplots_adjust(top=0.96)
plt.subplots_adjust(bottom=0.275)
plt.subplots_adjust(left=0.1)
plt.subplots_adjust(right=0.9)


plt.savefig(r"C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\Thesis_Images\Exported_Images\TVSS-HI.png",dpi=600)

plt.show()



import matplotlib.pyplot as plt

plt.style.use(['science'])
# Style location : C:\Users\Joseph Tarriela\.matplotlib\stylelib
plt.rcParams.update({
    "font.serif": ['Times New Roman'],  # specify font here
    "font.size": 10})          # specify font size here

sbes_x = [1.2, 2.2, 3.2, 4.2]
sbes_y = [174.7893068, 69.75158192, 264.3917632, 223.6217248]
iddes_x = [1.4, 2.4, 3.4, 4.4]
iddes_y = [177.4867949, 69.66816148, 283.0810207, 234.0348667]
kw_x = [1.6, 2.6, 3.6, 4.6]
kw_y = [157.5541319, 37.68651136, 236.2279368, 183.9224917]
experimental_x = [1, 2, 3, 4]
experimental_y = [169.5422535, 63.38028169, 264.6126761, 207.2519084]

error_hi = [12.67605634, 17.42957746, 22.18309859, 32.0610687]
error_low = [14.26056338, 22.18309859, 22.18309859, 35.49618321]

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.scatter(experimental_x, experimental_y, c='b', marker="o", s=18,label='Experimental')
ax1.scatter(sbes_x, sbes_y, c='orange', marker="s", s=18, label='SBES')
ax1.scatter(iddes_x, iddes_y, c='g', marker="^", s=18, label='IDDES')
ax1.scatter(kw_x, kw_y, c='r', marker="s", s=18, label='KW-SST')

plt.errorbar(experimental_x, experimental_y, yerr=[error_low, error_hi], ms=4, fmt='o', c='b', capsize=3)

tick_labels = ['0', '1', '4', '5', '6']
ax1.set_xticklabels(tick_labels)

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
# Y major/minor ticks
plt.tick_params(
    axis='y',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    left=True,  # ticks along the bottom edge are off
    right=False,  # ticks along the top edge are off
    labelbottom=False)  # labels along the bottom edge are off

plt.legend(loc='best', frameon=True, shadow=False)
# bbox_to_anchor=(.55, .425)
# plt.legend(bbox_to_anchor=(.54, .42),
#            frameon=False,
#            fontsize='small',
#            edgecolor='inherit')

plt.xlabel('Flow Condition')
plt.ylabel('Pressure Head (mmHg)')
plt.subplots_adjust(top=0.925)
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(left=0.15)
plt.subplots_adjust(right=0.95)
# plt.subplots_adjust(wspace=0.15)
plt.savefig(r"C:\Users\Joseph Tarriela\Documents\GitHub\FDA_Blood_Pump\postpro\Thesis_Images\Exported_Images\Pressure_Comparison.png",dpi=600)
plt.show()

import numpy as np
import tecplot as tp
import pandas as pd
import time
from tecplot.constant import *
from postpro.TecPlot.python import tputils
from postpro.TecPlot.python import tpmath

# Purpose of this script is to interpolate results from each file onto a single mesh for averaging
# Additionally, the script takes experimental datapoints and interpolates from calculated mean data



def experimental_df_loader(Case):
    # input: "C1_Experimental"
    # input: "C4_Experimental"
    # input: "C5_Experimental"

    C1_Experimental = {
        'D1': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C1_sampling_coordinates/C1_Experimental_Slice_Data/C1_D1.csv',
        'D2': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C1_sampling_coordinates/C1_Experimental_Slice_Data/C1_D2.csv',
        'D3': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C1_sampling_coordinates/C1_Experimental_Slice_Data/C1_D3.csv',
        'D4': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C1_sampling_coordinates/C1_Experimental_Slice_Data/C1_D4.csv',
        'Q1': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C1_sampling_coordinates/C1_Experimental_Slice_Data/C1_Q1.csv',
        'Q2': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C1_sampling_coordinates/C1_Experimental_Slice_Data/C1_Q2.csv'}

    C4_Experimental = {
        'Q1': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C4_sampling_coordinates/C4_Experimental_Slice_Data/C4_Q1.csv',
        'Q2': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C4_sampling_coordinates/C4_Experimental_Slice_Data/C4_Q2.csv'}

    C5_Experimental = {
        'D1': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_D1.csv',
        'D2': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_D2.csv',
        'D3': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_D3.csv',
        'D4': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_D4.csv',
        'Q1': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_Q1.csv',
        'Q2': r'https://raw.githubusercontent.com/jtarriela/FDA_Blood_Pump/main/postpro/C5_sampling_coordinates/C5_Experimental_Slice_Data/C5_Q2.csv'}

    if Case == "C1_Experimental":
        for i in enumerate(C1_Experimental):
            C1_Experimental[i[1]] = pd.read_csv(C1_Experimental[i[1]])
        return  C1_Experimental

    elif Case == "C4_Experimental":
        for i in enumerate(C4_Experimental):
            C4_Experimental[i[1]] = pd.read_csv(C4_Experimental[i[1]])
        return C4_Experimental

    elif Case == "C5_Experimental":
        for i in enumerate(C5_Experimental):
            C5_Experimental[i[1]] = pd.read_csv(C5_Experimental[i[1]])
        return C5_Experimental

def append_interpolation_xy_points(df,dataset_label):
    zone = dataset.add_ordered_zone(dataset_label, len(df))
    zone.values('CoordinateX')[:] = df['x-coord'].tolist()
    zone.values('CoordinateY')[:] = df['y-coord'].tolist()
    return


tp.session.connect()
frame = tp.active_frame()
with tp.session.suspend():
    dataset = frame.dataset
    index_zones = []

    # # Looping through zones by index
    for zindex in range(dataset.num_zones):
        z_num = zindex+1 # Adding 1 because summation function within averaging function  uses 1-based zone indices
        index_zones.append(z_num)
        dataset.zone(zindex).name = "Zone {}".format(z_num)
        print("Renamed to 'Zone {}'. \n".format(z_num))

    # This section copies zone one and renames for the corresponding interpolation zone
    solution_time = 1
    t1 = time.time()

    for i in index_zones:
        base_zone = dataset.zone('Zone 1')
        copied_zone = base_zone.copy(share_variables=False)
        copied_zone.name = "Copied - Zone {}".format(i)
        print('Successfully copied Zone {}.'.format(i))
        t2 = time.time()
        tp.data.operate.interpolate_inverse_distance(destination_zone=dataset.zone("Copied - Zone {}".format(i)),
                                                     source_zones=dataset.zone("Zone {}".format(i)))
        elapsed2 = time.time() - t2
        print('Successfully interpolated Zone {} in {} seconds.'.format(i,elapsed2))
        dataset.zone("Copied - Zone {}".format(i)).solution_time = solution_time
        print("Modified Zone {} solution time to {}s. \n".format(i, solution_time))
        solution_time = solution_time+0.0042857

    elapsed1 = time.time() - t1
    print('Total interpolation time: {} seconds \n'.format(elapsed1))

    # Removing original data
    for i in index_zones:
        dataset.delete_zones(dataset.zone("Zone {}".format(i)))

    # Averaging data over time strand
    # Creates new dataset
    in_strand = 1
    zones_by_strand = tputils.get_zones_by_strand(dataset)
    variables_to_average = [dataset.variable("Magnitude Velocity"),
                            dataset.variable("X Component Velocity"),
                            dataset.variable("Y Component Velocity"),
                            dataset.variable("Z Component Velocity"),
                            dataset.variable("Turbulent Kinetic Energy"),
                            dataset.variable("strain-rate-mag"),
                            dataset.variable("sbes-shielding-function"),
                            dataset.variable("turb-diss-rate-rans"),
                            dataset.variable("turb-diss-rate-sgs-cff"),
                            dataset.variable("Eddy Viscosity"),
                            dataset.variable("Turbulent Energy Dissipation"),
                            dataset.variable("turb-diss-rate-resolved")
                            ]
    constant_variables = [dataset.variable("CoordinateX"),
                          dataset.variable("CoordinateY"),
                          dataset.variable("CoordinateZ"),
                          # dataset.variable("X Component Position"),
                          # dataset.variable("Y Component Position"),
                          # dataset.variable("Z Component Position"),
                          dataset.variable("cell-volume"),
                          dataset.variable("dz-velocity-dx"),
                          dataset.variable("dy-velocity-dx"),
                          dataset.variable("dx-velocity-dx"),
                          dataset.variable("dz-velocity-dy"),
                          dataset.variable("dy-velocity-dy"),
                          dataset.variable("dx-velocity-dy")
                          ]
    strand_to_average = int(in_strand)
    source_zones = zones_by_strand[strand_to_average]
    print('Data averaging initializing \n')
    tpmath.compute_average(source_zones, variables_to_average, constant_variables)
    print('Data averaging complete \n')

    # Loading experimental data df
    exp_df = experimental_df_loader("C1_Experimental")
    exp_d2 = experimental_df_loader("C4_Experimental")
    exp_d3 = experimental_df_loader("C1_Experimental")

    # Appending active case with Quadrant & Diffuser data and saving out data as ascii
    for i in enumerate(exp_df):
        # print(i[0], i[1])
        # Reflecting axis from experimental to reflect model
        if i[1] == "Q1":
            exp_df[i[1]]['y-coord'] = -1 * exp_df[i[1]]['y-coord']

        elif i[1] == "Q2":
            exp_df[i[1]]['x-coord'] = -1 * exp_df[i[1]]['x-coord']

        append_interpolation_xy_points(exp_df[i[1]], i[1])
        t3 = time.time()
        print('Appended {} experimental data points for interpolation.'.format(i[1]))
        tp.data.operate.interpolate_inverse_distance(destination_zone=dataset.zone(i[1]),
                                                     source_zones=dataset.zone('Time Average - {}'.format(in_strand)))
        elapsed3 = time.time() - t3
        print('Successfully interpolated Zone {} in {} seconds.\n'.format(i[1], elapsed3))



#TODO compute new variable fluctuating velocity components for TKE, resolved TKE, %TKE
# https://www.youtube.com/watch?v=QKDFTCUh7zU&ab_channel=FluidMechanics101

#TODO save ascii file


### Equations for Tecplot Post Pro
# tpmath.compute_average(source_zones, variables_to_average, constant_variables)
# - all zones compute radius
# {radius} = sqrt({CoordinateX}**2+{CoordinateY}**2)
#
#
# - Compute for only exported data files datasets
# {u'} = {X Component Velocity} - {X Component Velocity}[7]
# {v'} = {Y Component Velocity} - {Y Component Velocity}[7]
# {w'} = {Z Component Velocity} - {Z Component Velocity}[7]
#
# {u'^2} = {u'}*{u'}
# {v'^2} = {v'}*{v'}
# {w'^2} = {w'}*{w'}
# -then time average, creates second time average zone last in index; for zones n, zone[n]
#
# - Compute for first time average zone n-1; zone[n-1]
# {TKE_resolved} = 0.5*({u'^2}[n]+{v'^2}[n]+{w'^2}[n]) <- Whichever is the last element in
# - Select only first time average zone n-1
# {Total_TKE} = {TKE_resolved}*(1-{sbes-shielding-function}) +  {Turbulent Kinetic Energy}
# {percent_TKE} = ({TKE_resolved}*(1-{sbes-shielding-function}))/{Total_TKE}
# {Total_Dissipation} = {Turbulent Energy Dissipation} +  {turb-diss-rate-resolved}*(1-{sbes-shielding-function})
# {percent_Dissipation} =  ({turb-diss-rate-resolved}*(1-{sbes-shielding-function})) /{Total_Dissipation}
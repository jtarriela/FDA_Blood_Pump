import numpy as np
import tecplot as tp
import pandas as pd
import time
from tecplot.constant import *
from postpro.TecPlot.python import tputils
from postpro.TecPlot.python import tpmath

# Purpose of this script is to interpolate results from each file onto a single mesh for averaging
# Additionally, the script takes experimental datapoints and interpolates from calculated mean data


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
        print('Interpolating to new Zone...')
        tp.data.operate.interpolate_inverse_distance(destination_zone=dataset.zone("Copied - Zone {}".format(i)),
                                                     source_zones=dataset.zone("Zone {}".format(i)))
        elapsed2 = time.time() - t2
        print('Successfully interpolated Zone {} in {} seconds.'.format(i,elapsed2))
        dataset.zone("Copied - Zone {}".format(i)).solution_time = solution_time
        print("Modified Zone {} solution time to {}s. \n".format(i, solution_time))

    elapsed1 = time.time() - t1
    print('Total interpolation time: {} seconds \n'.format(elapsed1))

    # Removing original data
    for i in index_zones:
        dataset.delete_zones(dataset.zone("Zone {}".format(i)))

    # Averaging data over time strand
    # Creates new dataset
    in_strand = 1
    zones_by_strand = tputils.get_zones_by_strand(dataset)
    variables_to_average = [dataset.variable("udm-0"),
                            dataset.variable("udm-1"),
                            dataset.variable("udm-2"),
                            dataset.variable("udm-3"),
                            dataset.variable("udm-4"),
                            dataset.variable("udm-5"),
                            dataset.variable("udm-6"),
                            dataset.variable("udm-7"),
                            dataset.variable("udm-8"),
                            dataset.variable("udm-9"),
                            dataset.variable("udm-10"),
                            dataset.variable("expr:vol_udm0"),
                            dataset.variable("expr:vol_udm1"),
                            dataset.variable("expr:vol_udm2"),
                            dataset.variable("expr:vol_udm3"),
                            dataset.variable("expr:vol_udm4"),
                            dataset.variable("expr:vol_udm5"),
                            dataset.variable("expr:vol_udm6"),
                            dataset.variable("expr:vol_udm7"),
                            dataset.variable("expr:vol_udm8"),
                            dataset.variable("expr:vol_udm9"),
                            dataset.variable("expr:vol_udm10")
                            ]
    constant_variables = [dataset.variable("CoordinateX"),
                          dataset.variable("CoordinateY"),
                          dataset.variable("CoordinateZ")]
    strand_to_average = int(in_strand)
    source_zones = zones_by_strand[strand_to_average]
    print('Data averaging initializing \n')
    tpmath.compute_average(source_zones, variables_to_average, constant_variables)
    print('Data averaging complete \n')

    # Rename first Time average zone
    dataset.zone(dataset.num_zones - 1).name = "Zone: TA-1"

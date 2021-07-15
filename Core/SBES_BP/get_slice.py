import tecplot as tp
import logging
logging.basicConfig(level=logging.DEBUG)
import functools
tp.session.connect(host='localhost', port=7600, timeout=10, quiet=False)

### Load dataset here ###
###                   ###

file_list = [r"C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\cas_data\SBES_BP_24M_Flow_SS-1-06000.cas.h5",
             r"C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\cas_data\SBES_BP_24M_Flow_SS-1-06000.dat.h5"]

dataset = tp.data.load_fluent_cff(file_list,
                           frame=None,
                           read_data_option= 0,
                           reset_style=None,
                           initial_plot_type=None)


var_remove = dataset.variable_names
var_keep = ['X', 'Y', 'Z', 'Density', 'Static Pressure', 'X Velocity', 'Y Velocity', 'Z Velocity', 'Turbulent Viscosity']
zone_remove = dataset.zone_names
zone_keep = ['volute', 'rotor']

for var in enumerate(var_keep):
  var_remove = list(filter((var[1]).__ne__, var_remove))
for var in enumerate(zone_keep):
  zone_remove = list(filter((var[1]).__ne__, zone_remove))


with tp.session.suspend():
  for var in enumerate(zone_remove):
    to_remove = var[1]
    dataset.delete_zones(dataset.zone(var[1]))

  for var in enumerate(var_remove):
    # to_remove = var[1]
    dataset.delete_variables(dataset.variable(var[1]))

tp.macro.execute_command(r'''
#!MC 1410
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'SetFieldVariables ConvectionVarsAreMomentum=\'F\' UVarNum=7 VVarNum=8 WVarNum=9 ID1=\'Pressure\' Variable1=6 ID2=\'Density\' Variable2=4'
$!ExtendedCommand 
  CommandProcessorID = 'CFDAnalyzer4'
  Command = 'Calculate Function=\'CELLVOLUME\' Normalization=\'None\' ValueLocation=\'Nodal\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''
''')

tp.data.operate.execute_equation('{radius} = sqrt(X**2 + Y**2)\n'
                              '{inst_Vmag} = sqrt({X Velocity}**2+{Y Velocity}**2 +{Z Velocity}**2)\n'
                                 '{cell_length} = abs({Cell Volume})**(1/3)',
                              zones = None)

print(dataset.variable_names)

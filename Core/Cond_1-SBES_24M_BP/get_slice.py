import tecplot as tp
import functools
from tecplot.constant import PlotType, SliceSource
from os import path
import logging
logging.basicConfig(level=logging.DEBUG)

class dataset_parsing():
    def __init__(self, file_list):
        self.file_list = file_list
        self.dataset = tp.data.load_fluent_cff(file_list,
                                               frame=None,
                                               read_data_option=0,
                                               reset_style=None,
                                               initial_plot_type=None)
    def data_slice(self):

        var_remove = self.dataset.variable_names
        var_keep = ['X', 'Y', 'Z', 'Density', 'Static Pressure', 'X Velocity', 'Y Velocity', 'Z Velocity', 'Turbulent Viscosity']
        zone_remove = self.dataset.zone_names
        zone_keep = ['volute', 'rotor']

        for var in enumerate(var_keep):
            var_remove = list(filter((var[1]).__ne__, var_remove))
        for var in enumerate(zone_keep):
            zone_remove = list(filter((var[1]).__ne__, zone_remove))


        with tp.session.suspend():
            for var in enumerate(zone_remove):
                self.dataset.delete_zones(self.dataset.zone(var[1]))
            for var in enumerate(var_remove):
                self.dataset.delete_variables(self.dataset.variable(var[1]))

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
                                         '{cell_length} = abs({Cell Volume})**(1/3)')

        with tp.session.suspend():

            # if copy_cell_centers is False, values stored at nodes interpolated at center
            # if true, stores values at cell center if slice passes through the center
            blade_passage_slice = tp.data.extract.extract_slice(origin = (0, 0, 0.006562),
                                                      normal = (0 ,0, 1),
                                                      mode = 0, #ExtractMode.SingleZone
                                                      zones = None,
                                                      copy_cell_centers = False)
            #rename slice zone macro
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 3
              NAME = "blade_passage_plane"
            ''')

            # blade_passage_slice = tp.data.extract


            quad_1_xpoints = tp.data.extract.extract_line(points = [(0, 0, 0.006562), (0.0214, -0.0214, 0.006562)],
                                                        num_points = 150)

            #rename extracted points zone macro
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 4
              NAME = "quadrant_1"
            ''')
            quad_2_xpoints = tp.data.extract.extract_line(points = [(0, 0, 0.006562), (-0.0214, -0.0214, 0.006562)],
                                                        num_points = 150)
            #rename extracted points zone macro
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 5
              NAME = "quadrant_2"
            ''')
            diffuser_1_xpoints = tp.data.extract.extract_line(points = [(0.02, 0.-0.02581, 0.006562), (0.02, -0.02986, 0.006562)],
                                                            num_points = 150)
            #rename extracted points zone
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 6
              NAME = "diffuser_1"
            ''')

            diffuser_2_xpoints = tp.data.extract.extract_line(points = [(0.025, -0.02476, 0.006562), (0.025, -0.03061, 0.006562)],
                                                            num_points = 150)
            #rename extracted points zone
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 7
              NAME = "diffuser_2"
            ''')

            diffuser_3_xpoints = tp.data.extract.extract_line(points = [(0.03, -0.006562, 0.006562), (0.03, -0.03151, 0.006562)],
                                                            num_points = 150)
            # rename extracted points zone
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 8
              NAME = "diffuser_3"
            ''')

            diffuser_4_xpoints = tp.data.extract.extract_line(points = [(0.035, -0.02296, 0.006562), (0.035, -0.03241, 0.006562)],
                                                            num_points = 150)
            # rename extracted points zone
            tp.macro.execute_command(r'''
            #!MC 1410
            $!RENAMEDATASETZONE 
              ZONE = 9
              NAME = "diffuser_4"
            ''')

            self.dataset.delete_variables(self.dataset.variable("Cell Volume"))
            self.dataset.delete_zones(self.dataset.zone('rotor'))
            self.dataset.delete_zones(self.dataset.zone('volute'))

            # save szl, take original input string name and save out -- where does it save -- or append
            # tp.data.save_tecplot_szl('6000.szplt')
            # tp.data.save_tecplot_plt()



    def save_slice(self):
        tp.data.save_tecplot_plt(self.file_list[1] + '.plt',
                             dataset=self.dataset,
                             variables=None,
                             zones=None,
                             include_geom=False,
                             include_data_share_linkage=True)
    def new_layout(self):
        tp.new_layout()

#######################################################



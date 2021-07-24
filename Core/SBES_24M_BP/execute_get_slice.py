import tecplot as tp
import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from get_slice import dataset_parsing
import functools
from tecplot.constant import PlotType, SliceSource
from os import path
tp.session.connect(host='localhost', port=7600, timeout=10, quiet=False)



# file_list = [r"C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\cas_data\SBES_BP_24M_Flow_SS-1-06000.cas.h5",
#              r"C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\cas_data\SBES_BP_24M_Flow_SS-1-06000.dat.h5"]


file_path = r'C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\cas_data'
import glob, os
os.chdir(file_path)
cas_files=[]
dat_files=[]
for file in glob.glob("*.cas.h5"):
    # print(file)
    cas_files.append(file_path + '\\' + file)
for file in glob.glob("*.dat.h5"):
    # print(file)
    dat_files.append(file_path + '\\' + file)
#
# cas_files = [r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-06000.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-06600.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-07200.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-07800.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-08400.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-09000.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-09600.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-10200.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-10800.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-11400.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-12000.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-12600.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-13200.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-13800.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-14400.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-15000.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-16200.cas.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_data\SBES_BP_24M_Flow_SS-1-16800.cas.h5']
# dat_files = [r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-06000.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-06600.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-07200.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-07800.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-08400.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-09000.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-09600.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-10200.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-10800.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-11400.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-12000.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-12600.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-13200.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-13800.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-14400.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-15000.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-16200.dat.h5',
#              r'C:\\Users\\Joseph Tarriela\\OneDrive - University of South Florida\\Projects\\Active\\Wenbin Mao\\FDA Round Robin\\Data & Instruction\\Model & Results.txt\\Hemolysis Fluent Models\\SBES\\24\\cas_dataSBES_BP_24M_Flow_SS-1-16800.dat.h5']

file_list = []
for i in enumerate(cas_files):
    file_list = [cas_files[i[0]], dat_files[i[0]]]
    pytec_dataset = dataset_parsing(file_list)
    pytec_dataset.data_slice()
    pytec_dataset.save_slice()
    pytec_dataset.new_layout()


import logging
logging.basicConfig(level=logging.DEBUG)

import tecplot as tp

# Run this script with "-c" to connect to Tecplot 360 on port 7600
# To enable connections in Tecplot 360, click on:
#   "Scripting" -> "PyTecplot Connections..." -> "Accept connections"
import sys
if '-c' in sys.argv:
    tp.session.connect(host='localhost', port=7600, timeout=10, quiet=False)

try:
    conected_bool = tp.session.connected(timeout=5)
    if conected_bool == True:
        print("Connected to Tecplot GUI")
        pass
    else:
        print("Not connected")
except:
  print("An exception occurred")


fluent_file_list = [r"C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\SBES_BP_24M_Flow_SS-1-06000.cas.h5",
                    r"C:\Users\Joseph Tarriela\OneDrive - University of South Florida\Projects\Active\Wenbin Mao\FDA Round Robin\Data & Instruction\Model & Results.txt\Hemolysis Fluent Models\SBES\24\SBES_BP_24M_Flow_SS-1-06000.dat.h5"]


tp.new_layout()
tp.data.load_fluent_cff(filenames =fluent_file_list, read_data_option=tp.constant.ReadDataOption.Replace)


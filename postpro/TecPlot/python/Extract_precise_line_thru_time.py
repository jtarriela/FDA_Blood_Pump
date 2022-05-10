import numpy as np
import tecplot as tp
import pandas as pd
import time
from tecplot.constant import *
from postpro.TecPlot.python import tputils
from postpro.TecPlot.python import tpmath



tp.session.connect()
frame = tp.active_frame()
with tp.session.suspend():
    dataset = frame.dataset
    index_zones = []

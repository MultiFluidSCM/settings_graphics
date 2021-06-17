'''
Script for creating graphics which make it easy to compare the single column model (SCM)
settings with those diagnosed from large eddy simulations (LESs)
'''

#Core Python modules
import os
import sys
import time
import numpy as np

#User-made modules
from src.objects.path_setup import path_setup
from src.plots.plot_graphic import plot_graphic

def make_graphics(id_scm="default"):
    
    folder = path_setup(__file__)
    
    folder_scm = os.path.join(folder.data_scm, id_scm)
    
    print("\nReading data")
    dummy_id = "test"
    dummy_variable = "$b_w$"
    dummy_settings_scm = 0.8
    dummy_settings_les = np.array([0.4, 0.9])
    
    print("\nProcessing data")
    
    print("\nCreating graphics")
    plot_graphic(dummy_id, dummy_variable, dummy_settings_scm, dummy_settings_les, folder=folder.outputs)
    
    
    
    
if __name__ == "__main__":
    timeInit = time.time()
    
    make_graphics()
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
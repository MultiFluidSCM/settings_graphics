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
from src.plots.plot_transfer_graphic import plot_all_transfer_graphics
from src.utilities.filter import filter_transfer_coefficients
from src.utilities.diagnose_b import diagnose_and_filter_b_all_times
from src.utilities.read_les import read_all_times
from src.utilities.read_scm import read_transfer_properties

def make_graphics(id_scm="default", greyscale=False):
    
    print(f"\n\nCreating graphics for {id_scm}")
    
    folder = path_setup(__file__)
    
    folder_scm_settings = os.path.join(folder.data_scm, id_scm, "settings", "transfer_properties")
    
    print("\nReading data")
    les_data = read_all_times(folder.data_les)
    scm_settings = read_transfer_properties(folder_scm_settings)
    
    print("\nProcessing data")
    scm_settings_transfers = filter_transfer_coefficients(scm_settings)
    les_data_b = diagnose_and_filter_b_all_times(les_data)
    
    print("\nCreating graphics")
    plot_all_transfer_graphics(
        scm_settings_transfers, 
        les_data_b, 
        folder = os.path.join(folder.outputs, id_scm), 
        title = id_scm,
        greyscale = greyscale
    )
    
    
    
    
if __name__ == "__main__":
    timeInit = time.time()
    
    id_scm = "default_simulation_version_1"
    
    make_graphics(id_scm=id_scm, greyscale=True)
    make_graphics(id_scm=id_scm, greyscale=False)
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
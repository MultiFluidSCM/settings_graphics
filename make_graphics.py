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
from src.utilities.diagnose_b import diagnose_and_filter_b
from src.utilities.read_les import read_all_fields
from src.utilities.read_scm import read_transfer_properties

def make_graphics(id_scm="default"):
    
    folder = path_setup(__file__)
    
    folder_scm_settings = os.path.join(folder.data_scm, id_scm, "settings", "transfer_properties")
    
    print("\nReading data")
    dummy_id = "test"
    dummy_variable = "$b_w$"
    dummy_settings_scm = 0.8
    dummy_settings_les = np.array([0.4, 0.9])
    
    data_les = read_all_fields(folder.data_les)
    settings = read_transfer_properties(folder_scm_settings)
    
    print("\nProcessing data")
    settings_transfers = filter_transfer_coefficients(settings)
    data_les_b = diagnose_and_filter_b(data_les)
    
    print("\nCreating graphics")
    # plot_transfer_graphic(dummy_id, dummy_variable, dummy_settings_scm, dummy_settings_les, folder=folder.outputs)
    plot_all_transfer_graphics(settings_transfers, data_les_b, folder=os.path.join(folder.outputs, id_scm))
    
    
    
    
if __name__ == "__main__":
    timeInit = time.time()
    
    id_scm = "default_simulation_version2"
    
    make_graphics(id_scm=id_scm)
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
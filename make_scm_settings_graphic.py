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
from src.utilities.read_les import read_les
from src.utilities.read_scm import read_transfer_properties
from src.utilities.time_elapsed import time_elapsed

@time_elapsed
def make_scm_graphic(id_scm="default", greyscale=False):
    '''
    Read in the tunable parameters for the single column model (SCM) version and display them
    relative to what the values should be according to diagnosed high-resolution data (LES).
    
    :param id_scm: The folder name/id containing the SCM settings files, str.
    :param greyscale: Select whether the graphics should be in color or grey, bool.
    :return: Dictionary of SCM settings and LES data, dict dict.
    '''
    print(f"\n\nCreating graphics for {id_scm}")
    folder = path_setup(__file__)
    folder_scm_settings = os.path.join(folder.data_scm, id_scm, "settings", "transfer_properties")
    
    print("\nReading data")
    les_data = read_les(folder.data_les)
    scm_settings = read_transfer_properties(folder_scm_settings)
    
    print("\nProcessing, cleaning and preparing data")
    scm_settings_transfers = filter_transfer_coefficients(scm_settings)
    les_data_b = diagnose_and_filter_b(les_data)
    
    print("\nCreating graphics")
    plot_all_transfer_graphics(
        scm_settings_transfers, 
        les_data_b, 
        folder    = os.path.join(folder.outputs, id_scm), 
        title     = id_scm,
        greyscale = greyscale
    )
    
    return scm_settings_transfers, les_data_b
    
    
    
    
if __name__ == "__main__":
    id_scm = "default_simulation_version_0"
    
    make_scm_graphic(id_scm=id_scm, greyscale=True)
    make_scm_graphic(id_scm=id_scm, greyscale=False)
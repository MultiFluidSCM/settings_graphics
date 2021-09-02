'''
Script for comparing the model (SCM) settings from one test case with the settings from 
another test case.
'''

#Core Python modules
import os
import sys
import time
import numpy as np

#User-made modules
from make_scm_settings_graphic import make_scm_graphic
from src.objects.path_setup import path_setup
from src.plots.plot_transfer_graphic import plot_all_transfer_graphics
from src.utilities.filter import filter_transfer_coefficients
from src.utilities.diagnose_b import diagnose_and_filter_b
from src.utilities.read_les import read_les
from src.utilities.read_scm import read_transfer_properties
from src.utilities.time_elapsed import time_elapsed

@time_elapsed
def compare_scm_settings(id_scm1="default", id_scm2="default", greyscale=False):
    '''
    Read in the tunable parameters for two single column model (SCM) versions and display them
    relative to each other, as well as the diagnosed high-resolution data (LES).
    
    :param id_scm1: The folder name/id containing the SCM settings files, str.
    :param id_scm2: The folder name/id containing the SCM settings files you are comparing to, str.
    :param greyscale: Select whether the graphics should be in color or grey, bool.
    :return: Dictionary of SCM settings and LES data, dict dict.
    '''
    print(f"\n\nCreating graphics for {id_scm1} vs {id_scm2}")
    folder = path_setup(__file__)
    
    scm_settings1, les_data1 = make_scm_graphic(id_scm=id_scm1, greyscale=greyscale)
    scm_settings2, les_data2 = make_scm_graphic(id_scm=id_scm2, greyscale=greyscale)
    
    print("\nCreating graphics")
    plot_all_transfer_graphics(
        scm_settings1, 
        les_data1, 
        settings_scm_old = scm_settings2,
        folder           = os.path.join(folder.outputs, f"{id_scm1}_vs_{id_scm2}"), 
        title            = id_scm1,
        greyscale        = greyscale
    )
    
    return scm_settings1, scm_settings2, les_data1
    
    
    
if __name__ == "__main__":
    id_scm = [
        "default_simulation_version_0",
        # "default_simulation_version_1",
        # "default_simulation_version_2",
        # "default_simulation_version_2p1p1",
        # "default_simulation_version_2p1p8",
        "default_simulation_version_3",
    ]
    
    for i in range(len(id_scm)-1):
        id_scm1 = id_scm[i+1]
        id_scm2 = id_scm[i]
        
        compare_scm_settings(id_scm1=id_scm1, id_scm2=id_scm2)
        compare_scm_settings(id_scm1=id_scm1, id_scm2=id_scm2, greyscale=True)
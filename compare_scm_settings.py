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
from src.objects.path_setup import path_setup
from src.plots.plot_transfer_graphic import plot_all_transfer_graphics
from src.utilities.filter import filter_transfer_coefficients
from src.utilities.diagnose_b import diagnose_and_filter_b_all_times
from src.utilities.read_les import read_all_times
from src.utilities.read_scm import read_transfer_properties

def make_graphics(id_scm1="default", id_scm2="default", greyscale=False):
    
    print(f"\n\nCreating graphics for {id_scm1} vs {id_scm2}")
    
    folder = path_setup(__file__)
    
    folder_scm_settings1 = os.path.join(folder.data_scm, id_scm1, "settings", "transfer_properties")
    folder_scm_settings2 = os.path.join(folder.data_scm, id_scm2, "settings", "transfer_properties")
    
    print("\nReading data")
    les_data = read_all_times(folder.data_les)
    scm_settings1 = read_transfer_properties(folder_scm_settings1)
    scm_settings2 = read_transfer_properties(folder_scm_settings2)
    
    print("\nProcessing data")
    scm_settings_transfers1 = filter_transfer_coefficients(scm_settings1)
    scm_settings_transfers2 = filter_transfer_coefficients(scm_settings2)
    les_data_b = diagnose_and_filter_b_all_times(les_data)
    
    print("\nCreating graphics")
    plot_all_transfer_graphics(
        scm_settings_transfers1, 
        les_data_b, 
        settings_scm_old = scm_settings_transfers2,
        folder = os.path.join(folder.outputs, f"{id_scm1}_vs_{id_scm2}"), 
        title = id_scm1,
        greyscale = greyscale
    )
    
    
    
    
if __name__ == "__main__":
    timeInit = time.time()
    
    
    id_scm = [
        "default_simulation_version_0",
        # "default_simulation_version_1",
        # "default_simulation_version_2",
        # "default_simulation_version_2p1p1",
        # "default_simulation_version_2p1p1_GD",
        # "default_simulation_version_2p1p2",
        # "default_simulation_version_2p1p3",
        # "default_simulation_version_2p1p4",
        # "default_simulation_version_2p1p5",
        # "default_simulation_version_2p1p6",
        # "default_simulation_version_2p1p7",
        # "default_simulation_version_2p1p8",
        # "default_simulation_version_2p2",
        # "default_simulation_version_2p2p1",
        # "default_simulation_version_2p2p2",
        # "default_simulation_version_2p2p3",
        # "default_simulation_version_2p2p4",
        "default_simulation_version_3",
    ]
    
    for i in range(len(id_scm)-1):
        id_scm1 = id_scm[i+1]
        id_scm2 = id_scm[i]
        
        make_graphics(id_scm1=id_scm1, id_scm2=id_scm2)
        make_graphics(id_scm1=id_scm1, id_scm2=id_scm2, greyscale=True)
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
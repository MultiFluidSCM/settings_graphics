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
from src.utilities.make_gif import make_gif_from_list
from src.utilities.read_les import read_all_fields
from src.utilities.read_scm import read_transfer_properties

def make_graphics(folder, id_scm="default", id_les="time_32000", greyscale=False):
    
    print(f"\n\nCreating graphics for {id_les}, {id_scm}")
    
    folder_les_data = os.path.join(folder.data_les, id_les)
    folder_scm_settings = os.path.join(folder.data_scm, id_scm, "settings", "transfer_properties")
    
    print("\nReading data")
    les_data = read_all_fields(folder_les_data)
    scm_settings = read_transfer_properties(folder_scm_settings)
    
    print("\nProcessing data")
    scm_settings_transfers = filter_transfer_coefficients(scm_settings)
    les_data_b = diagnose_and_filter_b(les_data)
    
    print("\nCreating graphics")
    plot_all_transfer_graphics(
        scm_settings_transfers, 
        les_data_b, 
        folder = os.path.join(folder.outputs, id_les), 
        title = id_les,
        greyscale = greyscale
    )
    
    
    
    
if __name__ == "__main__":
    timeInit = time.time()
    
    folder = path_setup(__file__)
    
    id_scm = "default_simulation_version_2"
    greyscale = True
    
    images_h = []
    images_v = []
    for i in range(18200, 38000, 600):
        id_les = f"time_{i}"
        make_graphics(folder, id_scm=id_scm, id_les=id_les, greyscale=greyscale)
        
        images_h.append(os.path.join(folder.outputs, id_les, "automatic", "settings_horizontal_title.png"))
        images_v.append(os.path.join(folder.outputs, id_les, "automatic", "settings_vertical_title.png"))
    
    make_gif_from_list(images_h, os.path.join(folder.outputs, "settings_horizontal_title.gif"), duration=500, loop=1)
    make_gif_from_list(images_v, os.path.join(folder.outputs, "settings_vertical_title.gif"),   duration=500, loop=1)
    
    timeElapsed = time.time() - timeInit
    print(f"Elapsed time: {timeElapsed:.2f}s")
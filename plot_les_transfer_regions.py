#Core Python modules
import os
import sys
import time
import numpy as np

#User-made modules
from src.objects.path_setup import path_setup
from src.plots.plot_les_transfer_regions import plot_les_transfer_regions
from src.utilities.diagnose_b import diagnose_and_filter_b
from src.utilities.read_les import read_les
from src.utilities.time_elapsed import time_elapsed

@time_elapsed
def plot_les_regions(id_scm="default", greyscale=False):
    '''
    Plot the regions of the LES data where different transfer phenomena are classified.
    
    :param greyscale: Select whether the graphics should be in color or grey, bool.
    :return: Dictionary of LES data, dict.
    '''
    print(f"\n\nCreating graphics for {id_scm}")
    folder = path_setup(__file__)
    
    print("\nReading data")
    les_data = read_les(folder.data_les)
    
    print("\nProcessing, cleaning and preparing data")
    les_data = diagnose_and_filter_b(les_data)
    
    print("\nCreating graphics")
    for transfer in ["plumeEdge", "particles"]:
        plot_les_transfer_regions(
            les_data[transfer], 
            folder    = folder.outputs, 
            id        = transfer,
            greyscale = greyscale
        )
    
    return les_data
    
    
    
    
if __name__ == "__main__":
    plot_les_regions()
    plot_les_regions(greyscale=True)
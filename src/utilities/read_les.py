import os
import sys
from scipy.io import loadmat
from .check_folder import get_folders_in_folder

def read_les(folder_data):
    '''
    Import all of the LES vertical profiles of the 2 fluids
    '''
    folders = ["plume", "plumeEdge", "particles"]
    
    data = {}
    
    for folder in folders:
        
        file = os.path.join(folder_data, folder, f"profiles.mat")
        
        if os.path.isfile(file):
            data[folder] = loadmat(file)
    
    return data


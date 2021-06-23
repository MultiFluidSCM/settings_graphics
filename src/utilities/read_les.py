import os
import sys
from scipy.io import loadmat
from .check_folder import get_folders_in_folder

def read_all_times(folder_les):
    folders = get_folders_in_folder(folder_les)
    
    data = {}
    for folder in folders:
        print(f"Reading LES data from {folder}")
        data[os.path.basename(folder)] = read_all_fields(folder)
    
    return data

def read_all_fields(folder_data):
    '''
    Import all of the LES vertical profiles of the 2 fluids
    '''
    folders = ["plume", "plumeEdge", "particles"]
    
    data = {}
    
    for folder in folders:
        
        dir = os.path.join(folder_data, "profilesMean", folder)
        if os.path.isdir(dir):
            data[folder] = read_fields(dir)
    
    return data

def read_fields(folder):
    '''
    Import LES vertical profiles
    '''
    fields = ["u", "v", "w", "qv", "ql", "theta"]
    
    data = {}
    
    for field in fields:
        file = os.path.join(folder, f"z_{field}.mat")
        
        if os.path.isfile(file):
            data[field] = loadmat(file)
            
            for subfield in data[field]:
                # Flatten the data if it is a data type that can be flattened:
                try:
                    data[field][subfield] = data[field][subfield].flatten()
                except:
                    data[field][subfield] = data[field][subfield]
    
    return data


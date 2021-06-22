import os
import sys
from scipy.io import loadmat

def read_all_fields(folder_data):
    '''
    Import all of the LES vertical profiles of the 2 fluids
    '''
    folders = ["mean_fields", "plume_edge"]
    
    data = {}
    
    for folder in folders:
        
        if os.path.isdir(os.path.join(folder_data, folder)):
            data[folder] = read_fields(os.path.join(folder_data, folder))
    
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
    
    return data


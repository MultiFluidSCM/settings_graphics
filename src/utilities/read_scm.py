import os
import sys

from .check_folder import get_files_in_folder

def read_transfer_properties(folder):
    '''
    Cycle through the settings files and read the settings into a python dictionary
    '''
    transfers = ["dwdz", "instability", "mixing", "mixing_cloud"]
    
    settings = {}
    
    # files = get_files_in_folder(folder, extension=".m")
    
    for transfer in transfers:
        file = os.path.join(folder, f"set_transfer_properties_{transfer}.m")
        
        if os.path.isfile(file):
            settings[transfer] = read_settings(file)
    
    return settings

def read_settings(file):
    '''
    Read settings file and add valid settings to a dictionary
    '''
    settings = {}
    
    file_content = read_file(file)
    lines = file_content.split("\n")
    
    # Cycle through lines in document
    for line in lines:
        if "=" in line and ";" in line:
            if line[0] != "%":
                line = line.split(";")[0]
                line = line.replace(" ", "")
                line = line.replace("true", "True")
                line = line.replace("false", "False")
                
                variable = line.split("=")[0]
                value = line.split("=")[1]
                
                # Remove undesirable variable name components
                variable = variable.replace("param.", "")
                
                if is_valid(value):
                    settings[variable] = {}
                    settings[variable]["name"] = variable
                    settings[variable]["id"] = variable
                    settings[variable]["symbol"] = variable
                    settings[variable]["value"] = eval(value)
    
    return settings

def read_file(file):
    '''
    Read file and return contents
    '''
    if os.path.isfile(file):
        file_object = open(file, "r+")
        file_content = file_object.read()
        file_object.close()
        
        return file_content
    
    return ""

def is_valid(string):
    '''
    Check if string can be interpretted by python
    '''
    try:
        eval(string)
        return True
    except:
        return False
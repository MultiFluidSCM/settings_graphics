import numpy as np

def diagnose_and_filter_b(data_les):
    '''
    Calculate the b coefficients and then filter them into the different transfer regimes
    '''
    data_b = diagnose_b(data_les)
    data_b = filter_b(data_b)
    
    return data_b

def diagnose_b(data_les):
    '''
    Diagnose the b-coefficients which describe the transferred properties between fluids.
    '''
    # Different types of transfer definitions
    definitions = ["plume_edge"]
    # definitions = ["plume_edge", "particles"]
    
    # Mean fields of the fluids
    mean = data_les["mean_fields"]
    
    # Transfer coefficients will be stored here
    data_b = {}
    
    for definition in definitions:
        fields = data_les[definition]
        
        data_b[definition] = {}
        
        for field in fields:
            if field in mean:
                b12, b21 = b_coefficients(
                    mean[field]["fluid1"], 
                    mean[field]["fluid2"], 
                    fields[field]["transfer12"], 
                    fields[field]["transfer21"]
                )
                
                data_b[definition][field] = {}
                data_b[definition][field]["z"] = fields[field]["z"].flatten()
                data_b[definition][field]["b12"] = b12.flatten()
                data_b[definition][field]["b21"] = b21.flatten()
                
    return data_b

def b_coefficients(a1, a2, a12, a21):
    '''
    Calculate the b-transfer coefficients
    '''
    delta_a = a2 - a1
    delta_a += 1e-8*(delta_a == 0)
    
    b12 = (a12 - a1) / delta_a
    b21 = (a21 - a2) /-delta_a
    
    return b12, b21


def filter_b(data_b):
    for key in data_b:
        for key2 in data_b[key]:
            z = data_b[key][key2]["z"]
            break
        break
    
    filters = {
        "all": z >= 0,
        "mixing": (z >= 0.3) * (z < 1.),
        "mixing_cloud": (z >= 1.2) * (z < 2.5),
        "instability": (z < 0.5),
        "dwdz": (z > 0.5)*(z < 1.2) + (z >= 2.5)
    }
    
    data_b_filtered = {}
    for filter in filters:
        data_b_filtered[filter] = {}
        
        for definition in data_b:
            data_b_filtered[filter][definition] = {}
            fields = data_b[definition]
            
            for field in fields:
                data_b_filtered[filter][definition][field] = {}
                for subfield in fields[field]:
                    data_b_filtered[filter][definition][field][subfield] = fields[field][subfield].copy()
                    data_b_filtered[filter][definition][field][subfield] = \
                        fields[field][subfield].copy()[filters[filter]]
    
    return data_b_filtered
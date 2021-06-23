import numpy as np

def diagnose_and_filter_b_all_times(data_les):
    data_b = {}
    
    for time in data_les:
        print(f"\nProcessing {time}")
        data_b_time = diagnose_and_filter_b(data_les[time])
        
        # Add data from each time to global data set
        for filter in data_b_time:
            if filter not in data_b:
                data_b[filter] = {}
            
            for definition in data_b_time[filter]:
                if definition not in data_b[filter]:
                    data_b[filter][definition] = {}
                
                for field in data_b_time[filter][definition]:
                    if field not in data_b[filter][definition]:
                        data_b[filter][definition][field] = {}
                    
                    for subfield in data_b_time[filter][definition][field]:
                        if subfield not in data_b[filter][definition][field]:
                            data_b[filter][definition][field][subfield] = np.array([])
                        
                        # Merge the data sets
                        data_1 = data_b[filter][definition][field][subfield]
                        data_2 = data_b_time[filter][definition][field][subfield]
                        data_b[filter][definition][field][subfield] = np.concatenate((data_1,data_2))
    
    return data_b

def diagnose_and_filter_b(data_les):
    '''
    Calculate the b coefficients and then filter them into the different transfer regimes
    '''
    data_b = diagnose_b(data_les)
    data_b = filter_b(data_les, data_b)
    
    return data_b

def diagnose_b(data_les):
    '''
    Diagnose the b-coefficients which describe the transferred properties between fluids.
    '''
    # Different types of transfer definitions
    # definitions = ["plumeEdge"]
    definitions = ["plumeEdge", "particles"]
    
    # Mean fields of the fluids
    mean_fields = {}
    if "plume" in data_les:
        mean_fields = data_les["plume"]
    
    # Transfer coefficients will be stored here
    data_b = {}
    
    for definition in definitions:
        
        if definition in data_les:
            fields = data_les[definition]
            
            data_b[definition] = {}
            
            for field in fields:
                if field in mean_fields:
                    b12, b21 = b_coefficients(
                        mean_fields[field]["fluid1"], 
                        mean_fields[field]["fluid2"], 
                        fields[field]["transfer12"], 
                        fields[field]["transfer21"]
                    )
                    
                    data_b[definition][field] = {}
                    data_b[definition][field]["z"] = fields[field]["z"]
                    data_b[definition][field]["b12"] = b12
                    data_b[definition][field]["b21"] = b21
                elif "fluid1" in fields[field]:
                    b12, b21 = b_coefficients(
                        fields[field]["fluid1"], 
                        fields[field]["fluid2"], 
                        fields[field]["transfer12"], 
                        fields[field]["transfer21"]
                    )
                    
                    data_b[definition][field] = {}
                    data_b[definition][field]["z"] = fields[field]["z"]
                    data_b[definition][field]["b12"] = b12
                    data_b[definition][field]["b21"] = b21
                
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


def filter_b(data_les, data_b):
    
    # Extract liquid water data and find cloud base and cloud height
    if "plume" in data_les:
        mean_fields = data_les["plume"]
        z = mean_fields["ql"]["z"]
        ql = mean_fields["ql"]["fluid2"]
        z_cloud = z[ql > 1e-5]
        
        # If no cloud detected, set last element as cloud to keep the process going
        if len(z_cloud) == 0:
            z_cloud = z[-1]
    else:
        # Default cloud base and cloud height for 9 hours into simulation
        z_cloud = np.array([1100, 2800])
    
    
    z_cloud_base = np.min(z_cloud)
    z_cloud_top  = np.max(z_cloud)
    
    # Apply some limits
    # z_cloud_base = min(z_cloud_base, 1400)
    # z_cloud_top  = min(z_cloud_top,  3400)
    
    print(f"Diagnosed cloud base: {z_cloud_base:.2f}m, Diagnosed cloud top: {z_cloud_top:.2f}m")
    
    # Create filters for where certain transfers exist (approximately) using boolean arrays
    filters = {
        "all": filter_all,
        "mixing": filter_mixing,
        "mixing_cloud": filter_mixing_cloud,
        "instability": filter_instability,
        "dwdz": filter_dwdz
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
                        fields[field][subfield].copy()[filters[filter](fields[field]["z"], z_cloud_base, z_cloud_top)]
    
    return data_b_filtered

def filter_all(z, z_cloud_base, z_cloud_top):
    return z >= 0

def filter_mixing(z, z_cloud_base, z_cloud_top):
    return (z >= 0.2*z_cloud_base) * (z < 0.8*z_cloud_base)

def filter_mixing_cloud(z, z_cloud_base, z_cloud_top):
    return (z >= z_cloud_base + 0.2*(z_cloud_top-z_cloud_base)) * (z < z_cloud_top - 0.2*(z_cloud_top-z_cloud_base))

def filter_instability(z, z_cloud_base, z_cloud_top):
    return (z < 0.5*z_cloud_base)

def filter_dwdz(z, z_cloud_base, z_cloud_top):
    return (z > 0.5*z_cloud_base)*(z < 1.2*z_cloud_base) + (z >= 2.5)
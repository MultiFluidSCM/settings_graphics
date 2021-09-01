import numpy as np

def diagnose_and_filter_b(data_les):
    '''
    Calculate the b coefficients and then filter them into the different transfer regimes
    '''
    data_b = diagnose_b(data_les)
    
    data_b_filtered = {}
    data_b_filtered["plumeEdge"] = filter_b(data_b["plume"], data_b["plumeEdge"])
    data_b_filtered["particles"] = filter_b(data_b["plume"], data_b["particles"])
    
    return data_b_filtered

def diagnose_b(data_les):
    '''
    Diagnose the b-coefficients which describe the transferred properties between fluids.
    '''
    definitions = ["plumeEdge", "particles"]
    variables = ["w", "qv", "th"]
    
    for definition in definitions:
        for variable in variables:
            
            mean_definition = definition
            if f"{variable}_1" not in data_les[mean_definition]:
                mean_definition = "plume"
            
            b12, b21 = b_coefficients(
                data_les[mean_definition][f"{variable}_1"],
                data_les[mean_definition][f"{variable}_2"],
                data_les[definition][f"{variable}_12"],
                data_les[definition][f"{variable}_21"]
            )
            
            data_les[definition][f"b{variable}_12"] = b12
            data_les[definition][f"b{variable}_21"] = b21
    
    return data_les

def b_coefficients(a1, a2, a12, a21):
    '''
    Calculate the b-transfer coefficients
    '''
    delta_a = a2 - a1
    delta_a = delta_a + 1e-8*(delta_a == 0)
    
    b12 = (a12 - a1) / delta_a
    b21 = (a21 - a2) /-delta_a
    
    return b12, b21


def filter_b(data_les_plume, data_les):
    
    variables = ["w", "qv", "th"]
    
    # Create filters for where certain transfers exist (approximately) using boolean arrays
    filters = {
        "all": filter_all,
        "mixing": filter_mixing,
        "mixing_cloud": filter_mixing_cloud,
        "instability": filter_instability,
        "dwdz": filter_dwdz
    }
    
    # Store the cloud base and top
    data_les["cloud_base"] = []
    data_les["cloud_top"] = []
    
    for time in data_les["times"][0]:
        # Find nearest time in the mean profiles data
        i = np.argmin(np.abs(data_les_plume["times"][0] - time))
        time_plume = data_les_plume["times"][0][i]
        print(f"Comparing t={time_plume:.0f}s (plume) with t={time:.0f}s")
        
        # Extract liquid water data and find cloud base and cloud height
        z = data_les_plume["z"]
        ql = data_les_plume["ql_2"][:,i]
        z_cloud = z[ql > 1e-5]
        
        # If no cloud detected, set as the approx. boundary layer height to keep the process going
        if len(z_cloud) == 0:
            z_cloud = [900]
        
        
        z_cloud_base = np.min(z_cloud)
        z_cloud_top  = np.max(z_cloud)
        
        data_les["cloud_base"].append(z_cloud_base)
        data_les["cloud_top"].append(z_cloud_top)
        
        print(f"Diagnosed cloud base: {z_cloud_base:.2f}m, Diagnosed cloud top: {z_cloud_top:.2f}m")
        
        for name, filter in filters.items():
            profile_name = f"filter_{name}"
            profile = filter(data_les["z"], z_cloud_base, z_cloud_top)
            print(profile_name)
            if profile_name not in data_les:
                data_les[profile_name] = profile.reshape((len(profile), 1))
            
            else:
                data_les[profile_name] = np.concatenate(
                    (
                        data_les[profile_name], 
                        profile.reshape((len(profile), 1))
                    ),
                    axis = -1
                )
    
    
    for filter in filters:
        
        for variable in variables:
            data_les[f"b{variable}_12_{filter}"] = data_les[f"b{variable}_12"][data_les[f"filter_{filter}"]]
            data_les[f"b{variable}_12_{filter}"] = data_les[f"b{variable}_12_{filter}"][~np.isnan(data_les[f"b{variable}_12_{filter}"])]
            
            data_les[f"b{variable}_21_{filter}"] = data_les[f"b{variable}_21"][data_les[f"filter_{filter}"]]
            data_les[f"b{variable}_21_{filter}"] = data_les[f"b{variable}_21_{filter}"][~np.isnan(data_les[f"b{variable}_21_{filter}"])]
    
    
    return data_les

def filter_all(z, z_cloud_base, z_cloud_top):
    return z >= 0

def filter_mixing(z, z_cloud_base, z_cloud_top):
    return (z >= 0.2*z_cloud_base) * (z < 0.8*z_cloud_base)

def filter_mixing_cloud(z, z_cloud_base, z_cloud_top):
    return (z >= z_cloud_base + 0.2*(z_cloud_top-z_cloud_base)) * (z < z_cloud_top - 0.2*(z_cloud_top-z_cloud_base))

def filter_instability(z, z_cloud_base, z_cloud_top):
    return (z < 0.5*z_cloud_base)

def filter_dwdz(z, z_cloud_base, z_cloud_top):
    return (z > 0.5*z_cloud_base)*(z < 1.2*z_cloud_base) + (z >= z_cloud_top - 0.2*(z_cloud_top-z_cloud_base))
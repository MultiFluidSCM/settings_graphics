import numpy as np

def diagnose_and_filter_b(data_les):
    '''
    Calculate the b coefficients and then filter them into the different transfer regimes
    '''
    data_b = diagnose_b(data_les)
    
    data_b_filtered = {}
    print("Diagnosing and filtering plume edge")
    data_b_filtered["plumeEdge"] = filter_b(data_b["plume"], data_b["plumeEdge"])
    print("Diagnosing and filtering particles")
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


def filter_b(data_les_plume, data_les, bl_default=850.):
    
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
    data_les["bl_top"] = []
    
    # Total cells in x
    lenx = 18000
    dx = 40
    nx = lenx/dx
    
    for time in data_les["times"][0]:
        # Find nearest time in the mean profiles data
        i = np.argmin(np.abs(data_les_plume["times"][0] - time))
        print(i)
        time_plume = data_les_plume["times"][0][i]
        print(f"Comparing t={time_plume:.0f}s (plume) with t={time:.0f}s")
        
        # Extract liquid water data and find cloud base and cloud height
        z = data_les_plume["z"]
        ql = data_les_plume["ql_2"][:,i]
        z_cloud = z[ql > 1e-5/nx**2]
        wth_res = data_les_plume["wth_res1"][:,i] + data_les_plume["wth_res2"][:,i]
        wth_res = wth_res[~np.isnan(wth_res)]
        
        # If no cloud detected, set as the approx. boundary layer height to keep the process going
        if len(z_cloud) == 0:
            # z_cloud = [bl_default]
            z_cloud = [0]
        if len(wth_res) == 0:
            wth_res = [0]
        
        z_cloud_base = np.min(z_cloud)
        z_cloud_top  = np.max(z_cloud)
        z_bl_top     = z[np.argmin(wth_res)]
        
        z_cloud_top = max(z_cloud_top, z_cloud_base)
        
        data_les["cloud_base"].append(z_cloud_base)
        data_les["cloud_top"].append(z_cloud_top)
        data_les["bl_top"].append(z_bl_top)
        
        print(f"Diagnosed cloud base: {z_cloud_base:.2f}m, Diagnosed cloud top: {z_cloud_top:.2f}m")
        
        for name, filter in filters.items():
            profile_name = f"filter_{name}"
            profile = filter(data_les["z"], z_bl_top, z_cloud_top)
            
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

def filter_all(z, z_bl_top, z_cloud_top):
    return z >= 0

def filter_mixing(z, z_bl_top, z_cloud_top):
    return (z >= 0.25*z_bl_top) * (z <= 0.75*z_bl_top)

def filter_mixing_cloud(z, z_bl_top, z_cloud_top):
    return (z >= z_bl_top + 0.25*(z_cloud_top-z_bl_top)) * (z <= z_cloud_top - 0.25*(z_cloud_top-z_bl_top))

def filter_instability(z, z_bl_top, z_cloud_top):
    return (z <= 0.25*z_bl_top)

def filter_dwdz(z, z_bl_top, z_cloud_top):
    return (z >= 0.75*z_bl_top)*(z <= z_bl_top + 0.25*(z_cloud_top-z_bl_top)) + \
           (z >= z_cloud_top - 0.25*(z_cloud_top-z_bl_top))*(z <= z_cloud_top + 0.25*(z_cloud_top-z_bl_top))
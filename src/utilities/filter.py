def filter_transfer_coefficients(settings):
    '''
    Cycle through the settings and extract only the b-coefficients which determine the transferred
    fluid properties.
    '''
    color_default = (0.,0.,0.)
    colors = {
        "mixing": (0.8,0,0.8),
        "mixing_cloud": (0,0,0.8),
        "instability": (0.9,0,0),
        "dwdz": (0.,0.7,0.),
    }
    
    superscript_default = ""
    superscripts = {
        "mixing": "MIX",
        "mixing_cloud": "MIC",
        "instability": "INS",
        "dwdz": "FRC",
    }
    
    name_default = (0.,0.,0.)
    names = {
        "mixing": "Mixing",
        "mixing_cloud": "Mixing cloud",
        "instability": "Instability",
        "dwdz": "dw/dz",
    }
    names = {
        "mixing": "Mid-BL",
        "mixing_cloud": "Mid-CL",
        "instability": "Surface",
        "dwdz": "BL/CL top",
    }
    
    settings_transfers = {}
    
    for transfer in settings:
        settings_transfers[transfer] = {}
        
        name = name_default
        if transfer in names:
            name = names[transfer]
        
        color = color_default
        if transfer in colors:
            color = colors[transfer]
        
        superscript = superscript_default
        if transfer in superscripts:
            superscript = superscripts[transfer]
        
        for setting in settings[transfer]:
            if   "bentrain" in setting:
                if "entrain" in settings[transfer]:
                    if settings[transfer]["entrain"]["value"]:
                        settings_transfers[transfer][setting] = settings[transfer][setting]
                        settings_transfers[transfer][setting]["name"] = "{} entrain".format(name)
                        settings_transfers[transfer][setting]["color"] = color
                        settings_transfers[transfer][setting]["type"] = "b21"
                        settings_transfers[transfer][setting]["symbol"] = "$b_{%s,21}^{%s}$" % (setting[-1], superscript)
            elif "bdetrain" in setting:
                if "detrain" in settings[transfer]:
                    if settings[transfer]["detrain"]["value"]:
                        settings_transfers[transfer][setting] = settings[transfer][setting]
                        settings_transfers[transfer][setting]["name"] = "{} detrain".format(name)
                        settings_transfers[transfer][setting]["color"] = color
                        settings_transfers[transfer][setting]["type"] = "b12"
                        settings_transfers[transfer][setting]["symbol"] = "$b_{%s,12}^{%s}$" % (setting[-1], superscript)
    
    return settings_transfers
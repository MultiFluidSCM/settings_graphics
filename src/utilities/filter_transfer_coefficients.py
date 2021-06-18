def filter_transfer_coefficients(settings):
    '''
    Cycle through the settings and extract only the b-coefficients which determine the transferred
    fluid properties.
    '''
    settings_transfers = {}
    
    for transfer in settings:
        settings_transfers[transfer] = {}
        
        for setting in settings[transfer]:
            if   "bentrain" in setting:
                if "entrain" in settings[transfer]:
                    if settings[transfer]["entrain"]["value"]:
                        settings_transfers[transfer][setting] = settings[transfer][setting]
                        settings_transfers[transfer][setting]["symbol"] = "$b_{%s,21}$" % (setting[-1])
            elif "bdetrain" in setting:
                if "detrain" in settings[transfer]:
                    if settings[transfer]["detrain"]["value"]:
                        settings_transfers[transfer][setting] = settings[transfer][setting]
                        settings_transfers[transfer][setting]["symbol"] = "$b_{%s,12}$" % (setting[-1])
    
    return settings_transfers
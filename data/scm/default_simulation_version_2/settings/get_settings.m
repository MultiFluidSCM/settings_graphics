function settings = get_settings(folders)
    settings.folders = folders;

    settings.model = model_settings(settings.folders);
    
    settings.plots = plot_settings(settings.folders);
    
end
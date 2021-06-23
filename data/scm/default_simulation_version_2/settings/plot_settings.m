function settings = plot_settings(folders)
    settings.folders = folders;

    % Gravitational acceleration
    settings.gravity = 9.806;

    % Figure font size
    settings.fs = 18;

    % Top of plots
    settings.zplottop = 4000;
    
    % Plot original set of figures from September 2020
    % Feature to be removed once other features optimised
    settings.plot_original_figures = false;
    
    % Plot every vertical profile (long computation)
    settings.plot_individual_profiles = true;
    
    % Save figures as .fig files?
    settings.save_figures = true;
    
    % Save figures as .png files?
    settings.save_images = true;
    
    % Render tile-based plots composed of multiply figures?
    settings.plot_combinations = true;
    
    % Indicate location of cloud base in 1D profiles?
    settings.indicate_cloud_base = true;
    
    % File containing SCM data
    %settings.scm_data = 'SCM_scheme0';     % Basic relaxation detrainment
    %settings.scm_data = 'SCM_scheme0ug1'; % ug = 1 m/s
    %settings.scm_data = 'SCM_scheme1';     % Sorting determines Mij but not etahat, qhat
    %settings.scm_data = 'SCM_scheme3';     % Sorting determines Mij and etahat, qhat
    %settings.scm_data = 'SCM_scheme4'; 
    %settings.scm_data = 'SCM_scheme5';     % Unreproducible result ???
    %settings.scm_data = 'SCM_scheme6x';     % Improved relabelling for variances, incomplete linearization
    %settings.scm_data = 'SCM_scheme6y';     % Improved relabelling for variances, better but still incomplete linearization
    %settings.scm_data = 'SCM_scheme7';     % Replace -dw2/dt by rate of mixing detrainment
    %settings.scm_data = 'SCM_scheme8';     % Improved relabelling for TKE (incomplete linearization)
    %settings.scm_data = 'SCM_scheme9dt5';  % Like scheme8 but only allow sorting where b<0. dt = 5 sec
    %settings.scm_data = 'SCM_scheme10';     % Like scheme9 but with a 'smooth switch' based on b/sigma_b
    %settings.scm_data = 'SCM_scheme10b';    % Like scheme10 but with half the sorting rate
    %settings.scm_data = 'SCM_scheme10e';    % Like scheme10b but different switch normalized on tke/L
    %settings.scm_data = 'SCM_scheme10edt5';   % 10e with dt = 5 sec
    settings.scm_data = fullfile(folders.data_scm, 'SCM_results.mat');

end

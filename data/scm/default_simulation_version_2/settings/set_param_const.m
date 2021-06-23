function param = set_param_const( )

% Set parameterization constants

% Note: setting bentrain < 1 introduces a positive feedback that can
% cause the solver to diverge when the entrainment timescale is short
% (e.g. idealised dry CBL case with large initial surface heat flux).
% It appears to be less of a problem in more realistic cases that spin
% up more gradually.

param.sigma00    = 0.001;   % Background sigma2 when nothing is going on
param.cld_thresh = 0.002;   % Threshold for detecting cloud base and cloud height
param.confrac    = 0.10;    % Reference updraft mass fraction
%param.alpha_plume = 1.5;   % Constant for updraft eta and q contrast
param.zrough     = 0.1;     % Roughness length

% Default entrainment and detrainment properties
% param.centrain  = 0.4;     % Entrainment coefficient
% param.cdetrain  = 0.7;     % Detrainment coefficient
param.bentrainw = 0.5;     % Factor for entrainment of w
param.bentraint = 1.0;     % Factor for entrainment of eta
param.bentrainq = 1.0;     % Factor for entrainment of water
param.bentrainu = 1.0;     % Factor for detrainment of u and v
param.bdetrainw = 1.0;     % Factor for detrainment of w
param.bdetraint = 1.0;     % Factor for detrainment of eta
param.bdetrainq = 1.0;     % Factor for detrainment of water
param.bdetrainu = 1.0;     % Factor for detrainment of u and v

% Custom properties for different types of entrainment and detrainment
param.sort      = set_transfer_properties_sorting();
param.dwdz      = set_transfer_properties_dwdz();
param.mix       = set_transfer_properties_mixing();
param.mix_cloud = set_transfer_properties_mixing_cloud();
param.instab    = set_transfer_properties_instability();

% Factors to multiply the turbulent length scales by
param.Lfactor1 = 1.0;
param.Lfactor2 = 1.0;

% Use sigma-weighted TKE when calculating the turbulent length scales.
param.sigma_weighted_tke = true;

% Magic numbers - dimensional constants that are not constants
% of nature - to be deprecated and avoided if at all possible
param.tke_min   = 1e-4 ;   % Minimum permitted tke (J / kg)
param.zstar_min = 50;      % Minimum allowed boundary layer depth (m)

end


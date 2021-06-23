function forcing = set_forcing()

% Set information needed for forcing
% Set time (x) and sensible (shf) - latent heat fluxes (lhf) in W m-2



% These are for testing/debugging

% Geostrophic wind
% forcing.ug = 10.0;
% forcing.vg = 0.0;

% Surface fluxes
% forcing.t   = [0;  7200; 14400; 27000; 36000; 45000; 52200];
% forcing.shf = [-30; -30;     0;     0;   100;   -10; -10];
% forcing.lhf = [30;   30;   450;   500;   420;   180;   0];


% These are the correct ARM values

% Geostrophic wind
forcing.ug = 10.0;
forcing.vg = 0.0;

% Surface fluxes
forcing.t   = [0;   14400; 23400; 27000; 36000; 45000; 52200];
forcing.shf = [-30; 90;    140;   140;   100;   -10;   -10];
forcing.lhf = [5; 250;   450;   500;   420;   180;   0];

end


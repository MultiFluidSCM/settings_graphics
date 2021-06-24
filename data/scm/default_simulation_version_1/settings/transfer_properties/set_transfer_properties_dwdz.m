function param = set_transfer_properties_dwdz( )

% Set coefficients for entrained and detrained fluid properties for
% entrainment/detrainment proportional to vertical convergence.
% Value of 1 means property of departed fluid does not change
% Value of 0 means property of receiving fluid does not change

% Note: setting bentrain < 1 introduces a positive feedback that can
% cause the solver to diverge when the entrainment timescale is short
% (e.g. idealised dry CBL case with large initial surface heat flux).
% It appears to be less of a problem in more realistic cases that spin
% up more gradually.

% Entrainment
param.entrain = false;     % Switch for entrainment
param.entrain_factor = 1;  % Multiply -dw/dz by this factor
param.bentrainw = 0.5;     % Factor for entrainment of w
param.bentraint = 1.0;     % Factor for entrainment of eta
param.bentrainq = 1.0;     % Factor for entrainment of water
param.bentrainu = 1.0;     % Factor for detrainment of u and v

% Detrainment
param.detrain = false;     % Switch for detrainment
param.detrain_factor = 1;  % Multiply -dw/dz by this factor
param.bdetrainw = 0.5;     % Factor for detrainment of w
param.bdetraint = 1.0;     % Factor for detrainment of eta
param.bdetrainq = 1.0;     % Factor for detrainment of water
param.bdetrainu = 1.0;     % Factor for detrainment of u and v

end


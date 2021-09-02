# Graphics for model settings
Programme for automatically generating graphical representations of the single column model (SCM) settings and how they compare to diagnosed values from high-resolution (LES) simulations.

SCM settings which run the [model](https://github.com/MultiFluidSCM/model) should be imported from [MultiFluidSCM/test_cases](https://github.com/MultiFluidSCM/test_cases).

# Contents
- [Sample outputs](#sample-outputs)
- [Installation](#installation)
- [Usage](#usage)

# Sample outputs

### "Automatic" output in colour using ```make_scm_settings_graphic.py```

The programme will automatically check the SCM settings and plot the relevant range which the setting falls within. Different types of transfer processes are colour coded.
SCM settings are shown with the black vertical markers. LES diagnostics for that setting are shown by the colours in the background. Darker colour means more data in that binned range.

<img src="/readme/settings_horizontal_title_color.png" width="90%">


### "Automatic" output in greyscale using ```make_scm_settings_graphic.py```

To better see the smaller (less probability) LES data diagnostics, it is better to use greyscale.

<img src="/readme/settings_horizontal_title_greyscale.png" width="90%">


### Comparing model configurations using ```compare_scm_settings.py```

Two model configurations can be compared to make it easier to track changes to the model settings as they are tuned. The graphics show the old settings in grey, the new settings in black, and an arrow to make it clear in what directions the settings have been shifted.

<img src="/readme/settings_horizontal_color_comparison.png" width="90%">


### Visualising the transfer regions using ```plot_les_transfer_regions.py```

The different colors in the settings graphics correspond to different transfer processes which occur at different altitudes. These regions can be visualised with the ```plot_les_transfer_regions.py``` script. The colors in the resulting image correspond to the colors used in the (non-greyscale) settings graphics. 

<img src="/readme/transfer_regions_plumeEdge.png" width="90%">

# Installation
Python 3 is required to run these scripts. Install with
```
sudo apt-get update
sudo apt-get install python3
```

## Required modules
Install numpy, scipy and matplotlib using
```
pip3 install numpy
pip3 install scipy
pip3 install matplotlib
```

## Upgrading Python 3 to a newer version (if old version is installed)
If you need to upgrade to a newer version of Python 3, you can use the following procedure (with the example of Python 3.9):
```
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
```
Note that by default you will have to use ```python3.9``` in the command line. In order to use ```python3```, we need to configure python 3 for which version should be prioritised:
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 2
```
A higher number is higher priority. Check this has worked using
```
sudo update-alternatives --config python3
```
and also check ```python3 --version``` to ensure Python 3.9 is being used.
In order to ensure pip is hooked up properly to the new python version, use
```
sudo apt install python3.9-distutils
pip3 install --upgrade setuptools
pip3 install --upgrade pip
pip3 install --upgrade distlib
```
and then check the version is correct using
```
python3.9 -m pip --version
```
or
```
pip3 --version
```

# Usage

Copy your test case folder (which includes the model settings) into the data folder as below:
```
cp -r path/to/MultiFluidSCM/test_cases/your_test_case_id/ path/to/MultiFluidSCM/settings_graphics/data/scm/
```

In [make_scm_settings_graphic.py](/make_scm_settings_graphic.py), change ```id_scm``` to ```your_test_case_id```. Then, run the master script with
```
python3 path/to/MultiFluidSCM/settings_graphics/make_scm_settings_graphic.py
```

In [compare_scm_settings.py](/compare_scm_settings.py), change ```id_scm1``` to the ID of the new model settings and ```id_scm2``` to the ID of the old model settings. Then, run the master script with
```
python3 path/to/MultiFluidSCM/settings_graphics/compare_scm_settings.py
```

For [plot_les_transfer_regions.py](/plot_les_transfer_regions.py), simply run the master script with
```
python3 path/to/MultiFluidSCM/settings_graphics/plot_les_transfer_regions.py
```

Data will be output to the outputs folder.

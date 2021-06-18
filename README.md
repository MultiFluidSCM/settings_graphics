# Graphics for model settings
Scripts for automatically generating graphical representations of the model settings and how they compare to diagnosed values from high-resolution (LES) simulations.

## Sample outputs

### dw/dz detrainment coefficient for moisture (default)

<img src="/readme/prototype_default.png" width="40%">


### dw/dz detrainment coefficient for moisture (wider range)

<img src="/readme/prototype_wide.png" width="40%">


### dw/dz detrainment coefficient for moisture (wider and negative)

<img src="/readme/prototype_wide_negative.png" width="40%">

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


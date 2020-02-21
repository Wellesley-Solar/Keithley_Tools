# Keithley_Tools

## Setup

### Requirement
To use all these code most conveniently, you would want to have the following installed:
 - Python 3
 - Jupyter Notebook (with Python 3)
 - Python 3 Modules: numpy, matplotlib, pySerial

### Ubuntu 18.04

```
sudo usermod -a -G tty $username
sudo usermod -a -G dialout $username
```

Then, restart your computer.

## Usage
Clone this repo, and navigate into it. Open `Jupyter Notebook` and open a Python 3 Notebook. Run `from jvtool import *` to import the classes in `jvtool.py`. Refer to `jvtool.py` and `Keithley.ipynb` for usage examples.
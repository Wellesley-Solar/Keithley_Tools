# Keithley Tools
This repo contains all of the code needed to use Keithley Tools in Dr. Belisle's Solar Lab @ Wellesley College.

## Setup

### Software Requirement
To use all these code most conveniently, you would want to have the following installed for your corresponding system:
 - Git
 - Anaconda
  - Python 3 
  - Jupyter Notebook (with Python 3; it is recommended to install both Python3 and Jupyter Notebook by installing Anaconda)
 - Python 3 Modules: numpy, scipy, matplotlib, pySerial

### Windows
Open `Anaconda Prompt` by searching for it in the search bar at the lower left. On the lab laptop, navigate to the public Github folder through the following command.
```
cd C:\Users\Public\Github
```
Open Jupyter Notebook in `Anaconda Prompt`.
```
Jupyter Notebook
```
The likely port of the serial connection to the Keithley 2401 is `/COM3`. This is what you should type into the port argument in PySerial. To look for the correct port, open the device manager on Windows.

### Ubuntu 18.04
In order to have the priviledge to access serial ports, you may need to run the following commands in terminal.
```
sudo usermod -a -G tty $username
sudo usermod -a -G dialout $username
```
Then, restart your computer.

To look for the serial port to the Keithley 2401, run the following command in terminal.
```
ls /dev/tty*
```
The default right now is to use `/dev/ttyUSB0`.

## Usage
Clone this repo, and navigate into it. Open `Jupyter Notebook` and open a Python 3 Notebook. Run `from jvtool import *` to import the classes in `jvtool.py`. Refer to `jvtool.py` and `Keithley.ipynb` for usage examples.

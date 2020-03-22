# SOP: Keithley Measurements

### For the lastest SOP, please always check [here](https://github.com/Wellesley-Solar/Keithley_Tools/blob/master/Keithley_SOP.md).
By setting Keithley 2401 in RS-232 Mode, we can control the instrument over serial communication from a laptop. Therefore, before you begin, make sure that the RS-232 cable is connected and that the following settings are configured correctly on the Keithley's setup menu if they haven't been already. 
```
Communication Mode: RS-232
BAUD:  57600
BITS: 8
PARITY: NONE
TERMINATOR: <CR>
FLOW-CTRL: NONE
```

## 1. You will likely need the following software packages on your laptop in order to use the existing code
- Git
- Anaconda
- Python 3 
- Jupyter Notebook (with Python 3; it is recommended to install both Python3 and Jupyter Notebook by installing Anaconda)
- Python 3 Modules: numpy, scipy, matplotlib, pySerial

## 2. Writing to and Reading from Keithley
To begin communicating with Keithley over your laptop, open a Jupyter Notebook, import the Python library `jvtool.py`.

```
>> from jvtool import *     # This imports the library
>> %matplotlib notebook     # allows you to resize plots
>> keith=k2401('**serial port**') # the port Keithley is on
```
You can find out the exact serial port by opening `Device Manger` on Windows and check the tab `Ports (COM & LPT)`. The likely serial port for the Keithley 2401 on Windows is `\COMx` where `x` is an integer digit. On Ubuntu 18.04, you can look for the port by typing `ls /dev/tty*` in the terminal. The likely form you will see is `/dev/ttyUSBx` where `x` is an integer digit. Please feel free to update this document if you have experience working on Mac.

To write a command to Keithley, simply call the function in a Jupyter Notebook cell.
```
>> keith.write('***Command Here***')
```
For instance, the following will make Keithley source current.
```
>> keith.write(':SOURCE:FUNCTION CURRENT')
```
If you want information such as measurements or current settings of the instrument, you would first write a command to Keithley requesting that information. For example, you have configured Keithley to start sourcing a current and measuring a voltage in return, you need to call the following to actually start getting a reading.
```
>> keith.write(':READ?')
```
Then, by simply calling the following in a separate cell, you will be returned the voltage reading on your computer screen.
```
>> keith.read()
```
All current and voltage values that Keithley uses have the standard SI units in `A` and `V`, respectively, when you read or write to the instrument. For example, if you specify `10E-10` as the sourcing current, it will translate to `1nA` current.

For a full list of commands, please look at [the Series 2400 SourceMeter User's Manual](https://download.tek.com/manual/2400S-900-01_K-Sep2011_User.pdf).

## 3. Streamlined JV Measurement
Without having to write your own Keithley commands line by line yourself, you can perform a JV Sweep by calling `simple_jv()` in `jvtool.py`:
```
>> keith.simple_jv(v_series, v_rang, i_rang, i_prot, delay=0)
```
This function operates in "Source Voltage Measure Current". It takes a list of float as the series of voltage values (input argument `v_series`) to perform current measurements at. `v_rang` is a string should be picked based on the extrema of `v_series` to provide more precise voltage sourcing range. `i_rang` is a string and should be chosen so it provides more resolutions in the current measurement. `i_prot` is also a string specifies the compliance current. `delay`, a float, gives the delay between measurements at different voltages.

Once your data collection is done, call `save_csv()` and your series of current and voltage values will be saved to a csv file.
```
>> keith.save_csv(filename)
```
The argument `filename` should be a string that ends with `.csv`.

## 4. Streamlined Conductivity Measurement
Without having to stand in front of your computer when the conductivity measurement takes hours to run, you can simply call `sweepI_senseV()` to do the job of measuring and saving the files. 
```
>> sweepI_senseV(sample, Ilist=['10E-11','0','10E-11','0'],trigcoun='1500',Ilevel='10E-8',Irang='10E-15',Vprot='10E-1',Vrang='10E-2')
```
`sample`, a string, is where you can say something about the sample you are performing the measurement on. It will be saved as part of the filename of the csv data file. `Ilist` is a list of strings that specify the current sourcing level. For each sourcing level, `trigcoun` sets the number of measurements to take before moving onto the next current sourcing level. `Ilevel` does not actually matter so you can leave it as the default. `Irang` specifies the current sourcing range so Keithley can source a precise enough current. `Vprot` is the compliance voltage. It could be useful in terms of preventing a high potential difference setting off electrochemical reactions. `Vrang` should be selected such that the voltage readings can be accurate with a good number signifcant digits. `Vrang='10E-2'`, in combination with the current configuration of this function, allows the instrument to make precise voltage measurements whose absolute value from .1mV to 999.9mV.

The function would always begin by measuring 50 data points of voltage with 0A sourcing current. A file saved from this function can have the name `I3N2V4388.89@I10E-11@1583970017.csv`. `I3N2` stands for `MAPbI3` samples in nitrogen. `V` stands for voltage measurement. As of now, there is no good way to track the time between each measurement. Given the thousands of measurement points that last over minutes if not hours, subsecond differences can be assumed to average out. Thus, the total duration is given by `4388.89` between `V` and `@`. `@I10E-11` means the current sourcing level when it is on. `@1583970017` is the time at which the file is save when you call `time.time()` in Python.

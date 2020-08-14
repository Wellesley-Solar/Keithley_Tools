#%% import packages for communicating with keithley over \COM
from jvtool import k2401
import time
import matplotlib
import pandas
# %% Enable communication with Keithley
keith=k2401('\COM4') # the port Keithley is on

#%%
sample_name = '\MAPbX3_1nA_DC_conductivity.csv'
directory_name = 'G:\Shared drives\Wellesley Solar\Current Projects\Conductivity\Becky_Data'
sample_time = 900 #desired time in minutes

# initialize values for experiment
current = []
voltage = []
volts = []
measure_time = []

# Set up source current units in Amps
set_current = '10E-10'
keith.write(':SOURCE:FUNCTION CURRENT')
keith.write(':SOUR:CURR:MODE FIXED')
keith.write(':SOUR:CURR:RANG 10E-30')
keith.write(':SOUR:CURR:LEV 0') #initil source zero volts

# Set up measure Voltage
keith.write(':SENSE:VOLT:PROTECTION 10E-1')
keith.write(':SENSE:FUNC "VOLT"')
keith.write(':SENSE:VOLT:RANG 10E-2')
keith.write(':FORM:ELEM volt')
time.sleep(0.1) #give the keithley a moment to respons

# Turn on output and start time
keith.write(':OUTPUT ON')
start=time.time()
sample_time_sec = sample_time*60 #convert to seconds for accounting with clock

#get background data 
for points in range(100):
    keith.write(':READ?')
    raw = keith.read()
    current.append(0)
    voltage.append(raw)
    measure_time.append(time.time())
    time.sleep(.1)

keith.write(':OUTPUT OFF')

#run measurement
keith.write(':SOUR:CURR:LEV ' +str(set_current))
keith.write(':OUTPUT ON')

while abs(start-time.time())<sample_time_sec:
    keith.write(':READ?')
    #time.sleep(.01)
    raw = keith.read()
    measure_time.append(time.time())
    current.append(float(set_current))
    voltage.append(raw)
    measure_time.append(time.time())
    time.sleep(5)

end = time.time()
print('Measurement Complete', end)
keith.write(":OUTPUT OFF")
run_time = [element - start for element in measure_time] #get time in seconds
#convert voltage from string to flost
element=0
while element < len(voltage):
    try: 
        volts.append(float(voltage[element]))
        element = element+1
    except ValueError:
        volts.append(0)
        print(element)
        element = element+1

results = pandas.DataFrame(list(zip(run_time, current, volts)), columns=['Time [s]', 'Current [A]', 'Voltage [V]']) #make dataframe
results.to_csv(directory_name+str(sample_name)) #savefile


# %% Works with GPIB Cable 
# Import necessary packages
from pymeasure.instruments.keithley import Keithley2400
import numpy as np
import pandas as pd
from time import sleep

# Set the input parameters
data_points = 50
averages = 50
max_current = 0.000001
min_current = -max_current

# Connect and configure the instrument
sourcemeter = Keithley2400("GPIB::24")
sourcemeter.reset()
sourcemeter.use_front_terminals()
sourcemeter.measure_voltage()
sourcemeter.apply_current(compliance_voltage=5)
sleep(0.1) # wait here to give the instrument time to react
sourcemeter.config_buffer(points=10, delay=0)

# Allocate arrays to store the measurement results
currents = np.linspace(min_current, max_current, num=data_points)
voltages = np.zeros_like(currents)
voltage_stds = np.zeros_like(currents)
#%%
# Loop through each current point, measure and record the voltage
for i in range(data_points):
    sourcemeter.source_current = currents[i]
    sourcemeter.enable_source()
    sleep(0.1)
    sourcemeter.start_buffer()
    sourcemeter.wait_for_buffer()
    sourcemeter.reset_buffer()

    # Record the average and standard deviation
    print(sourcemeter.means)
    #voltage_stds[i] = sourcemeter.standard_devs

# Save the data columns in a CSV file
data = pd.DataFrame({
    'Current (A)': currents,
    'Voltage (V)': voltages,
    'Voltage Std (V)': voltage_stds,
})
data.to_csv('example.csv')

sourcemeter.shutdown()

# %%

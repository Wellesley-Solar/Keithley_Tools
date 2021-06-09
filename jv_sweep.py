#%% import packages for communicating with keithley over \COM
from jvtool import*
import matplotlib
import pandas
import numpy as np
# %% Enable communication with Keithley
 keith=k2401('\COM3') # the port Keithley is on, may need to update and/or unplug the USB to get it to work

#%% UPDATE PARAMETERS FOR YOUR EXPERIMENT

#set your sample name and where you'll save data
sample_name = '\\diode_test.csv'
directory_name = r'C:\Users\rbelisle\Desktop\JVData'

#set desired voltage range
v_min = -.5 #minimum voltage in Volts
v_max = 3 #maximum voltage in Voltas
v_step = .01 #step size in Volts

#set current compliance
compliance = '2E-2'

#%% Initialize values and settings for experiment 
volts = np.linspace(v_min, v_max, int(round((v_max-v_min)/v_step))) #create integers for desired source voltages

current = []
voltage = []


# Set up source voltage units in Amps
start_volts =     current_voltage = "{:.2e}".format((volts[0]))

keith.write(':SOURCE:FUNCTION VOLTAGE')
keith.write(':SOUR:VOLT:MODE FIXED')
keith.write(':SOUR:VOLT:RANG 10E0')
keith.write(':SOUR:VOlT:LEV '+start_volts) #initil source zero volts

# Set up measure current
keith.write(':SENSE:CURR:PROTECTION '+compliance)
keith.write(':SENSE:FUNC "CURR"')
keith.write(':SENSE:CURR:RANG 1E-2')
keith.write(':FORM:ELEM CURR')
time.sleep(0.1) #give the keithley a moment to respond

#TODO get this to work with autoranging for current
#run experiment
keith.write(':OUTPUT ON')

for i in range(len(volts)):
    current_voltage = "{:.2e}".format((volts[i]))
    keith.write(':SOUR:VOLT:LEV ' +current_voltage)
    time.sleep(.1)

    keith.write(':READ?')
    raw = keith.read()
    current.append(float(raw))
    voltage.append(volts[i])
    time.sleep(.01)

keith.write(':OUTPUT OFF')

# plot data 
fig1, ax1 = plt.subplots( figsize=(6,4))
ax1.set_xlabel('Voltage [V]', size=12)
ax1.set_ylabel('Current [A]', size = 12)
ax1.set_xlim(v_min,v_max)
ax1.plot(voltage,current, 'r')

# %% save data
results = pandas.DataFrame(list(zip(current, voltage)), columns=['Current [A]', 'Voltage [V]']) #make dataframe
results.to_csv(directory_name+str(sample_name)) 

# %%

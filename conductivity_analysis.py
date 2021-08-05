#%%

import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats
from scipy.optimize import curve_fit
import pandas as pd

#%%
path = r'/Users/rbelisle/Desktop' # use your path
data = path+'/MAPBI3_N2_1nA.csv'
measure = pd.read_csv(data,delimiter=',',header=0) #read file

# %% Call out relevant variables
time = np.array(measure['Time [s]'])
voltage = np.array(measure['Voltage [V]'])
current = np.array(measure['Current [A]'])

#%%
fig2,ax2 = plt.subplots()
ax2.set_xlabel('Time [s]',size=14) #Define x-axis label
ax2.set_ylabel('Voltage [V]',size=14)#Define y-axis label
#ax2.set_ylim([0,0.015])
#ax2.set_xlim([0,3000])
#ax2.plot(time2-50,voltage2-voltage2[500], 'ro--')
plt.plot(time,voltage, 'ko--')
#plt.plot(time,current, 'ro--')

#%%
def simple_model(t, Vo, tao):
    return Vo*(1-np.exp(-t*tao))
# %%

p0 = (.0035, .02)
popt,pcov = curve_fit(simple_model, time-10, voltage-voltage[100], p0, maxfev=6000)
plt.plot(time-10,voltage-voltage[100], 'ko--')
plt.plot(time,simple_model(time, *popt))
print(popt[0], np.sqrt(np.diag(pcov))[0])
# %%
p0 = (.0035, .02)
popt,pcov = curve_fit(simple_model, time2[501:1000]-50, voltage2[501:1000]-voltage2[500], p0, maxfev=6000)
plt.plot(time2[0:1000]-50,voltage2[0:1000]-voltage2[500], 'ko--')
plt.plot(time[0:900],simple_model(time[0:900], *popt))
print(popt[0], np.sqrt(np.diag(pcov))[0])

# %%

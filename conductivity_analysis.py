#%%

import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.stats
import scipy.optimize 
import pandas as pd

#%%
path = r'/Users/rbelisle/Desktop' # use your path
data = path+'/MAPBBr2I_sample2_N2_1nA.csv'
measure = pd.read_csv(data,delimiter=',',header=0) #read file

# %% Call out relevant variables
time = np.array(measure['Time [s]'])
voltage = np.array(measure['Voltage [V]'])
current = np.array(measure['Current [A]'])

#%%
fig2,ax2 = plt.subplots()
ax2.set_xlabel('Time [s]',size=14) #Define x-axis label
ax2.set_ylabel('Voltage [V]',size=14)#Define y-axis label
#ax2.set_ylim([0,0.02])
ax2.set_xlim([-100,2000])
plt.plot(time,voltage, 'ko--')
plt.plot(time,current*10**6)


#%%
def simple_model(t_, C, V0, Vinf):
    Re=Vinf/Iin;
    Ri=Vinf*V0/(Iin*(Vinf-V0));
#     C=10^-7*5;
    return (Ri*Re)/(Ri+Re)*Iin*np.exp(-t_/((Re+Ri)*C))-Re*Iin*(np.exp(-t_/((Re+Ri)*C))-1);
# %%
Iin = current[100]
p0 = [10**-7, .0035, .02]
popt,pcov = curve_fit(simple_model, time[0:700], voltage[0:700], p0, maxfev=6000)
plt.plot(time[0:700],voltage[0:700], 'ko--')
plt.plot(time[0:900],simple_model(time[0:900], *popt))
# %%

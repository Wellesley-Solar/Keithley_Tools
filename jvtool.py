import serial, string, time, csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

class k2401:
    """
    Class k2401 inspired by Professor Brad Minch's Python code

    More details can be found in Series 2400 SourceMeter User's Manual:
    https://download.tek.com/manual/2400S-900-01_K-Sep2011_User.pdf0S-900-01_K-Sep2011_User.pdf&usg=AOvVaw3q6tLQ1qQb21E2OXp-eijR
    """

    def __init__(self, port, baudrate = 57600):
        self.dev = serial.Serial(port, baudrate)
        self.v_series = []
        self.i_series = []


    def write(self, command):
        ''' write command to Keithley
        command: string; keithley 2401 standard commands
        '''
        self.dev.write(('{0!s}\r'.format(command)).encode())


    def read(self):
        ''' reads serial buffer on computer and remove formatting bytes
        command: string; keithley 2401 standard commands
        '''

        temp_read=str(self.dev.read(self.dev.in_waiting))
        pos_b=temp_read.find("b'")+2
        pos_r=temp_read.find("\\r'")
        
        return temp_read[pos_b:pos_r]


    def save_csv(self,filename):
        ''' Save v and i lists to separate rows of a csv file
        filename: string; filename with .csv extension
        '''
        with open(filename, 'w', newline='') as csvfile:
            jvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            v_temp=list(self.v_series)
            v_temp.insert(0,'V')
            i_temp=list(self.i_series)
            i_temp.insert(0,'I')
            jvwriter.writerow(v_temp)
            jvwriter.writerow(i_temp)


    def simple_jv(self, v_series, v_rang, i_rang, i_prot, delay=0.5):
        ''' Simple JV measurement of current as a range of voltage is sweeped through
        v_series: list/np_array; a series of voltage to set Keithley to
        v_rang: str; 
        i_rang: str; 
        i_prot: str; 
        delay: float; wait time between querying info from Keithley and reading serial buffer
        
        Developed based on the example on 3-19 (Page74) of User Manual
        '''
        self.v_series=v_series
        self.write(':SOUR:FUNC VOLT')               # Select voltage source
        self.write(':SOUR:VOLT:MODE FIXED')         # Fixed voltage source mode
        self.write(':SOUR:VOLT:RANG '+v_rang)            # Specify voltage source range
        self.write(':SENS:CURR:PROT '+i_prot)         # Specify current compliance in Amp
        self.write(':SENS:FUNC "CURR"')             # Select current measure function
        self.write(':SENS:CURR:RANG '+i_rang)         # Specify current measurement range
        self.write(':FORM:ELEM CURR')               # Return current reading only
        self.write(':OUTPut ON')                    # Turn on OUTPUT
        _ = self.read()                             # Clear the serial buffer
        self.i_series = []                          # Clear the i series to store incoming output
        for v in self.v_series:
            
            self.write(':SOUR:VOLT:LEV '+str(v))    # Source given output voltage
            self.write(':READ?')                    # Trigger, acquire reading
            time.sleep(delay)                       # Delay before reading 
            self.i_series.append(float(self.read()))           # Read measurement and add to output series
            
        self.write(':OUTPUT OFF')

    def plotIV(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('I-V Curve')
        self.ax.plot(self.v_series,self.i_series)
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')
        self.ax.set_xlabel('Voltage (V)')
        self.ax.set_ylabel('Current Density (mA*cm^-2)')   



class analyzer:
    def __init__(self, filename, activearea):
        '''

        activearea: active area of the device in cm^2
        '''
        self.filename=filename
        self.activearea=activearea
        temp=[]
        with open(self.filename, newline='') as csvfile:
            jvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # print(spamreader)
            for row in jvreader:
                temp.append(row)
        self.v_series=np.array([float(i) for i in temp[0][1:]])
        self.i_series=np.array([float(i)*-1000 for i in temp[1][1:]]) # Import current series but flip the sign and use mAmp

        # Calculate Isc and Voc
        self.Isc = np.interp(0, self.v_series,self.i_series)
        self.Voc = np.interp(0, np.flip(self.i_series), np.flip(self.v_series))
        self.IscVoc = self.Isc*self.Voc
        

        # Simple Model Fitting
        self.fitparam, self.fitparam_cov = optimize.curve_fit(self.simple_model, self.v_series, self.i_series, bounds=([0,1.0,0], [10^6, 2.0, 10^6])) 
        [self.I0, self.n, self.Rsh] = self.fitparam     # I0: reverse saturation current
                                                        # n: ideality factor
                                                        # Rsh: shunt resistance

        # Simple Model Fill Factor
        self.v_maxpower=optimize.minimize(self.simple_model_power,self.Voc/2).x
        self.i_maxpower=self.simple_model(self.v_maxpower,*self.fitparam)
        self.ff = self.v_maxpower*self.i_maxpower/self.IscVoc


        print('Jsc', self.Isc/self.activearea, "mA*cm^-2")
        print('Voc', self.Voc, "V")
        print('Fill Factor', self.ff)


    def plotJV(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('J-V Curve')
        self.ax.plot(self.v_series,np.multiply(self.i_series,1/self.activearea))
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')
        self.ax.set_xlabel('Voltage (V)')
        self.ax.set_ylabel('Current Density (mA*cm^-2)')   


    def plotJVfit(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('J-V Curve')
        self.ax.plot(self.v_series,np.multiply(self.i_series,1/self.activearea), 'b.',label='measurement',LineWidth=2)
        self.ax.plot(self.v_series,np.multiply(self.simple_model(self.v_series,*self.fitparam),1/self.activearea), 'r-',label='fit', LineWidth=2)
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')
        self.ax.set_xlabel('Voltage (V)')
        self.ax.set_ylabel('Current Density (mA*cm^-2)')   
        self.ax.legend()


    def simple_model(self, v, I0, n, Rsh):
        return self.Isc-I0*(np.exp(v/(n*0.0259))-1)-v/Rsh

    def simple_model_power(self, v):
        return -(self.Isc-self.I0*(np.exp(v/(self.n*0.0259))-1)-v/self.Rsh)*v

    


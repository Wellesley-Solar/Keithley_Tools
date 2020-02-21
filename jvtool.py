import serial, string, time, csv
import numpy as np
import matplotlib.pyplot as plt

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
            
            v_temp=list(self.v)
            v_temp.insert(0,'V')
            i_temp=list(self.i)
            i_temp.insert(0,'I')
            jvwriter.writerow(v_temp)
            jvwriter.writerow(i_temp)


    def simple_jv(self, v_series, v_rang, i_rang, i_prot, delay):
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
        self.write(':SOUR:VOLT:RANG .5')            # Specify voltage source range
        self.write(':SENS:CURR:PROT 10E-1')         # Specify current compliance in Amp
        self.write(':SENS:FUNC "CURR"')             # Select current measure function
        self.write(':SENS:CURR:RANG 10E-1')         # Specify current measurement range
        self.write(':FORM:ELEM CURR')               # Return current reading only
        self.write(':OUTPut ON')                    # Turn on OUTPUT
        _ = self.read()                             # Clear the serial buffer
        self.i_series = []                          # Clear the i series to store incoming output
        for v in self.v_series:
            
            self.write(':SOUR:VOLT:LEV '+str(v))    # Source given output voltage
            self.write(':READ?')                    # Trigger, acquire reading
            time.sleep(delay)                       # Delay before reading 
            self.Iout.append(self.read())           # Read measurement and add to output series
            
        self.write(':OUTPUT OFF')



class analyzer:
    def __init__(self, filename):
        temp=[]
        with open(filename, newline='') as csvfile:
            jvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            # print(spamreader)
            for row in jvreader:
                temp.append(row)
        self.v_series=[float(i) for i in temp[0][1:]]
        self.i_series=[float(i) for i in temp[1][1:]]

        # Calculate Isc and Voc !!! To be improved because not all solar cells are resistive heater !!!
        _,self.Isc = np.polyfit(self.v_series,self.i_series,1)  # To be improved because not all solar cells are resistive heater
        _,self.Voc = np.polyfit(self.i_series,self.v_series,1)  # To be improved because not all solar cells are resistive heater
        self.IscVoc = self.Isc*self.Voc

        # Calculate Fill Factor !!! to be improved with numerically calculated max power instead
        product=np.multiply(self.v_series,self.i_series)
        outPower=[]
        for i,p in enumerate(list(product)):
            if p<0:
                outPower.append(p)
        try:
            self.ff = abs(min(outPower))/abs(self.IscVoc)
        except ValueError:
            print('A fill factor is not calculated.')


        print('Isc', self.Isc)
        print('Voc', self.Voc)
        print('Fill Factor', self.ff)


    def plotJV(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('J-V Curve')
        self.ax.plot(self.v_series,self.i_series)
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')
        self.ax.set_xlabel('Voltage (V)')
        self.ax.set_ylabel('Current (A)')   


    

#%%
import serial, string 

class K2400ser:

    def __init__(self, port, **kwargs):
        self.dev = serial.Serial(port, baudrate = 57600)
        self.function = kwargs.get('function', None)
        self.ilimit = kwargs.get('ilimit', None)
        self.vlimit = kwargs.get('vlimit', None)
        self.write(":SYSTEM:BEEPER:STATE 0")
        if self.ilimit==None:
            self.write(":SENSE:CURRENT:PROTECTION:LEVEL?".encode())
            self.ilimit = float(self.read())
        else:
            self.write(':SENSE:CURRENT:PROTECTION:LEVEL {0!s}'.format(self.ilimit))
        if self.vlimit==None:
            self.write(':SENSE:VOLTAGE:PROTECTION:LEVEL?')
            self.vlimit = float(self.read())
        else:
            self.dev.write(':SENSE:VOLTAGE:PROTECTION:LEVEL {0!s}'.format(self.vlimit))
        if self.function==None:
            self.function = self.get_function()
        self.set_function(self.function)

    def write(self, command):
        self.dev.write(('{0!s}\r'.format(command)).encode())

    def read(self):
        ret = ''
        done = False
        while not done:
            numbytes = self.dev.inWaiting()
            while numbytes==0:
                numbytes = self.dev.inWaiting()
            while numbytes!=0:
                ret = ret + str(self.dev.read(numbytes))
                numbytes = self.dev.inWaiting()
            if ret[-1]=='\r':
                done = True
        return string.rstrip(ret)

    def get_function(self):
        self.write(':SOURCE:FUNCTION?')
        ans = self.read()
        if ans=='CURR':
            return 1
        else:
            return 0

    def set_function(self, fn):
        if fn==0:
            self.write(':SOURCE:FUNCTION VOLTAGE')
            self.write(':SOURCE:VOLTAGE:RANGE:AUTO 1')
            self.write(':SENSE:FUNCTION "CURRENT"')
            self.write(':SENSE:CURRENT:PROTECTION:LEVEL {0!s}'.format(self.ilimit))
            self.write(':FORMAT:ELEMENTS CURRENT')
        else:
            self.write(':SOURCE:FUNCTION CURRENT')
            self.write(':SOURCE:CURRENT:RANGE:AUTO 1')
            self.write(':SENSE:FUNCTION "VOLTAGE"')
            self.write(':SENSE:VOLTAGE:PROTECTION:LEVEL {0!s}'.format(self.vlimit))
            self.write(':FORMAT:ELEMENTS VOLTAGE')
        self.function = fn

    def get_meas(self):
        done = 0
        while not done:
            if self.function==0:
                self.write(':MEASURE:CURRENT?')
            else:
                self.write(':MEASURE:VOLTAGE?')
            ret = self.read()
            try:
                value = float(ret)
            except ValueError:
                print('Error trying to convert "{0}" to a float, trying again...'.format(ret))
            else:
                done = 1
        return [value, self.function]

    def set_source(self, value, units = None):
        if units==None:
            units = self.function
        if self.function!=units:
            self.set_function(units)
            self.on()
        if units==0:
            self.write(':SOURCE:VOLTAGE {0!s}'.format(value))
        else:
            self.write(':SOURCE:CURRENT {0!s}'.format(value))

    def off(self):
        self.write(':OUTPUT OFF')

    def on(self):
        self.write(':OUTPUT ON')

    def set_digout(self, value):
        if value>=0 and value<16:
            self.write(':SOURCE2:TTL {0!s}'.format(int(value)))

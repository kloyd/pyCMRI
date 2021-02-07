# Use PYSerial
import serial

class CMRI:

    def __init__(self):
        self.serialPort = None
        self.baud_rate = 0
        self.maxBuf = 0
        self.abort_in = 0
        self.input_tries = 0
        self.init_err = 0

    def initialize_port(self, serial_port, baud_100, maximumBuffers):
        #  serial_port
        # BAUD100  = PC baud rate divided by 100
        # MAXBUF   = Maximum number of input bytes allowed in MSComm's...
        #      ...input data buffer before declare PC overrun error
        print("Init port " + serial_port)
        self.baud_rate = baud_100 * 100
        self.serialPort = serial.Serial(serial_port, self.baud_rate)
        self.maxBuf = maximumBuffers

    def close_port(self):
        self.serialPort.close()


def init_railroad(cmri):
    print("Initialize Railroad")

def read_railroad(cmri):
        print("Read Railroad")

print("CMRI Starting")
cmri = CMRI()

cmri.initialize_port("/dev/ttyUSB0", 5760, 50)
init_railroad(cmri)
read_railroad(cmri)

cmri.close_port()

print("CRMI Exiting")
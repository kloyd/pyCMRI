# Use PYSerial
import serial
# Signals for interrupt
from signal import signal, SIGINT
from sys import exit
import time


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

    def init_node(self, UA, DL, number_dp, num_out_bytes, max_tries, num_in_bytes, num_two_lead_sigs, ct):
        # Initialize a CMRI Node
        # node_address - node number assigned on dip switches
        # delay, number_dp
        # CT is the array for config ports_
        #      UA       = USIC address (range 0 to 127) unless using...
        # DL       = USIC transmission delay
        # strNDP     = Node definition parameter = "M", "N" or "X"
        # iNumOutputBytes = number of output bytes in the buffer
        # iNumInputBytes = number of input bytes in the buffer
        # MAXTRIES = Maximum number of PC tries to read input bytes prior to PC aborting inputs
        pass


def handler(signal_received, frame):
    print(f'\nSignal {signal_received} caught.')
    cmri.close_port()
    print("CRMI Exiting")
    exit(0)


def init_railroad(cmri):
    print("Initialize Railroad")


def read_railroad(cmri):
    print("Read Railroad")


def signal_logic(cmri):
    print("Signal Logic")


def write_railroad(cmri):
    print("Write Railroad")


def main():
    print("CMRI Starting")
    cmri.initialize_port("/dev/ttyUSB0", 5760, 50)
    init_railroad(cmri)
    signal(SIGINT, handler)
    while True:
        read_railroad(cmri)
        signal_logic(cmri)
        write_railroad(cmri)
        time.sleep(10)


if __name__ == "__main__":
    cmri = CMRI()
    main()

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
        # REM**GLOBALIZE SERIAL PROTOCOL HANDLING VARIABLES
        #DIM SHARED OB(60), IB(60), CT(15), TB(80), CLOR(170)
        out_byte = [n for n in range(60)]
        in_byte = [n for n in range(60)]
        ct = [n for n in range(15)]
        tx_byte = [n for n in range(80)]
        lm = 0 # length of message

    
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

    def init_node(self, ua, dl, node_type, ns, num_out_bytes, num_in_bytes, max_tries, ct):
        # Initialize a CMRI Node
        # node_address - node number assigned on dip switches
        # delay, number_dp
        # CT is the array for config ports_
        # UA       = USIC address (range 0 to 127) unless using...
        # DL       = USIC transmission delay
        # strNDP     = Node definition parameter = "M", "N" or "X"
        # iNumOutputBytes = number of output bytes in the buffer
        # iNumInputBytes = number of input bytes in the buffer
        # ns = number of 4 card sets or number of searchlights
        # MAXTRIES = Maximum number of PC tries to read input bytes prior to PC aborting inputs
        pass

    def txpack(self):
        """
        SUB TXPACK()
        Transmit packet from PC to NODE 
        Use with SUSIC and SMINI nodes """

        # FORM PACKET TO SEND TO USIC, SUSIC OR SMINI
        self.tx_byte[1] = 255              #Set 1st start byte to all 1's
        self.tx_byte[2] = 255 #TB(2) = 255              #Set 2nd start byte to all 1's
        self.tx_byte[3] = 2 #TB(3) = 2                #Define start-of-text (STX = 2)
        self.tx_byte[4] = self.ua + 65 #TB(4) = UA + 65          #Add 65 offset to USIC address
        self.tx_byte[5] = self.mt #TB(5) = MT               #Define message type
        tp = 6                   #Define next position for transmit pointer
        if self.mt != 80:
            #goto ENDMSG   #Poll request so branch to end message
            i = 1
            while i <= self.lm:
                # escape control char by prefixing with 16
                if self.out_byte[i] == 2 | self.out_byte == 3 | self.out_byte == 16:
                    self.tx_byte[tp] = 16
                    tp = tp + 1
                # add actual output byte
                self.tx_byte[tp] = self.out_byte[tp]
                tp = tp + 1
    

        self.tx_byte[tp] = 3 # (TP) = 3  'Add end-of-text (ETX = 3)

        self.serialPort.write(self.tx_byte)

  #REM**TRANSMIT PACKET TO USIC, SUSIC OR SMINI
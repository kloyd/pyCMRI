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
        self.out_byte = []
        self.in_byte = []
        self.tx_byte = []
        for n in range(0, 60):
            self.out_byte.append(0)
        for n in range(0, 60):
            self.in_byte.append(0)
        ct = [n for n in range(15)]
        for n in range(0, 80):
            self.tx_byte.append(0)
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

    def init_node(self, node_number, dl, node_type, ns, num_out_bytes, num_in_bytes, max_tries, ct):
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
        # pass
        for n in range(0,60):
            self.out_byte[n] = 0
        
        message_type = ord('I')             # Define message type = "I" (decimal 73)
        self.out_byte[0] = ord(node_type)   # Define node definition parameter
        self.out_byte[1] = int(dl / 256)    # Set USIC delay high-order byte
        self.out_byte[2] = dl % 256         # Set USIC delay low-order byte
        self.out_byte[3] = ns               #D efine number of card sets of 4 for USIC and SUSIC cases 
                                            # Or number of 2-lead yellow aspect oscillating signals for SMINI.

        lm = 3  #Initialize length of message to start of loading CT elements

        # M == SMINI node. X = SUSIC node.
        if node_type == "M":
            # init SMINI - only send CT if NS > 0
            # Always 6 configuration bytes in CT for SMINI
            if ns > 0:
                for i in range(0, 6):
                    lm = lm + 1
                    self.out_byte[lm] = ct[i]
        else:
            #init SUSIC
            # ns is number of 4 card sets in the IOMBX
            #INITUSIC:
            #**SUSIC-NODE (either "N" or "X") SO LOAD CT( ) ARRAY ELEMENTS
            #FOR I = 1 TO NS     #Loop through number of card sets...
            #             #LM = LM + 1      #...accumulating message length while...
            #OB(LM) = CT(I)   #...loading card type definition CT...
            #NEXT I              #...array elements into output byte array
            #GOTO TXMSG  #CT( )s complete so branch to transmit initialization...
                             #...message to interface
            for i in range(0, ns):
                lm = lm + 1
                self.out_byte[lm] = ct[i]

        #
        self.txpack(node_number, message_type, message_length=lm)
        # clean up output bytes
        #**COMPLETED USE OF OUTPUT BYTE ARRAY SO CLEAR IT BEFORE EXIT SUBROUTINE
        for i in range(0, num_out_bytes + 1):
            self.out_byte[i] = 0


    def txpack(self, node_number, message_type, message_length):
        """
        SUB TXPACK()
        Transmit packet from PC to NODE 
        Use with SUSIC and SMINI nodes """

        # FORM PACKET TO SEND TO USIC, SUSIC OR SMINI
        self.tx_byte[0] = 255               #Set 1st start byte to all 1's
        self.tx_byte[1] = 255               #Set 2nd start byte to all 1's
        self.tx_byte[2] = 2                  #Define start-of-text (STX = 2)
        self.tx_byte[3] = node_number + 65  #Add 65 offset to NODE address
        self.tx_byte[4] = message_type      #Define message type
        tp = 5                   #Define next position for transmit pointer
        if message_type != 80:
            #goto ENDMSG   #Poll request so branch to end message
            i = 0
            while i <= message_length:
                # escape control char by prefixing with 16
                if self.out_byte[i] == 2 | self.out_byte[i] == 3 | self.out_byte[i] == 16:
                    self.tx_byte[tp] = 16
                    tp = tp + 1
                # add actual output byte
                self.tx_byte[tp] = self.out_byte[tp]
                tp = tp + 1
    

        self.tx_byte[tp] = 3 # (TP) = 3  'Add end-of-text (ETX = 3)

        # self.serialPort.write(self.tx_byte)
        print(self.tx_byte)

  #REM**TRANSMIT PACKET TO USIC, SUSIC OR SMINI
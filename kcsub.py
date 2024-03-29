import cmri
# Signals for interrupt
from signal import signal, SIGINT
from sys import exit
import time

def handler(signal_received, frame):
    print('\nSignal {signal_received} caught.')
    cmri.close_port()
    print("CRMI Exiting")
    exit(0)


def init_railroad(cmri):
    print("Initialize Railroad")
    # def init_node(self, ua, dl, node_type, ns, num_out_bytes, num_in_bytes, max_tries, ct):
    # SUSIC cards = OOII = 90 = 5A = 01 01 10 10
    ct = [90]
    cmri.init_node(0, 100, "X", 1, 8, 8, 5, ct)



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
    cmri = cmri.CMRI()
    main()

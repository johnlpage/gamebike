
from pprint import pprint
import struct
import math
import logging
import time
import hid
import gamebike.controlmapbits as cmb
#A small slide clicker with 4 buttons
#For Brakes etc.
CLICKER_VID=0x1d57
CLICKER_DID=0xad03



class Clicker(object):
    def __init__(self):
      
        logging.basicConfig(level=logging.INFO)
        try:
            
            self.clicker  = hid.device()
            logging.info("Opening Clicker")
            self.clicker.open(CLICKER_VID, CLICKER_DID)
            self.clicker.set_nonblocking(1)
        except Exception as e:
            logging.error(f"Unable to open  Clicker -  is it plugged in and do the VID and DID match? {e}\n")
            self.clicker = False

    def get_button(self):
        if self.clicker:
            clicker_data = bytearray(self.clicker.read(64))
            if clicker_data :
                byte = clicker_data[cmb.CLICKER_BUTTONS]
                if byte in cmb.CLICKER_UP:
                    return 1
                if byte in cmb.CLICKER_DOWN:
                    return 3
                if byte in cmb.CLICKER_RIGHT:
                    return 2
                if byte in cmb.CLICKER_LEFT:
                    return 4
        return 0


if __name__ == "__main__":

    print("Testing clicker standalone")
    clicker = Clicker()

    while True:
        v = clicker.get_button()
        if v>0:
            logging.info(v)


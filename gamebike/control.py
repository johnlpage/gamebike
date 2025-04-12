from pprint import pprint
import struct
import math
import logging
import time
import hid

# A small slide clicker with 4 buttons
# For Brakes etc.
CLICKER_VID = 0x1D57
CLICKER_DID = 0xAD03
CLICKER_BUTTONS = 2
CLICKER_LEFT = [0x4B]
CLICKER_RIGHT = [0x4E]
CLICKER_UP = [0x05]
CLICKER_DOWN = [0x3E, 0x29]  # Toggles


class Clicker(object):
    def __init__(self):

        logging.basicConfig(level=logging.INFO)
        try:

            self.clicker = hid.device()

            self.clicker.open(CLICKER_VID, CLICKER_DID)
            self.clicker.set_nonblocking(1)
            logging.info("Handlebar control available")
        except Exception as e:
            logging.error(f"Handlebar control not plugged in\n")
            self.clicker = False

    def get_button(self):
        if self.clicker:
            clicker_data = bytearray(self.clicker.read(64))
            if clicker_data:
                byte = clicker_data[CLICKER_BUTTONS]
                if byte in CLICKER_UP:
                    return 1
                if byte in CLICKER_DOWN:
                    return 3
                if byte in CLICKER_RIGHT:
                    return 2
                if byte in CLICKER_LEFT:
                    return 4
        return 0


if __name__ == "__main__":

    print("Testing clicker standalone")
    clicker = Clicker()

    while True:
        v = clicker.get_button()
        if v > 0:
            logging.info(v)

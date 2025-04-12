# This class if very specific to a Pi 4 / Pi Zero
# It uses a virtual HID Device configured using  https://github.com/milador/XAC-Virtual-Joystick
# You need to run the define_controller script to set up the virtual device
# Each time you boot


# Keeing this independant of the underlying game were possible
# Might need to use a combination of cmb and device setup if I want ot use the PS3 again

#import gamebike.controlmapbits as cmb
import xac_controlmapbits as cmb
from pprint import pprint
import logging
import time

VXACDEVICE = "/dev/hidg0"
DESC_SIZE = 17
STEERING_SENSITIVITY = 9 

class VirtualXAC(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.emulated_controller_fd = None
    
        self.XAC_data = bytearray([0] * DESC_SIZE)
        logging.debug(''.join(format(x, '02x') for x in self.XAC_data) )

    def setup_XAC(self):
        try:
            self.emulated_controller_fd = open(VXACDEVICE, "rb+", buffering=0)
            logging.debug("Found suitable HID device")
            return True
        except Exception as e:
            logging.error(
                """Unable to open virtual Joystick - have you created it
and is this running with permissions to write to it?"""
                + str(e)
            )
            return False

    # Lets us write multie changes at one time

    def send(self):
        #logging.debug(self.XAC_data.hex())
        self.emulated_controller_fd.write(self.XAC_data)

    # Input range from -100 to 100
    def steering(self,angle):
        STEER_MID = 32767
        val = int((angle * STEER_MID)/100) + STEER_MID
        self.XAC_data[1] = int(val / 256)
        self.XAC_data[0] = int(val % 256)
        logging.debug(''.join(format(x, '02x') for x in self.XAC_data) )
        self.send()



    # Pressure is -110 to 100
    def accelerator(self, pressure):

        ZAXIS_HIGHBYTE = 9
        ZAXIS_LOWBYTE = 8
        MIDPOINT = 512
        value = MIDPOINT + int((pressure*MIDPOINT)/100)

        self.XAC_data[ZAXIS_LOWBYTE] = value % 256
        self.XAC_data[ZAXIS_HIGHBYTE] = int(value / 256)
        #logging.debug(pressure%256)

    def reset(self):
        self.XAC_data = bytearray([0] * DESC_SIZE)
        self.send()
        

    #A Momentary push of n milliseconds
    def _push_button(self,button,millis):
        self.reset()

        self.XAC_data[button[0]] |= button[1]
        for h in range(0,int(millis/100)):
            self.send()
            time.sleep(0.1)
        
        self.reset()
        self.send()

    #Dpad encoding is different as only one duirection at a time
    def _push_dpad(self,button,millis):
        self.reset()
        self.XAC_data[button[0]] &= ~cmb.XAC_DPAD_MASK
        self.XAC_data[button[0]] |= button[1]
        for h in range(0,int(millis/100)):
            self.send()
            time.sleep(0.1)
        
        self.reset()
        self.send()


  
    

if __name__ == "__main__":

    print("Testing class VirtualXAC standalone")
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)d -  %(threadName)s %(message)s')
     
    vXAC = VirtualXAC()
   
    vXAC.setup_XAC()
    #vXAC.configure_steam()
    
    #100% left to 100% right and 100% accelerate to 100% brake/reverse
    while True:
        for x in range(-100,100):
            vXAC.steering(x)
            vXAC.accelerator(x)
            vXAC.send()
            time.sleep(0.01)
        for x in range(100,-100,-1):
            vXAC.steering(x)
            vXAC.accelerator(x)
            vXAC.send()
            time.sleep(0.01)


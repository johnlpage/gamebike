# This class if very specific to a Pi 4 / Pi Zero
# It uses a virtual HID Device configured using  https://github.com/milador/XAC-Virtual-Joystick
# You need to run the define_controller script to set up the virtual device
# Each time you boot


# Keeing this independant of the underlying game were possible
# Might need to use a combination of cmb and device setup if I want ot use the PS3 again

import gamebike.controlmapbits as cmb
from pprint import pprint
import logging
import time

VWHEELDEVICE = "/dev/hidg0"

STEERING_SENSITIVITY = 9 

class VirtualWheel(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.emulated_controller_fd = None
        self.wheel_data = bytearray(cmb.WHEEL_NEUTRAL)

    def setup_wheel(self):
        try:
            self.emulated_controller_fd = open(VWHEELDEVICE, "rb+", buffering=0)
            logging.info("Found suitable HID device")
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
        logging.debug(self.wheel_data.hex())
        self.emulated_controller_fd.write(self.wheel_data)

    # Only emulating inputs as Required - Initially probably
    # Steering, Accelerator , gears (fwd/reverse) and maybe handbrake

    def steering(self, angle):

        tmp = 128 - (angle*STEERING_SENSITIVITY)
        #Limits
        if tmp > 250:
            tmp=250
        if tmp < 10: 
            tmp=10

        wheel_value = int(tmp * (cmb.STEER_MAX / 256))
        logging.info(wheel_value)
        self.wheel_data[cmb.WHEEL_WHEEL_HIGHBYTE] = int(wheel_value / 256)
        self.wheel_data[cmb.WHEEL_WHEEL_LOWBYTE] = wheel_value % 256

    #All calibration of how hard to press is a level up this time
    def accelerator(self, pressure):
        self.wheel_data[cmb.WHEEL_ACCELERATEBYTE] = 255 - (pressure % 256)
        logging.debug(pressure%256)

    def reset(self):
        self.wheel_data = bytearray(cmb.WHEEL_NEUTRAL)
        self.send()
        
    def gear(self, input):
        # Using -1 as reverse otherwise 1
        # Assumign Manual Sequential box

        c = cmb.WHEEL_GEARDOWN
        t = cmb.WHEEL_GEARUP
        buttons = [c, c, c, c, t, t]
        # Change down
        for button in buttons:
            self.wheel_data[button[0]] |= button[1]
            self.send()
            time.sleep(0.2)
            self.wheel_data[button[0]] &= ~button[1]
            self.send()
            time.sleep(0.2)

        # Up twice
        if input > 0:
            buttons = [t, t]
            for button in buttons:
                self.wheel_data[button[0]] |= button[1]
                self.send()
                time.sleep(0.2)
                self.wheel_data[button[0]] &= ~button[1]
                self.send()
                time.sleep(0.2)

    def brake(self):
        button = cmb.WHEEL_SQUARE;
        self.wheel_data[button[0]] |= button[1]

       

    #A Momentary push of n milliseconds
    def _push_button(self,button,millis):
        self.reset()

        self.wheel_data[button[0]] |= button[1]
        for h in range(0,int(millis/100)):
            self.send()
            time.sleep(0.1)
        
        self.reset()
        self.send()

    #Dpad encoding is different as only one duirection at a time
    def _push_dpad(self,button,millis):
        self.reset()
        self.wheel_data[button[0]] &= ~cmb.WHEEL_DPAD_MASK
        self.wheel_data[button[0]] |= button[1]
        for h in range(0,int(millis/100)):
            self.send()
            time.sleep(0.1)
        
        self.reset()
        self.send()


    def configure_steam(self):
        print("This is an interactive setup for Steam as a Controller")
        print("In steam go to the page to configure a new controller have gets to to press keys")
        input("Press Enter  when ready")
       
        for b in cmb.STEAM_BUTTON_MAPPINGS:
            self._push_button(b,200)
            time.sleep(0.2)

        for b in cmb.STEAM_DPAD_MAPPINGS:
            self._push_dpad(b,200)
            time.sleep(0.2)
        
        for x in range(0,30):
            self.steering(x)
            self.send()
            time.sleep(0.02)
  
        #Timing matters in this part
        self.reset()
        self.send()
        
        time.sleep(0.2)
        for x in range(128,255,4):
            vwheel.accelerator(x);
            vwheel.send();
            time.sleep(0.02)

        self.reset()
        self.send();

        time.sleep(0.2)
        for b in cmb.STEAM_BUTTONS2_MAPPINGS:
            self._push_button(b,200)
            time.sleep(0.2)
        self.reset()    
        self.send();
        time.sleep(0.5)
        self._push_button(cmb.WHEEL_TRIANGLE,200)

    

if __name__ == "__main__":

    print("Testing class VirtualWheel standalone")
    vwheel = VirtualWheel()
   
    vwheel.setup_wheel()
    #vwheel.configure_steam()
    
    vwheel.accelerator(160)
    while True:
        for x in range(-30,30):
            vwheel.steering(x)
            vwheel.send()
            time.sleep(0.02)
        for x in range(30,-30,-1):
            vwheel.steering(x)
            vwheel.send()
            time.sleep(0.02)



# This class if very specific to a Pi 4 / Pi Zero
# You need to run the define_controller script to set up the virtual device
# Each time you boot

import sys

# Keeing this independant of the underlying game were possible

# 2 Bytes, first 13 bits are buttons then 3 padding bits
# 1 byte 4  bits HAT (includes diagonal directions, 4 bits padding
# 4 bytes X Y Z RZ. analoge 0-255

GAMEPAD_TRIANGLE = (0, 0x08)
GAMEPAD_CIRCLE = (0, 0x04)
GAMEPAD_CROSS = (0, 0x02)
GAMEPAD_SQUARE = (0, 0x01)

GAMEPAD_DPAD_MASK = 0x0F


GAMEPAD_DPAD_U = (2, 0x00)
GAMEPAD_DPAD_R = (2, 0x02)
GAMEPAD_DPAD_D = (2, 0x04)
GAMEPAD_DPAD_L = (2, 0x06)


GAMEPAD_PSMENU = (1, 0x10)
GAMEPAD_SELECT = (1, 0x01)
GAMEPAD_START = (1, 0x02)

GAMEPAD_LJOY_BUTTON = (1, 0x04)
GAMEPAD_RJOY_BUTTON = (1, 0x08)
GAMEPAD_L1 = (0, 0x10)
GAMEPAD_R1 = (0, 0x20)
GAMEPAD_L2 = (0, 0x40)
GAMEPAD_R2 = (0, 0x80)
#All AXIS are 8 bits


JOY_AXIS_MID = 0x7F

GAMEPAD_RTRIGGER = 18
GAMEPAD_LTRIGGER = 17

GAMEPAD_LJOY_X = 3
GAMEPAD_LJOY_Y = 4
GAMEPAD_RJOY_Z = 5
GAMEPAD_RJOY_ZR = 6
CONTROLLER_NEUTRAL = [0x00, 0x00,GAMEPAD_DPAD_MASK, JOY_AXIS_MID,JOY_AXIS_MID,JOY_AXIS_MID,JOY_AXIS_MID]





from pprint import pprint
import logging
import time

VPSDEVICE = "/dev/hidg0"
STEERING_SENSITIVITY = 9 

class VirtualPS(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.emulated_controller_fd = None
        self.PS_data = bytearray(CONTROLLER_NEUTRAL)

    def setup_PS(self):
        try:
            self.emulated_controller_fd = open(VPSDEVICE, "rb+", buffering=0)
            logging.info("Virtual PS Controller ready.")
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
        #logging.debug(self.PS_data.hex())
        self.emulated_controller_fd.write(self.PS_data)

    # Input range from -100 to 100
    def steering(self,angle):
      
        val = int((angle * JOY_AXIS_MID)/100 + JOY_AXIS_MID)
        self.PS_data[GAMEPAD_LJOY_X] = int(val )
        logging.debug(''.join(format(x, '02x') for x in self.PS_data) )
        self.send()



    # Pressure is -100 to 100
    def accelerator(self, pressure):
        pressure = -pressure
        value = int(JOY_AXIS_MID + (pressure*JOY_AXIS_MID)/100)

        self.PS_data[GAMEPAD_RJOY_Z] = int(value)

        #logging.debug(pressure%256)

    def reset(self):
        self.PS_data = bytearray(CONTROLLER_NEUTRAL)
        self.send()
        

    #A Momentary push of n milliseconds
    def _push_button(self,button,millis):
        self.reset()

        self.PS_data[button[0]] |= button[1]
        for h in range(0,int(millis/100)):
            self.send()
            time.sleep(0.1)
        
        self.reset()
        self.send()

    #Dpad encoding is different as only one duirection at a time
    def _push_dpad(self,button,millis):
        self.reset()
        self.PS_data[button[0]] &= ~GAMEPAD_DPAD_MASK
        self.PS_data[button[0]] |= button[1]
        for h in range(0,int(millis/100)):
            self.send()
            time.sleep(0.1)
        
        self.reset()
        self.send()


  
    

if __name__ == "__main__":

    print("Testing class VirtualPS standalone")
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)d -  %(threadName)s %(message)s')
     
    vPS = VirtualPS()
    vPS.setup_PS()

    #vPS.configure_steam()
    if len(sys.argv) > 1 and sys.argv[1] == "configure":
        while True:
            d = input("Type a direction (f,b,l,r) to test, or 'exit' to quit: ")
            logging.info("You typed: "+ d)
            if d == "exit":
                break
            elif d == "f":
                vPS.accelerator(100)
                vPS.send()
                time.sleep(1)
                vPS.reset()
            elif d == "b":
                vPS.accelerator(-100)
                vPS.send()
                time.sleep(1)
                vPS.reset()
            elif d == "l":
                vPS.steering(-100)
                vPS.send()
                time.sleep(1)
                vPS.reset()
            elif d == "r":   
                vPS.steering(100)
                vPS.send()
                time.sleep(1)
                vPS.reset()
               
            else:
                print("Unknown command")
    else:
    #100% left to 100% right and 100% accelerate to 100% brake/reverse]
        vPS.accelerator(0)
        while True:
            for x in range(-100,100):
                vPS.steering(x)

                vPS.send()
                time.sleep(0.01)
            for x in range(100,-100,-1):
                vPS.steering(x)

                vPS.send()
                time.sleep(0.01)


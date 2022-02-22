""" 
Python Class to Create a steeing Wheel from
a Game controller and a Bicycle on a Turbo Trainer
This is actually a rewrite targeting Forza Horizons 4 but
With ease of configuration for other games.
#Adding support for TheCrew back in

It's quite specific for what I want in terms of devices
mapping and behaviour - not as a generic class

Simplifying compared to PS3 version as can use Keyboard for control too
so dont need to map a real controller through.

Also Using Bluetooth for Bike speed (XOSS sensor and Steering rather than i2c)

"""


__author__ = "John Page"
__copyright__ = "Copyright 2021 John Page <johnlpage@gmail.com>"
__license__ = "GPLv3-or-later"
__email__ = "johnlpage@gmail.com"
__version__ = "2.1"

import time
import logging
from gamebike.handlebar import Handlebar
from gamebike.speedsensor import WheelSpeedSensor
from gamebike.telemetry import Telemetry
from gamebike.resistance import Resistance
from gamebike.wheelcontroller import VirtualWheel
from gamebike.control import Clicker

SPEEDGRACE = 1.5
PEDALRATE = 220
PEDALNEUTRAL = 135
WHEEL_MULTIPLIER=2.21

class GameBike(object):
    def __init__(self):

        logging.basicConfig(level=logging.INFO)
        
        logging.info("Controller")
        self.gamecontroller = VirtualWheel()
        self.gamecontroller.setup_wheel()

        logging.info("Wheel Speed")
        self.speedsensor = WheelSpeedSensor()
        rpm = self.speedsensor.getRPM()
        logging.info("Telemetry")
        self.telemetry = Telemetry()
       
        logging.info("Resistance")
        self.resistance = Resistance()
        self.resistance.set_resistance(0)
        self.prevresistance = -1
        self.clicker = Clicker()
        self.pedalpressure = 128
        self.braking = False
        logging.info("Handlebar")
        self.handlebar = Handlebar()
        dir = self.handlebar.getSteer()  

    def start_controller(self):
        logging.info("Starting ...")
        
        self.handlebar.calibrate()
 
       
        self.telemetry.read_telemetry()
        logging.info("Awaiting Telemetry")
        while self.telemetry.receiving == False:
           self.telemetry.read_telemetry()
        logging.info(f"Game is {self.telemetry.game} - Ready...")
        self.lastresistance = round(time.time() * 1000)
        gcount=0
        gtotal=0
        while True:
            self.telemetry.read_telemetry()
            dir = self.handlebar.getSteer()
            rpm = self.speedsensor.getRPM()
            
            self.targetspeed = (rpm/60)*WHEEL_MULTIPLIER
            gamespeed = self.telemetry.speedms
          
            #Replace this with somethign MUCH smarter this is just ON if we are too slow
            if gamespeed > self.targetspeed + SPEEDGRACE :
                self.pedalpressure  = PEDALNEUTRAL
                logging.info("Slower")
            elif gamespeed >= 0 and gamespeed < self.targetspeed:
                logging.info("Faster")
                self.pedalpressure = PEDALRATE


            gradient = self.telemetry.gradient
            if gradient <0:
                gradient = 0
            if gradient > 9:
                gradient = 9     
            gcount =gcount+1
            gtotal=gtotal+gradient

         
            logging.info(f"GS:{gamespeed} TS:{self.targetspeed} D:{dir} GD:{gradient}")

       
            #Do not set the resistance as frequently
            now = round(time.time() * 1000)
            if now - self.lastresistance > 200:
                resistance = int(gtotal/gcount)
                if self.prevresistance != resistance:
                    logging.info(f"Setting resistance to {resistance}")
                    self.resistance.set_resistance(int(gtotal/gcount))
                self.lastresistance = now
                self.prevresistance = resistance
                gcount=0
                gtotal=0
           
            control = self.clicker.get_button()
            if control == 1:
                exit()
            if control == 2:
                self.braking = True
            if control == 3:
                self.braking = False
           

            if self.braking:
                self.gamecontroller.accelerator(100)
                self.gamecontroller.brake()
                logging.info("Brake!!")
            else :
                self.gamecontroller.accelerator(int(self.pedalpressure))
               
                #Right button brake
            
            self.gamecontroller.steering(dir)
            self.gamecontroller.send()

            time.sleep(0.05)
           


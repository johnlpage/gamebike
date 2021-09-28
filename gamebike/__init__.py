""" 
Python Class to Create a steeing Wheel from
a Game controller and a Bicycle on a Turbo Trainer
This is actually a rewrite targeting Forza Horizons 4 but
With ease of configuration for other games.

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
from gamebike.wheelcontroller import VirtualWheel

SPEEDGRACE = 1
PEDALRATE = 220
PEDALNEUTRAL = 128
WHEEL_MULTIPLIER=2.5

class GameBike(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.handlebar = Handlebar()
        self.speedsensor = WheelSpeedSensor()
        self.telemetry = Telemetry()
        self.gamecontroller = VirtualWheel()
        self.pedalpressure = 128


    def start_controller(self):
        logging.info("Starting ...")
        
        self.handlebar.calibrate()
 
        self.gamecontroller.setup_wheel()

        while True:
            self.telemetry.read_horizon_telemetry()
            dir = self.handlebar.getSteer()
            rpm = self.speedsensor.getRPM()
            
            self.targetspeed = (rpm/60)*WHEEL_MULTIPLIER
            gamespeed = self.telemetry.speedms
          
            #Replace this with somethign MUCH smarter this is just ON if we are too slow
            if gamespeed > self.targetspeed :
                self.pedalpressure  = PEDALNEUTRAL
            elif gamespeed < self.targetspeed - SPEEDGRACE :
                self.pedalpressure = PEDALRATE

            logging.info(f"GameSpeed:  {gamespeed} Target: {self.targetspeed} Pedal Pressure: {self.pedalpressure} Direction: {dir}, RPM: {rpm}")
            self.gamecontroller.accelerator(int(self.pedalpressure))
            self.gamecontroller.steering(dir)
            self.gamecontroller.send()
            time.sleep(0.05)
           


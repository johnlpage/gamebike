"""
Python Class to Create a steeing XAC from
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
from gamebike.kickr_resistance import KickrResistance
from gamebike.ps_controller import VirtualPS
from gamebike.control import Clicker
import curses

RESISTANCE_SCALE = 4
SPEEDGRACE = 1.5
PEDALRATE = 50
PEDALNEUTRAL = 1
SPEED_MULTIPLIER = 3


class GameBike(object):
    def __init__(self):

        logging.basicConfig(
            level=logging.INFO, format="%(filename)s:%(lineno)d - %(message)s"
        )

        # logging.info("Configuring Virtual Game Controller Device")
        self.gamecontroller = VirtualPS()
        self.gamecontroller.setup_PS()

        logging.debug("Configuring Speed Sensor")
        self.speedsensor = WheelSpeedSensor()
        rpm = self.speedsensor.getRPM()

        self.telemetry = Telemetry()

        logging.debug("Configuring KICKR Resistance")
        self.resistance = KickrResistance()
        self.resistance.set_resistance(0)
        self.prevresistance = -1

        self.clicker = Clicker()
        self.pedalpressure = 0
        self.braking = False

        logging.debug("Configuring Steering controls")
        self.handlebar = Handlebar()
        self.handlebar.getSteer()

        logging.debug("Setup complete. Starting main loop")

    def report(self, dir):
        logging.info(f"dir:{dir} gamespeed: { self.telemetry.speedms} speed:{self.targetspeed}")

    def start_controller(self):

        self.telemetry.read_telemetry()

        while self.telemetry.receiving == False:
            logging.info("Awaiting Telemetry")
            self.telemetry.read_telemetry()
            time.sleep(1)

        # logging.info(f"Game is {self.telemetry.game} - Ready...")
        self.lastresistance = round(time.time() * 1000)
        gcount = 0
        gtotal = 0
        # self.stdscr = curses.initscr()
        # self.stdscr.clear()
        while True:
            self.telemetry.read_telemetry()
            dir = self.handlebar.getSteer()
            rpm = self.speedsensor.getRPM()

            self.targetspeed = (rpm / 60) * SPEED_MULTIPLIER
            gamespeed = self.telemetry.speedms

            # Replace this with somethign MUCH smarter this is just ON if we are too slow
            if gamespeed > self.targetspeed + SPEEDGRACE:
                self.pedalpressure = PEDALNEUTRAL
                logging.debug("Slower")
            elif gamespeed >= 0 and gamespeed < self.targetspeed:
                logging.debug("Faster")
                self.pedalpressure = PEDALRATE

            gradient = self.telemetry.gradient
            if gradient < 0:
                gradient = 0
            if gradient > 9:
                gradient = 9
            gcount = gcount + 1
            gtotal = gtotal + gradient

            logging.debug(f"")

            # Do not set the resistance as frequently
            now = round(time.time() * 1000)
            if now - self.lastresistance > 200:
                resistance = int(gtotal / gcount)
                if self.prevresistance != resistance:
                    logging.info(f"Setting resistance to {resistance}")
                    self.resistance.set_resistance(int(gtotal / gcount) * RESISTANCE_SCALE)
                self.lastresistance = now
                self.prevresistance = resistance
                gcount = 0
                gtotal = 0

            control = self.clicker.get_button()
            if control == 1:
                logging.info("Exit")
                exit()
            if control == 2:
                self.braking = True
                logging.info("Brake on")
            if control == 3:
                self.braking = False
                logging.info("Brake off")
            

            if self.braking:
                self.gamecontroller.accelerator(-50)
            else:
                self.gamecontroller.accelerator(int(self.pedalpressure))

            self.gamecontroller.steering(dir)
            self.gamecontroller.send()
            self.report(dir)

            time.sleep(0.05)

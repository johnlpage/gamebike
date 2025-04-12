#!/usr/bin/python

# Code to Read an XOSS BLE wheel power sensor up to provide sepped data
# Code is specific to my hardware but shodul be easy to adapt.

from bluepy.btle import Scanner, Service, Characteristic, DefaultDelegate, Peripheral
from pprint import pprint
import logging
import time
import struct

"""
            '0000180a-0000-1000-8000-00805f9b34fb', //Device Information
            '00001816-0000-1000-8000-00805f9b34fb', // Cycling power & Cadence
            '00001818-0000-1000-8000-00805f9b34fb', // Cycling Power
            '00001826-0000-1000-8000-00805f9b34fb', // Fitness Machine
"""

# This is Cycling Power
SERVICEUUID = "00001818-0000-1000-8000-00805f9b34fb"
# This is the power measurement characteristic
CHARUUID  = '00002aa6-0000-1000-8000-00805f9b34fb'
DEVICENAME = "KICKR"
STALELIMIT = 4


class NotifyDelegate(DefaultDelegate):
    def __init__(self, powersensor):
        DefaultDelegate.__init__(self)
        self.parent_powersensor = powersensor

    def handleNotification(self, cHandle, data):
        logging.debug(data)
        self.parent_powersensor.calcPowerFromData(data)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass


class WheelpowerSensor(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.powersensor = None
        self.Power = 0
        self.prevCumulativeCrankRev = 0
        self.prevCrankTime = 0
        self.prevCrankStaleness = 0

    def set_resistance(self, resistance):
        if self.device == None:
            self.find_powersensor()

        if self.device != None and self.powersensor == None:
            self.connect_to_powersensor()

        try:
            while self.powersensor.waitForNotifications(0.01):
                logging.debug("Read sensor")
                pass

        except Exception as e:
            logging.error(e)
            self.powersensor = None
        pass

    def find_powersensor(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        self.device = None
        while self.device == None:
            logging.info("Scanning for KICKR Sensor")
            try:
                devices = scanner.scan(2.0)
                for dev in devices:
                    for (adtype, desc, value) in dev.getScanData():
                        if 'ame' in desc:
                            logging.info(f"{desc} {value}")

                        if DEVICENAME in value:
                            logging.info(vars(dev))
                            self.device = dev
            except Exception as e:
                #logging.error(e)
                time.sleep(1)

        logging.info("Found a wheel power sensor")
        return

    def connect_to_powersensor(self):
        if self.device == None:
            return

        self.powersensor = None
        while self.powersensor == None:
            logging.info("Tying to connect to power sensor")
            try:
                self.powersensor = Peripheral(self.device)
                logging.info("Connected to power sensor")
            except Exception as e:
                #logging.error(e)
                time.sleep(1)

        try:
            services = self.powersensor.getServices()
        except Exception as e:
            logging.error(e)
            self.powersensor = None
            return
            # Bluetooth LE breaks a lot :-(

        self.powersensor.setDelegate(NotifyDelegate(self))
        try:
            logging.info("Looking for power sensor service")
            powersensorService = self.powersensor.getServiceByUUID(SERVICEUUID)
            logging.info(vars(powersensorService))
            logging.info("Found power sensor service")
            logging.info("Looking for power sensor characteristics")
            motionCharacteristics = powersensorService.getCharacteristics(
                forUUID=CHARUUID
            )
            configHandle = motionCharacteristics[0].getHandle() + 1
            # This wasn't obvious - you need to write to enable notification
            self.powersensor.writeCharacteristic(configHandle, b"\x01\x00")
            logging.info("Subscribed to rotation notifications")
            return
        except Exception as e:
            logging.error("powersensor is missing required services?!")
            logging.error(e)
            try:
                self.powersensor.disconnect()
            except:
                logging.error("Was unable to disconnect!")
            self.powersensor = None

    def getPower(self):
        if self.device == None:
            self.find_powersensor()

        if self.device != None and self.powersensor == None:
            self.connect_to_powersensor()

        try:
            while self.powersensor.waitForNotifications(0.01):
                logging.debug("Read sensor")
                pass

        except Exception as e:
            logging.error(e)
            self.powersensor = None

        return self.Power

    #Smooth out?
    def calcPowerFromData(self, data):
        flags = int.from_bytes(data[0:2], "little")
        instant_power = int.from_bytes(data[2:4], "little")
        self.Power = instant_power


    def OldSalcPowerFromData(self, data):
        cumulativeCrankRev = int.from_bytes(data[1:3], "little")
        lastCrankTime = int.from_bytes(data[5:7], "little")

        deltaRotations = cumulativeCrankRev - self.prevCumulativeCrankRev
        if deltaRotations < 0:
            deltaRotations += 65535

        timeDelta = lastCrankTime - self.prevCrankTime
        if timeDelta < 0:
            timeDelta += 65535

        logging.debug(f"rotations: {deltaRotations} timedelta: {timeDelta}ms")
        # If cadence drops we use pref Power up for to 4 seconds

        if timeDelta != 0:
            self.prevCrankStaleness = 0
            self.Power = (deltaRotations / timeDelta) * (60000)
            # Power not Powers
            if self.Power > 500:
                self.Power = 0  # First reading can be crazy high
            self.prevPower = self.Power
            logging.debug(f"computed Power: {self.Power}")

        elif timeDelta == 0 and self.prevCrankStaleness < STALELIMIT:
            self.Power = self.prevPower
            self.prevCrankStaleness += 1
        elif self.prevCrankStaleness >= STALELIMIT:
            self.Power = 0

        self.prevCumulativeCrankRev = cumulativeCrankRev
        self.prevCrankTime = lastCrankTime


if __name__ == "__main__":

    print("Testing wheel power sensor class standalone")
    wsensor = WheelpowerSensor()

    while True:
        Power = wsensor.set_resistance(50);
        logging.info(f"Power Reading: {Power}")
        time.sleep(1)

#!/usr/bin/python

# Code to Read an XOSS BLE wheel speed sensor up to provide sepped data
# Code is specific to my hardware but shodul be easy to adapt.

from bluepy.btle import Scanner, Service, Characteristic, DefaultDelegate, Peripheral
from pprint import pprint
import logging
import time
import struct

# This is standard Rotation sensor bluetooth UUID
SERVICEUUID = "00001816-0000-1000-8000-00805f9b34fb"
# This is the standard notify characteristic UUID
CHARUUID = "00002a5b-0000-1000-8000-00805f9b34fb"
DEVICENAME = "XOSS S-"
STALELIMIT = 4


class NotifyDelegate(DefaultDelegate):
    def __init__(self, speedsensor):
        DefaultDelegate.__init__(self)
        self.parent_speedsensor = speedsensor

    def handleNotification(self, cHandle, data):
        logging.debug(data)
        self.parent_speedsensor.calcRPMFromData(data)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass


class WheelSpeedSensor(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.speedsensor = None
        self.rpm = 0
        self.prevCumulativeCrankRev = 0
        self.prevCrankTime = 0
        self.prevCrankStaleness = 0

    def find_speedsensor(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        self.device = None
        while self.device == None:
            logging.info("Scanning for Speed Sensor")
            devices = scanner.scan(2.0)
            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    if "ame" in desc:
                        logging.info(f"{desc} {value}")
             
                    if DEVICENAME in value:
                        self.device = dev
        logging.info("Found a wheel speed sensor")
        return

    def connect_to_speedsensor(self):
        if self.device == None:
            return

        self.speedsensor = None
        while self.speedsensor == None:
            logging.info("Tying to connect to speed sensor")
            try:
                self.speedsensor = Peripheral(self.device)
                logging.info("Connected to speed sensor")
            except Exception as e:
                logging.error(e)
                time.sleep(1)

        try:
            services = self.speedsensor.getServices()
        except Exception as e:
            logging.error(e)
            self.speedsensor = None
            return
            # Bluetooth LE breaks a lot :-(

        self.speedsensor.setDelegate(NotifyDelegate(self))
        try:
            speedsensorService = self.speedsensor.getServiceByUUID(SERVICEUUID)
            motionCharacteristics = speedsensorService.getCharacteristics(
                forUUID=CHARUUID
            )
            configHandle = motionCharacteristics[0].getHandle() + 1
            # This wasn't obvious - you need to write to enable notification
            self.speedsensor.writeCharacteristic(configHandle, b"\x01\x00")
            logging.info("Subscribed to rotation notifications")
            return
        except Exception as e:
            logging.error("speedsensor is missing required services?!")
            logging.error(e)
            try:
                self.speedsensor.disconnect()
            except:
                logging.error("Was unable to disconnect!")
            self.speedsensor = None

    def getRPM(self):
        if self.device == None:
            self.find_speedsensor()

        if self.device != None and self.speedsensor == None:
            self.connect_to_speedsensor()

        try:
            while self.speedsensor.waitForNotifications(0.01):
                logging.debug("Read sensor")
                pass

        except Exception as e:
            logging.error(e)
            self.speedsensor = None

        return self.rpm

    def calcRPMFromData(self, data):
        cumulativeCrankRev = int.from_bytes(data[1:3], "little")
        lastCrankTime = int.from_bytes(data[5:7], "little")

        deltaRotations = cumulativeCrankRev - self.prevCumulativeCrankRev
        if deltaRotations < 0:
            deltaRotations += 65535

        timeDelta = lastCrankTime - self.prevCrankTime
        if timeDelta < 0:
            timeDelta += 65535

        logging.debug(f"rotations: {deltaRotations} timedelta: {timeDelta}ms")
        # If cadence drops we use pref RPM up for to 4 seconds

        if timeDelta != 0:
            self.prevCrankStaleness = 0
            self.rpm = (deltaRotations / timeDelta) * (60000)
            # RPM not RPms
            if self.rpm > 500:
                self.rpm = 0  # First reading can be crazy high
            self.prevRPM = self.rpm
            logging.debug(f"computed RPM: {self.rpm}")

        elif timeDelta == 0 and self.prevCrankStaleness < STALELIMIT:
            self.rpm = self.prevRPM
            self.prevCrankStaleness += 1
        elif self.prevCrankStaleness >= STALELIMIT:
            self.rpm = 0

        self.prevCumulativeCrankRev = cumulativeCrankRev
        self.prevCrankTime = lastCrankTime


if __name__ == "__main__":

    print("Testing wheel speed sensor class standalone")
    wsensor = WheelSpeedSensor()

    while True:
        rpm = wsensor.getRPM()
        logging.info(f"RPM: {rpm}")
        time.sleep(1)

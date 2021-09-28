#!/usr/bin/python

# Code to Read an Arduino 33 BLE set up to provide acceleration data for steering
# Code goes with associateed Arduino Sketch handlebar.ino

from bluepy.btle import Scanner, Service, Characteristic, DefaultDelegate, Peripheral
from pprint import pprint
import struct
import math
import logging
import time


DEVICENAME = "InternetThing"
SERVICEUUID = "90db"
CHARUUID = "d0c5"
values = ["ax", "ay", "az", "gx", "gy", "gz", "mx", "my", "mz"]
scale = [1000, 1000, 1000, 2, 2, 2, 100, 100, 100]
DIRVAL = "mx"


class NotifyDelegate(DefaultDelegate):
    def __init__(self, handlebar):
        DefaultDelegate.__init__(self)
        self.parent_handlebar = handlebar

    def handleNotification(self, cHandle, data):
        rec = {}
        c = 0
        for valname in values:
            value = int.from_bytes(data[c * 2 : c * 2 + 2], "little")
            if value > 0:
                rec[valname] = (value - 5000) / scale[c]
            c = c + 1
        logging.debug(rec)
        self.parent_handlebar.data = rec


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass


class Handlebar(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.forwards = 0
        self.handlebar = None
        self.last_direction = None

    def find_handlebar(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        self.device = None
        while self.device == None:
            logging.info("Scanning")
            devices = scanner.scan(2.0)
            logging.info("Scan Complete")

            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    logging.debug(f"{desc} {value}")
                    if DEVICENAME in value:
                        self.device = dev
        logging.info("Found a handlebar")
        return

    def connect_to_handlebar(self):
        if self.device == None:
            return

        self.handlebar = None
        while self.handlebar == None:
            logging.info("Tying to connect to handlebar")
            try:
                self.handlebar = Peripheral(self.device)
                logging.info("Connected")
            except Exception as e:
                logging.error(e)
                time.sleep(1)

        try:
            services = self.handlebar.getServices()
        except Exception as e:
            logging.error(e)
            self.handlebar = None
            return
            # Bluetooth LE breaks a lot :-(

        self.handlebar.setDelegate(NotifyDelegate(self))
        try:
            handlebarService = self.handlebar.getServiceByUUID(SERVICEUUID)
            motionCharacteristics = handlebarService.getCharacteristics(
                forUUID=CHARUUID
            )
            configHandle = motionCharacteristics[0].getHandle() + 1
            # This wasn't obvious - you need to write to enable notification
            self.handlebar.writeCharacteristic(configHandle, b"\x01\x00")
            logging.info("Subscribed to Gyro notifications")
            return
        except Exception as e:
            logging.error("handlebar is missing required services?!")
            logging.error(e)
            try:
                self.handlebar.disconnect()
            except:
                logging.error("Was unable to disconnect!")
            self.handlebar = None

    def getDirection(self):
        if self.device == None:
            self.find_handlebar()

        if self.device != None and self.handlebar == None:
            self.connect_to_handlebar()

        try:
            while self.handlebar.waitForNotifications(0.01):
                logging.debug("Read sensor")
                mx = self.data.get("mx", None)
                my = self.data.get("my", None)
                if mx != None and my != None:
                    self.last_direction = math.atan2(mx, my) * 57.29

        except Exception as e:
            logging.error(e)
            self.handlebar = None

        return self.last_direction

    def calibrate(self):
        dir = self.getDirection()
        logging.info("Calibrating Handlebars")
        tries = 20
        count = 0
        sum = 0
        while count < tries:
            dir = self.getDirection()
            if dir != None:
                sum = sum + dir
                time.sleep(0.2)
                count += 1
        self.forwards = sum / count
        logging.info(self.forwards)

    def getSteer(self):
        dir = self.getDirection()
        return int(dir - self.forwards)


if __name__ == "__main__":

    print("Testing classs handlebar standalone")
    hbar = Handlebar()

    while True:
        dir = hbar.getDirection()
        logging.info(dir)
        time.sleep(0.1)

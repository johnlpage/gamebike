#!/usr/bin/python

# Code to Read an Arduino 33 BLE set up to provide acceleration data for steering
# Code goes with associateed Arduino Sketch handlebar.ino

from bluepy.btle import Scanner, Service, Characteristic, DefaultDelegate, Peripheral
from pprint import pprint
import struct
import math
import logging
import time
import bluepy.btle as btle

DEVICENAME = "Handlebar"
SERVICEUUID = "4a9d"
CHARUUID = "ba75"
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
        if isNewDev:
            # print (f"Discovered device { dev.addr } ")
            pass
        elif isNewData:
            # print (f"Received new data from {dev.addr}")
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
            logging.info("Scanning for Handlebar")
            devices = scanner.scan(3.0, passive=False)

            for dev in devices:
               
                if dev.getValueText(255) == "4a4f484e50424152":  # JOHNPBAR
                    logging.info(vars(dev))
                    self.device = dev
            time.sleep(1)

        logging.info("Found steeing control (handlebar")
        return

    def connect_to_handlebar(self):
        if self.device == None:
            return

        self.handlebar = None
        while self.handlebar == None:
            logging.info("Tying to connect to handlebar")
            try:
                self.handlebar = Peripheral(self.device, btle.ADDR_TYPE_PUBLIC)
                logging.info("Connected")
            except Exception as e:
                logging.error(e)
                time.sleep(5)

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
            mx = None
            my = None
            while self.handlebar.waitForNotifications(0.025):
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

        if dir:
            offset = dir - self.forwards
            if offset > 180:
                offset = offset - 360

            # dead zone
            if -2 <= offset <= 2:
                return 0
            return offset
        else:
            return 0


if __name__ == "__main__":

    print("Testing classs handlebar standalone")
    hbar = Handlebar()

    while True:
        dir = hbar.getDirection()
        logging.info(dir)
        time.sleep(0.1)

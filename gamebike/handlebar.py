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
        self.parent_handlebar.data = rec


class Handlebar(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.forwards = 0
        self.handlebar = None
        self.last_direction = None
   
        self.ready = False
        self.faults = 0

    def find_handlebar(self):

        scanner = Scanner()
        self.device = None
        count = 5
        logging.debug("Scanning for Handlebar")
        while count > 0 and self.device == None:
            count = count - 1
            try:
                devices = scanner.scan(2.0, passive=False)
                for dev in devices:
                    if dev.getValueText(255) == "4a4f484e50424152":  # JOHNPBAR
                        self.device = dev
                        logging.debug("Found handlebar: " + dev.addr)
                        
            except Exception as e:
                logging.debug("Error scanning for handlebar: " + str(e))
                pass
        
        return

    def connect_to_handlebar(self):
        self.ready = False
        if self.device == None:
            return

        self.handlebar = None
        count = 5
        logging.debug("Tying to connect to handlebar")
        while count > 0 and self.handlebar == None:
            count = count - 1
            try:
                self.handlebar = Peripheral(self.device)
            except Exception as e:
                logging.debug(e)
                time.sleep(1)
                pass

        if self.handlebar != None:
            self.handlebar.setDelegate(NotifyDelegate(self))
            try:
                handlebarService = self.handlebar.getServiceByUUID(SERVICEUUID)
                motionCharacteristics = handlebarService.getCharacteristics(
                    forUUID=CHARUUID
                )
                configHandle = motionCharacteristics[0].getHandle() + 1
                # This wasn't obvious - you need to write to enable notification
                self.handlebar.writeCharacteristic(configHandle, b"\x01\x00")
                logging.info("Handlebar steering connected")
                self._calibrate()
              
                self.ready = True
                return True
            except Exception as e:
                logging.error(e)
                try:
                    self.handlebar.disconnect()
                except:
                    logging.error("Was unable to disconnect!")
                self.handlebar.disconnect()
                self.handlebar = None
                self.ready = False

       
        return False

    def getDirection(self):

        #Find Device
        if self.device == None:
            self.find_handlebar()
            return

        #Connect Device
        if self.handlebar == None:
           self.connect_to_handlebar()
           return
        
        #Ready means device connected and OK
        if self.ready:
            try:
                mx = None
                my = None
                while self.handlebar != None and self.handlebar.waitForNotifications(0.025):
                    mx = self.data.get("mx", None)
                    my = self.data.get("my", None)
                if mx != None and my != None:
                    self.last_direction = math.atan2(mx, my) * 57.29
            except Exception as e:
                logging.info(e)
                self.handlebar = None
                self.ready = False
               
                    

        return self.last_direction

        

    def _calibrate(self):
        logging.info("Calibrating Handlebars")
        tries = 6
        count = 0
        sum = 0
        while count < tries:
            mx = None
            my = None
            try:
                while self.handlebar.waitForNotifications(0.025):
                    mx = self.data.get("mx", None)
                    my = self.data.get("my", None)
                if mx != None and my != None:
                    dir = math.atan2(mx, my) * 57.29
                    if dir != None:
                        sum = sum + dir
                        count += 1
                    time.sleep(0.25)
            except Exception as e:
                logging.error(f"Calibration failed {e}")
                self.handleBar = None
                return
        logging.info("Handlebar Calibration complete")
        self.forwards = sum / count


    def getSteer(self):
        dir = self.getDirection()
        if dir:
            offset = dir - self.forwards
            if offset > 180:
                offset = offset - 360
            # dead zone
            if -2 <= offset <= 2:
                return 0
            return -offset
        else:
            return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)d -  %(threadName)s %(message)s')
        
    print("Testing classs handlebar standalone")
    hbar = Handlebar()

    while True:
        dir = hbar.getSteer()
        if dir:
            logging.info(dir)
        time.sleep(1)

#!/usr/bin/python

# Code to Read an XOSS BLE wheel speed sensor up to provide sepped data
# Code is specific to my hardware but shodul be easy to adapt.

from bluepy.btle import Scanner, Service, Characteristic, DefaultDelegate, Peripheral
from pprint import pprint
import logging
import time
import struct
UARTSERVICE_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E";
UART_RX_CHARACTERISTIC_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E";
UART_TX_CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E";

UNPAIREDDEVICENAME = "goput"
PAIREDNAME="BBC micro:bit"
STALELIMIT = 4


class NotifyDelegate(DefaultDelegate):
    def __init__(self, resistance):
        DefaultDelegate.__init__(self)
        self.parent_resistance = resistance

    def handleNotification(self, cHandle, data):
        logging.debug(data)
        self.parent_resistance.calcRPMFromData(data)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        pass


class Resistance(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.unpaired = False
        self.resistance = None
        self.configHandle = None
       

    def find_resistance(self):
        scanner = Scanner().withDelegate(ScanDelegate())
        self.device = None
        while self.device == None:
            logging.info("Scanning")
            devices = scanner.scan(2.0)
            logging.info("Scan Complete")
            self.unpaired = False
            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    if "Name" in desc:
                            logging.info(f"{desc} {value}")
                    if UNPAIREDDEVICENAME in value or PAIREDNAME in value:
                        logging.info(value)
                        self.device = dev
                        if  UNPAIREDDEVICENAME in value:
                            self.unpaired = True
                            print("Device is UNPAIRED!")
        logging.info("Found your microbit ")
        return

    #Horrible logic as microbit, affter adding new code needs re-paired
    #But linux wont re-pair as it thinks it is paired alreadys
    #SO you have try to pair, fail, reconnect, unpair, try to pair again then the device needs
    #manually rebooted so you can connect after pairing (at which point it has different name)
    def connect_to_resistance(self):
        if self.device == None:
            return

        self.resistance = None
        while self.resistance == None:
            logging.info("Tying to connect to resistance device")
            try:
                self.resistance = Peripheral(self.device)
                logging.info("Connected :-)")
            except Exception as e:
                logging.error(e)
                time.sleep(1)

        if self.unpaired:
            try:
                self.resistance.pair()
                logging.info("PAIR SUCEEDED ... sleeping")
                time.sleep(5)
                self.resistance.disconnect()
                logging.info("Disconnecting")
                self.resistance = None
                self.device=None
                return
            except Exception as e:
                logging.error(e)
                try:
                    self.resistance = Peripheral(self.device)
                    self.resistance.unpair()
                except:
                    pass
               
                self.resistance = None
                self.device=None
                time.sleep(5)
                return;
                    

        
        try:
            services = self.resistance.getServices()
        except Exception as e:
            logging.error("Cannot list services")
            logging.error(e)
            self.resistance = None
            # Bluetooth LE breaks a lot :-(

       

        try:
            logging.info("Getting Service Handle")
            resistanceService = self.resistance.getServiceByUUID(UARTSERVICE_SERVICE_UUID)
            logging.info("Getting Characteristic Handles")
            self.rxcharacteristics = resistanceService.getCharacteristics(forUUID=UART_TX_CHARACTERISTIC_UUID)
            pprint(self.rxcharacteristics)
            logging.info("Getting write handle")
            self.configHandle = self.rxcharacteristics[0].getHandle()
           
        except Exception as e:
            logging.error("resistance is missing required services?!")
            logging.error(e)
            try:
                self.resistance.disconnect()
                self.resistance = None
                self.device=None
            except:
                logging.error("Was unable to disconnect!")
                self.resistance = None
                self.device=None
            return False;

    def set_resistance(self,newresistance):
        if self.device == None:
            self.find_resistance()

        if self.device != None and self.resistance == None:
            self.connect_to_resistance()

        # This wasn't obvious - you need to write to enable notification
        if self.configHandle:
            try:
                stringversion = f"{newresistance}\n"
                self.resistance.writeCharacteristic(self.configHandle, str.encode(stringversion))
            except Exception as e:
                logging.error(e)
                self.resistance = None

        return


if __name__ == "__main__":

    print("Testing resistance class standalone")
    resistance = Resistance()
    while True:
        for x in range(10):
            resistance.set_resistance(x)
            time.sleep(1)
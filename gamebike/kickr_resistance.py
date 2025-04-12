#!/usr/bin/python

# Code to Read an XOSS BLE wheel power sensor up to provide sepped data
# Code is specific to my hardware but shodul be easy to adapt.

from bluepy.btle import Scanner, Service, Characteristic, DefaultDelegate, Peripheral
from pprint import pprint
import logging
import time
import struct
from pprint import pprint
from struct import unpack



"""

jlp@steampi:~/gamebike/gamebike $ sudo gatttool -b "f2:e5:54:98:07:ac" -t random  --char-write-req --handle=0x2f --value=32EEFC 
Characteristic value was written successfully

jlp@steampi:~/gamebike/gamebike $ sudo gatttool -b "f2:e5:54:98:07:ac" -t random  --char-write-req --handle=0x2f --value=400001
Characteristic value was written successfully
jlp@steampi:~/gamebike/gamebike $ sudo gatttool -b "f2:e5:54:98:07:ac" -t random  --char-write-req --handle=0x2f --value=403FFF
Characteristic value was written successfully


https://github.com/codeinversion/sensors-swift-trainers

       case UNLOCK                     = 32
        case SETRESISTANCEMODE          = 64
        case SETSTANDARDMODE            = 65
        case setErgMode                 = 66
        case setSimMode                 = 67
        case setSimCRR                  = 68
        case setSimWindResistance       = 69
        case SETSIMGRADEMODE                = 70
        case setSimWindSpeed            = 71
        case setWheelCircumference      = 72

           public static func unlockCommand() -> [UInt8] {
        return [
            WahooTrainerSerializer.OperationCode.unlock.rawValue,
            0xee,   // unlock code
            0xfc    // unlock code
        ]
    }
    
    public static func setResistanceMode(_ resistance: Float) -> [UInt8] {
        let norm = UInt16((1 - resistance) * 16383)
        return [
            WahooTrainerSerializer.OperationCode.setResistanceMode.rawValue,
            UInt8(norm & 0xFF),
            UInt8(norm >> 8 & 0xFF)
        ]
    }
    
    public static func setStandardMode(level: UInt8) -> [UInt8] {
        return [
            WahooTrainerSerializer.OperationCode.setStandardMode.rawValue,
            level
        ]
    }

"""
SETRESISTANCEMODE          = 64
SETSTANDARDMODE            = 65
SETSIMGRADEMODE                = 70
# This is Cycling Power
SERVICEUUID = "00001818-0000-1000-8000-00805f9b34fb"
# This is the power measurement characteristic
CHARUUID = "A026E005-0A7D-4AB3-97FA-F1500F9FEB8B"
DEVICENAME = "KICKR"
STALELIMIT = 4


class ReadCharacteristicDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print ("got handle: 0x%x  data: 0x%x" % (cHandle, unpack('>i','\x00'+data)[0]))



class KickrResistance(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.resistance_control = None
        self.Power = 0
        self.ready = False

    def set_resistance(self, resistance):

        if resistance > 1.0:
            resistance = 1.0
        if resistance < 0.0:
            resistance = 0.0
        normal=int(resistance * 16383)

        if self.device == None or self.resistance_control == None or not self.ready:
            self.find_powersensor()
            return

        logging.info(f"Setting resistance to {resistance}")

        packed_bytes = struct.pack('<BH', SETRESISTANCEMODE, normal)
        isSet = False
        count = 5
        while count > 0 and not isSet:
            try:
                count = count - 1
                response = self.controlcharacteristic.write(packed_bytes,withResponse=True)
                isSet = True
            except Exception as e:
                time.sleep(0.2)
                logging.debug(e)

        if not isSet:
            logging.info("KICKR not responding, retrying")
            self.resistance_control = None
            self.ready = False
            return isSet
       

    def find_powersensor(self):

        scanner =  Scanner()
        self.device = None
        logging.debug("Scanning for KICKR SNAP")
        count = 2
        while count > 0 and self.device == None:
            try:
                count = count - 1
                devices = scanner.scan(2.0)
                for dev in devices:
                    for adtype, desc, value in dev.getScanData():   
                        if DEVICENAME in value:
                            logging.debug("Found KICKR SNAP device")
                            self.device = dev
            except Exception as e:
                logging.debug(e)
                pass

        if self.device == None:
            logging.info("KICKR SNAP not found, will retry")
            return

        logging.debug("Connecting to KICKR SNAP.")
        count = 5
        while count > 0 and self.resistance_control == None:
            count=count -1
            try:
                self.resistance_control = Peripheral(self.device)
                logging.debug("Connected to KICKR SNAP.")
                # self.resistance_control.withDelegate(ReadCharacteristicDelegate())
            except Exception as e:
                time.sleep(0.2)

        if  self.resistance_control == None:
            return
    
        service = self.resistance_control.getServiceByUUID(SERVICEUUID);
        self.controlcharacteristic = service.getCharacteristics(CHARUUID)[0]
       
        logging.debug("Unlocking Control of resistance.")
        count = 5
        while count > 0 and not self.ready:
            try:
                self.controlcharacteristic.write(b"\x20\xee\xfc",withResponse=True)
                self.ready = True
                logging.info("KICKR Resistance READY")
            except Exception as e:
                   time.sleep(0.2)
        
        if not self.ready:
            self.resistance_control = None


    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(filename)s:%(lineno)d -  %(threadName)s %(message)s')
    print("Testing KICKR RESISTANCE class standalone")
    kickr = KickrResistance()
    
    while True:
        kickr.set_resistance(0.05)
        time.sleep(1)


    
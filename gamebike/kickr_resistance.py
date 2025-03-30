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




class WheelpowerSensor(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.scanner = None
        self.device = None
        self.powersensor = None
        self.Power = 0

    def set_resistance(self, resistance):

        if self.device == None:
            self.find_powersensor()

        
        if self.device != None and self.powersensor == None:
            self.connect_to_powersensor()
        try:
            logging.info(f"Setting resistance to {resistance}")
            self.powersensor.writeCharacteristic(37, struct.pack("<H", resistance))
        except Exception as e:
            logging.error(e)
            self.powersensor = None
        pass

    def find_powersensor(self):
        scanner = Scanner()
        self.device = None
      
        while self.device == None:
            logging.info("Scanning for KICKR SNAP")
            try:
                devices = scanner.scan(2.0)
                for dev in devices:
                    
                    for adtype, desc, value in dev.getScanData():   
                        if "ame" in desc:
                            logging.info(f"Found {desc} {value}")
                        if DEVICENAME in value:
                            self.device = dev
                            logging.info(vars(dev))
            except Exception as e:
                logging.info(e)
                time.sleep(1)

        logging.info("Found.")

        logging.info("Creatng Peripheral.")
        while self.powersensor == None:
            try:
                self.powersensor = Peripheral(self.device)
                logging.info("Connected.")
                self.powersensor.withDelegate(ReadCharacteristicDelegate())
            except Exception as e:
                time.sleep(1)

        service = self.powersensor.getServiceByUUID(SERVICEUUID);
        self.controlcharacteristic = service.getCharacteristics(CHARUUID)[0]
        logging.info(f"Control characteristic: {self.controlcharacteristic.propertiesToString()} {self.controlcharacteristic.getHandle()}")    
        return

    

if __name__ == "__main__":

    print("Testing KICKR RESISTANCE class standalone")
    wsensor = WheelpowerSensor()
    wsensor.find_powersensor()
    unlocked = False
    logging.info("Unlocking")
    while not unlocked:
        try:
            unlock = wsensor.controlcharacteristic.write(b"\x20\xee\xfc",withResponse=True)
            unlocked = True
        except Exception as e:
                print(e)    
        
    normal = 12000

    while True:
   
      
        packed_bytes = struct.pack('<BH', SETRESISTANCEMODE, normal)
        isSet = False
        while not isSet:
            try:
                response = wsensor.controlcharacteristic.write(packed_bytes,withResponse=True)
                print(f"Response: {response}")
                isSet = True
            except Exception as e:
                print(e)    
        print(f"Setting resistance to {normal} {packed_bytes.hex()} { wsensor.controlcharacteristic.getHandle()}")
        text = input("Enter Resistance ")
        normal = int(text)

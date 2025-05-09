#!/usr/bin/python

# Class to listen to game telemetry so we can map acceleration to speed better

import logging
import time
import struct
from struct import unpack
import socket 

TELEMETRY_IP = "0.0.0.0"
TELEMETRY_PORT = 5005


class Telemetry(object):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.speedms=0.0
        self.gradient=0.0
        self.receiving=False
        self.game = "unknown"
        try:
            self.telemetry_socket = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM  # Internet
            )  # UDP
            self.telemetry_socket.setblocking(0)
            self.telemetry_socket.bind((TELEMETRY_IP, TELEMETRY_PORT))
            logging.info("Opened receiving telemetry socket")


        except Exception as e:
            logging.error("Cannot open receiving telemetry socket")
            logging.error(e)
            self.crew_telemetry_socket = None


                

    def parse_horizon_telemetry(self,data):
        self.receiving = True
        self.game = "horizon4"
        # Just unpack what we want
        self.gradient = float(struct.unpack("<f", data[60: 64])[0])
        #Thats -ve radians for some reason
        self.gradient= self.gradient*-57
        self.speedms = float(struct.unpack("<f", data[256: 260])[0])
            
       

    def parse_thecrew_telemetry(self,data):
        self.receiving = True
        self.game = "thecrew"
        logging.debug(f"Received TheCrew telemetry message: {data}")
        fmt = "IffffffffffffIIII"
        telemetry = unpack(fmt, data)
        telemetry = list(map(lambda x: round(x, 2), telemetry))
        telemetry = {
            "time": telemetry[0],
            "angularVelocity": telemetry[1:4],
            "orientation": telemetry[4:7],
            "acceleration": telemetry[7:10],
            "velocity": telemetry[10:13],
            "position": telemetry[13:16],
            "gameid": telemetry[16],
        }

        self.gradient = telemetry["orientation"][1] * 57
        self.speedms = telemetry["velocity"][1] 


    def read_telemetry(self):
        if self.telemetry_socket == None:
            return False
        try:
            #Eat data until we run out
            while True:
                data, addr = self.telemetry_socket.recvfrom(324)
                if len(data) == 324:
                    self.parse_horizon_telemetry(data)
                if len(data) == 68:
                    self.parse_thecrew_telemetry(data)
        
        except BlockingIOError:
            #logging.debug(f"speed(m/s): {self.speedms:.2} gradient:{self.gradient:.2}")
            pass
        except Exception as e:
            logging.error(f"Odd: {str(e)}")
            pass
            

if __name__ == "__main__":

    print("Testing class Telemetry standalone")
    game_telemetry = Telemetry()

    while True:
        game_telemetry.read_telemetry()

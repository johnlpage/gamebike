#!/usr/bin/python3

import gamebike
import os

if os.geteuid() != 0:
	print("This script must be run as root")
	exit(1)	
	
try:
	bike = gamebike.GameBike()
except Exception as e:
	print(e)
	exit(1)

bike.start_controller ()

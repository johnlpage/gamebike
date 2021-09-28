#!/usr/bin/python3

import gamebike

try:
	bike = gamebike.GameBike()
except Exception as e:
	print(e)
	exit(1)

bike.start_controller ()

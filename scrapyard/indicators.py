import RPi.GPIO as GPIO
def turn_off_all_gpio():
    # Use the BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)
    
    # Get a list of all GPIO pins (BCM mode)
    pins = [4, 5, 6, 12, 13, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
    
    # Set up each pin and turn it off
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    # Clean up the GPIO settings
    GPIO.cleanup()
if __name__ == "__main__":
    turn_off_all_gpio()
    print("All GPIO pins have been turned off.")
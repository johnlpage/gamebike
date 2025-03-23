/*
   A Bluetooth LE enabled Acellerometer/Gyro/Magnetomeoter for the
   Arduino Nano BLE - Exposes one Service with One Characteristic
   That has the info packed 2 bytes per axis as a little endian integer
   Accreleration is 1000-9000 with 0 at 5000 anfd in first 3 bytes
   GYRO and MAG are TODO
*/
#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

// Not an OFFICIAL Service GUID - 90db short for mon9oDB
BLEService dataService("4a9d");

// Not an Official characteristic GUID - short for "docs"
BLECharacteristic movementChar("ba75",                    //16-bit characteristic UUID
                               BLERead | BLENotify, 18);  // remote clients will be able to get notifications if this characteristic changes


long previousMillis = 0;  // Used to keep track of when last reading sent
bool debug = false;       //If I used #define I coudl reduce code size but don't need to for now.

void error_light(int t) {
  while (true) {
    for (int x = 0; x < t; x++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(400);
      digitalWrite(LED_BUILTIN, LOW);
      delay(400);
    }
    // turn the LED on (HIGH is the voltage level)
    delay(1000);
  }
}
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  if (debug) {
    Serial.begin(9600);  // initialize serial communication
    while (!Serial) {}   //Infinite loop if no cable connected so make sure we are NOT in debug
  }


  if (!IMU.begin()) {
    if (debug) Serial.println("Failed to initialize IMU!");
    error_light(2);
    
  }


  // begin initialization
  if (!BLE.begin()) {
    if (debug) Serial.println("starting BLE failed!");
    error_light(3);
    
  }

  /* Set a local name for the BLE device
     This name will appear in advertising packets
     and can be used by remote devices to identify this BLE device
     The name can be changed but maybe be truncated based on space left in advertisement packet
  */
  BLE.setLocalName("SteerBar");
  BLE.setDeviceName("SteerBar");
  byte data[8] = {'J', 'O', 'H', 'N', 'P','B','A','R'};

  BLE.setManufacturerData(data, 5);
  BLE.setAdvertisedService(dataService);        // add the service UUID
  dataService.addCharacteristic(movementChar);  // add the movement characteristic
  BLE.addService(dataService);                  // Add the  service


  /* Start advertising BLE.  It will start continuously transmitting BLE
     advertising packets and will be visible to remote BLE central devices
     until it receives a new connection */

  // start advertising
  BLE.advertise();
  if (debug) Serial.println("Bluetooth device active, waiting for connections...");
}

void loop() {
  // wait for a BLE central
  BLEDevice central = BLE.central();

  // if a central is connected to the peripheral:
  if (central) {
    if (debug) Serial.print("Connected to central: ");
    // print the central's BT address:
    if (debug) Serial.println(central.address());
    // turn on the LED to indicate the connection:
    digitalWrite(LED_BUILTIN, HIGH);

    // check the sensors ever 20ms
    // while the central is connected:
    while (central.connected()) {
      long currentMillis = millis();
      if (currentMillis - previousMillis >= 50) {
        previousMillis = currentMillis;
        updateReadings();
      }
    }

    // when the central disconnects, turn off the LED:
    digitalWrite(LED_BUILTIN, LOW);
    if (debug) Serial.print("Disconnected from central: ");
    if (debug) Serial.println(central.address());
  } else {
    delay(1000);
     digitalWrite(LED_BUILTIN, HIGH);
     delay(400);
     digitalWrite(LED_BUILTIN, LOW);
    

  }
}

void updateReadings() {
  unsigned short value[9];
  float x, y, z;

  for (int i = 0; i < 9; i++) value[i] = 0;  //Zero out - not valid reading

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

    value[0] = x * 1000 + 5000;  //Scaled from 1000 to 9000
    value[1] = y * 1000 + 5000;
    value[2] = z * 1000 + 5000;
  }

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    value[3] = x * 2 + 5000;  //Scaled from 1000 to 9000
    value[4] = y * 2 + 5000;
    value[5] = z * 2 + 5000;
  }


  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(x, y, z);

    value[6] = x * 100 + 5000;  //Scaled from 1000 to 9000
    value[7] = y * 100 + 5000;
    value[8] = z * 100 + 5000;
  }

  if (debug) {
    Serial.println(z);
  }
  movementChar.writeValue(value, 18);  // update the characteristic
}

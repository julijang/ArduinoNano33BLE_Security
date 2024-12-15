#include <ArduinoBLE.h>
#include <Arduino_HS300x.h>
#include <Arduino_APDS9960.h>

#define VALUE_SIZE 20

BLEService temperatureService = BLEService("00000000-5EC4-4083-81CD-A10B8D5CF6EC");
BLECharacteristic temperatureCharacteristic = BLECharacteristic("00000001-5EC4-4083-81CD-A10B8D5CF6EC", BLERead | BLENotify, VALUE_SIZE);
BLEService proximityService = BLEService("00000003-5EC4-4083-81CD-A10B8D5CF6EC");
BLECharacteristic proximityCharacteristic = BLECharacteristic("00000004-5EC4-4083-81CD-A10B8D5CF6EC", BLERead | BLENotify, VALUE_SIZE);


// last temperature reading
int oldTemperature = 0;
// last proximity reading
uint8_t oldProximity = 0;
// last time the temperature was checked in ms
long previousMillis = 0;

void setup() {
  // Initialize serial communication for debugging
  Serial.begin(9600);
  while (!Serial); // Wait for Serial Monitor readiness
  Serial.println("Initializing sensors and BLE...");

  // Initialize the temperature sensor (HS300x)
  if (!HS300x.begin()) {
    Serial.println("Failed to initialize HS300x. Check connections.");
    while (1); // Halt execution if initialization fails
  }
  Serial.println("HS300x initialized successfully.");

  // Initialize the proximity sensor (APDS9960)
  if (!APDS.begin()) {
    Serial.println("Failed to initialize APDS9960. Check connections.");
    while (1); // Halt execution if initialization fails
  }
  Serial.println("APDS9960 initialized successfully.");

  // Initialize the built-in LED pin to indicate when a central is connected
  pinMode(LED_BUILTIN, OUTPUT);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Failed to start BLE. Check configuration.");
    while (1); // Halt execution if BLE initialization fails
  }

  // Set BLE device and service names
  BLE.setLocalName("BLE-TEMP");
  BLE.setDeviceName("BLE-TEMP");

  // Add characteristics to their respective services
  temperatureService.addCharacteristic(temperatureCharacteristic);
  proximityService.addCharacteristic(proximityCharacteristic);

  // Add services to the BLE stack
  BLE.addService(temperatureService);
  BLE.addService(proximityService);

  // Set initial values for characteristics
  temperatureCharacteristic.writeValue("0.0");
  proximityCharacteristic.writeValue("0");

  // Start BLE advertising
  BLE.advertise();
  Serial.println("BLE advertising started. Device is ready for connections.");
}


void loop() {
  // wait for a Bluetooth® Low Energy central
  BLEDevice central = BLE.central();

  // if a central is connected to the peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's BT address:
    Serial.println(central.address());
    // turn on the LED to indicate the connection
    digitalWrite(LED_BUILTIN, HIGH);


    // while the central is connected
    // update temperature & proximity every 200ms
    while (central.connected()) {
      long currentMillis = millis();
      if (currentMillis - previousMillis >= 200) {
        previousMillis = currentMillis;
        updateTemperature();
        updateProximity();
      }
    }

    // turn off the LED after disconnect
    digitalWrite(LED_BUILTIN, LOW);
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

void updateTemperature() {
  float temperature = HS300x.readTemperature();

  if (temperature != oldTemperature) {
    char buffer[VALUE_SIZE];
    int ret = snprintf(buffer, sizeof buffer, "%f", temperature);

    if (ret >= 0) {
      temperatureCharacteristic.writeValue(buffer);
      Serial.print("Temperature: ");
      Serial.println(buffer); // Print to Serial for debugging
      oldTemperature = temperature;
    }
  }
}

void updateProximity() {
  // Check if proximity data is available
  if (APDS.proximityAvailable()) {
    // Read the proximity value
    int proximity = APDS.readProximity();

    if (proximity == -1) {
      Serial.println("Proximity read error.");
      return; // Exit if the reading is invalid
    }

    // Check for significant changes to reduce BLE updates
    if (proximity != oldProximity) {
      char buffer[VALUE_SIZE];
      int ret = snprintf(buffer, sizeof(buffer), "%u", proximity); // Convert proximity to string

      if (ret >= 0) {
        // Send proximity value over BLE
        proximityCharacteristic.writeValue(buffer);

        // Print proximity and thresholds to Serial Monitor
        Serial.print("Proximity: ");
        Serial.println(proximity);

        if (proximity > 150) {
          Serial.println("Status: Far");
        } else if (proximity > 50 && proximity <= 150) {
          Serial.println("Status: Medium");
        } else {
          Serial.println("Status: Close");
        }

        // Update the last known proximity value
        oldProximity = proximity;
      }
    }
  }
}


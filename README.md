# BLE Temperature Monitoring

This repository contains code for a BLE (Bluetooth Low Energy) temperature monitoring system. It includes:
- A **peripheral device** (Arduino) that reads temperature data and broadcasts it via BLE.
- A **central device** (Windows machine running Python) that connects to the peripheral to display the temperature data in real time.


---

## Requirements

### Peripheral (Arduino):
- **Hardware**:
  - Arduino board with BLE support (e.g., Arduino Nano 33 BLE Sense).
  - HS300x Temperature and Humidity Sensor.
- **Software**:
  - Arduino IDE (latest version).
  - Libraries:
    - `ArduinoBLE`
    - `Arduino_HS300x`
  - Install these libraries from the Arduino Library Manager.

### Central (Windows Machine):
- **Hardware**:
  - BLE-supported device (e.g., Bluetooth adapter).
- **Software**:
  - Python 3.8 or higher.
  - Libraries:
    - `bleak` (Install using `pip install bleak`).

---

## Setup Instructions

### Peripheral (Arduino)
1. **Connect Hardware**:
   - Connect the HS300x sensor to the Arduino board as per the sensor's datasheet.

2. **Upload Code**:
   - Open `peripheral/peripheral.ino` in the Arduino IDE.
   - Select the correct board and port from the **Tools** menu.
   - Click **Upload** to upload the sketch to your Arduino.

3. **Verify Functionality**:
   - Open the Serial Monitor (set to 9600 baud rate).
   - You should see messages indicating BLE initialization and connection status.

---

### Central (Windows Machine)
1. **Set Up Python Environment**:
   - Install Python 3.8 or higher.
   - Install the required library by running:
     ```bash
     pip install bleak
     ```

2. **Run the Central Script**:
   - Navigate to `central/ble_temperature/`.
   - Run the script:
     ```bash
     python simpleBLETemp.py
     ```

3. **Connect to the Peripheral**:
   - The script will scan for BLE devices and display available devices.
   - It will automatically connect to a device named `BLE-TEMP` (as defined in the Arduino sketch).
   - Once connected, temperature data will be displayed in real time.

---

## Testing the System

1. **Peripheral Setup**:
   - Ensure the Arduino is powered and running the `peripheral.ino` sketch.
   - Verify that the Serial Monitor shows: `Bluetooth® device active, waiting for connections...`.

2. **Central Setup**:
   - Run `simpleBLETemp.py` on your Windows machine.
   - Check for messages indicating the BLE device is found and connected.

3. **Expected Behavior**:
   - On connection, the LED on the Arduino (built-in or external) should light up.
   - Temperature readings should appear in the terminal running the Python script, e.g.:
     ```
     Temperature: 25.3 °C
     Temperature: 25.5 °C
     ```

4. **Disconnect**:
   - If the BLE central disconnects, the Arduino LED should turn off, and the Python script should exit.

---

## Troubleshooting

### Peripheral
- **No BLE advertising**:
  - Ensure the Arduino sketch is correctly uploaded.
  - Check the Serial Monitor for errors.

### Central
- **Device not found**:
  - Ensure the peripheral is powered on and advertising.
  - Verify the BLE adapter on your Windows machine is working.

- **UUID mismatch**:
  - Check that the service and characteristic UUIDs in `simpleBLETemp.py` match those in `peripheral.ino`.

---

## Extending the Project
- Add humidity monitoring using the HS300x sensor.
- Integrate data logging or visualization on the central device.
- Build a mobile application to act as the BLE central.

---

## License
This project is open source and available under the MIT License.

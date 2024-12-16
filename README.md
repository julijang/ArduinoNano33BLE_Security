# BLE Security System with Temperature and Proximity Monitoring

This repository contains code for a BLE-based security system that triggers an alarm when:
- The **temperature fluctuates** by ±1°C.
- The **proximity sensor** detects a value below 245.

The system includes:
- A **peripheral device** (Arduino) that monitors temperature and proximity values, broadcasting them via BLE through a windows-compatible machine.
- A **central device** (Windows machine running Python/C++) that connects to the peripheral, processes the data, and opens a **visual alarm (GUI)** with an audible alarm response.

---

## Requirements

### Peripheral (Arduino Nano 33 BLE Sense Rev2):
- **Hardware**:
  - Arduino board with BLE support (e.g., Arduino Nano 33 BLE Sense) containing a **HS300x Temperature and Humidity Sensor** and an **APDS9960 Proximity Sensor**.
- **Software**:
  - Arduino IDE (latest version).
  - Visual Studio Code or a viable shell program compatible with python scripts.
  - Arduino IDE Libraries:
    - `ArduinoBLE`
    - `Arduino_HS300x`
    - `Arduino_APDS9960`
  - Install these libraries via the Arduino Library Manager.

### Central (Windows Machine):
- **Hardware**:
  - BLE-supported device (e.g., built-in Bluetooth adapter or external BLE dongle).
  - Audio device (built-in speakers or external A/V equipment).
- **Software**:
  - Python 3.8 or higher.
  - Libraries:
    - `bleak` (for BLE communication)
    - `playsound` (for alarm sound playback)
    - `tkinter` (built-in for GUI)
  - Install the required libraries using `pip`:
    ```bash
    python -m pip install --upgrade pip setuptools wheel
    pip install bleak playsound==1.3.0
    ```

---

## Setup Instructions

### Peripheral (Arduino)
1. **Connect the Hardware**:
   - Plug the Arduino board into a viable Central machine via usb.

2. **Upload Code**:
   - Open `peripheral/peripheral.ino` in the Arduino IDE.
   - Select the correct board and port from the **Tools** menu.
   - Click **Upload** to upload the sketch to your Arduino.

3. **Verify Functionality**:
   - Open the Serial Monitor (set to 9600 baud rate).
   - Confirm initialization of sensors and BLE:
     ```
     HS300x initialized successfully.
     APDS9960 initialized successfully.
     Bluetooth® device active, waiting for connections...
     ```

---

### Central (Windows Machine)
1. **Set Up Python Environment**:
   - Ensure Python 3.8 or higher is installed.
   - Install the required libraries:
     ```bash
     python -m pip install --upgrade pip setuptools wheel
     pip install bleak playsound==1.3.0
     ```

2. **Run the Central Script**:
   - Navigate to the central script directory:
     ```bash
     cd central/ble_security
     ```
   - Run the program:
     ```bash
     python simpleBLESecurity.py
     ```

3. **Connect to the Peripheral**:
   - The script will scan for BLE devices and connect to a device named `BLE-TEMP`.
   - Once connected, the program will monitor:
     - **Temperature**: Fluctuations of ±1°C.
     - **Proximity**: Values below a proximity of `245`.

4. **Triggering the Alarm**:
   - If a security event occurs (rapid temperature change or sudden proximity drop), the program will:
     - Play an **alarm sound** in a loop.
     - Display a **red GUI** with details of the trigger.
   - The user can disable the alarm using the **"Disable Alarm"** button.

---

## Testing the System

### Peripheral Setup
1. Ensure the Arduino is powered and running the `peripheral.ino` sketch.
2. Verify the Serial Monitor shows BLE initialization and sensor outputs.

### Central Setup
1. Run `simpleBLESecurity.py` on your Windows machine.
2. Observe BLE scanning and connection messages:


### Expected Behavior
1. **Normal Operation**:
- The GUI will display:
  ```
  System is secure.
  ```

2. **Triggered Alarm**:
- For temperature fluctuations:
  ```
  Temperature fluctuation of 1.50°C detected at: 23.50°C
  ```
- For low proximity:
  ```
  Proximity alert! Value: 240
  ```
- The GUI background will turn red, and the alarm sound will play in a loop.

3. **Disabling the Alarm**:
- Clicking the **"Disable Alarm"** button will reset the alarm state and return the GUI to its normal (green) background.

4. **Exiting the Program**:
- Click the **"X"** button at the top-right corner of the GUI to close the GUI.
- CTRL + C to terminate the Arduino in the terminal of your IDE/Shell.

---

## Troubleshooting

### Peripheral (Arduino)
- **No BLE Advertising**:
- Ensure the correct Arduino board and port are selected.
- Check the Serial Monitor for errors during initialization.
- Verify the Central device has bluetooth enabled.

### Central (Windows Machine)
- **Device Not Found**:
- Verify the Arduino is powered on and advertising.
- Ensure the BLE adapter on your Windows machine is functional.

- **Invalid UUID Errors**:
- Confirm that the service and characteristic UUIDs in `simpleBLESecurity.py` match those in `peripheral.ino`.

- **Alarm Sound Not Playing**:
- Verify the path to the alarm sound file is correct (paths may vary based on the Machine).
- Ensure `playsound` is installed:
 ```bash
 pip install playsound==1.3.0
 ```

---

## Extending the Project
- Integrate additional sensors (e.g., humidity or velocity detection).
- Add logging functionality to store sensor events and alarm triggers.
- Develop a mobile app to monitor the security system remotely.

---

## License
This project is open source and available under the MIT License.

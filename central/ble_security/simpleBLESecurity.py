import asyncio
from bleak import BleakScanner, BleakClient
from tkinter import *
import threading
from playsound import playsound
import os
import sys

# UUIDs for BLE services and characteristics
TEMPERATURE_SERVICE_UUID = "00000000-5EC4-4083-81CD-A10B8D5CF6EC"
TEMPERATURE_CHARACTERISTIC_UUID = "00000001-5EC4-4083-81CD-A10B8D5CF6EC"
PROXIMITY_SERVICE_UUID = "00000003-5EC4-4083-81CD-A10B8D5CF6EC"
PROXIMITY_CHARACTERISTIC_UUID = "00000004-5EC4-4083-81CD-A10B8D5CF6EC"
DEVICE_NAME = "BLE-TEMP"

# Globals for alarm and GUI
alarm_active = False
last_temperature = None
last_proximity = None
activation_info = "System is secure."
ALARM_SOUND_PATH = "C:/Users/Julijan/Documents/CIS_310/ArduinoNano33BLE_Security/Alarm.mp3"


# GUI Functions
def play_alarm():
    """Plays the alarm sound on loop."""
    while alarm_active:
        playsound(ALARM_SOUND_PATH)


def start_alarm():
    """Starts the alarm sound and updates the GUI."""
    global alarm_active
    alarm_active = True
    info_label.config(text=activation_info, fg="white", bg="red")  # Update info_label
    gui.configure(bg="red")
    threading.Thread(target=play_alarm, daemon=True).start()


def reset_alarm():
    """Resets the alarm without closing the GUI."""
    global alarm_active
    alarm_active = False
    info_label.config(text="System is secure.", fg="white", bg="green")  # Update info_label
    gui.configure(bg="green")


def on_close():
    """Handles GUI close event."""
    global alarm_active
    alarm_active = False
    print("Stopping program...")
    try:
        asyncio.get_event_loop().stop()  # Stop the asyncio event loop
    except Exception:
        pass
    gui.destroy()  # Close the GUI
    sys.exit(0)  # Forcefully exit the program


# GUI Setup
def launch_gui():
    """Launches the GUI."""
    global gui, info_label

    gui = Tk(className="Security Alert")
    gui.geometry("800x400")
    gui.configure(bg="green")  # Initial safe state

    # Handle the window close event (X button)
    gui.protocol("WM_DELETE_WINDOW", on_close)

    # Display warning message
    title = Label(gui, text="Break-in Warning", bd=9, relief=GROOVE,
                  font=("times new roman", 50, "bold"), bg="white", fg="black")
    title.pack(side=TOP, fill=X)

    # Display activation info
    info_label = Label(gui, text=activation_info, font=("times new roman", 20, "bold"), bg="green", fg="white")
    info_label.pack(pady=20)

    # Add disable alarm button
    frame = Frame(gui)
    frame.pack()
    button = Button(frame, text="Disable Alarm", command=reset_alarm)
    button.pack()

    gui.mainloop()


# BLE Functions
async def handle_temperature_data(sender, data):
    """Handles temperature notifications from the BLE device."""
    global last_temperature, alarm_active, activation_info

    try:
        temperature = float(data.decode("utf-8"))
        if last_temperature is not None and abs(temperature - last_temperature) >= 0.1:
            activation_info = f"Temperature fluctuation of {abs(temperature - last_temperature):.2f}°C detected at: {temperature:.2f}°C"
            if not alarm_active:
                start_alarm()
        last_temperature = temperature
        print(f"Temperature: {temperature:.2f} °C")
    except ValueError:
        print(f"Invalid temperature data received: {data}")


async def handle_proximity_data(sender, data):
    """Handles proximity notifications from the BLE device."""
    global last_proximity, alarm_active, activation_info

    try:
        proximity = int(data.decode("utf-8"))
        if proximity < 245:
            activation_info = f"Proximity alert! Value: {proximity}"
            if not alarm_active:
                start_alarm()
        last_proximity = proximity
        print(f"Proximity: {proximity}")
    except ValueError:
        print(f"Invalid proximity data received: {data}")


async def connect_to_device():
    """Main function to scan, connect, and handle BLE notifications."""
    print("Scanning for BLE devices... This may take a few seconds.")
    devices = await BleakScanner.discover()

    target_device = None
    for device in devices:
        print(f"Found device: {device.name}, Address: {device.address}")
        if device.name == DEVICE_NAME:
            target_device = device
            break

    if not target_device:
        print(f"Device '{DEVICE_NAME}' not found. Make sure it's advertising and try again.")
        return

    print(f"Connecting to {DEVICE_NAME} at address {target_device.address}...")
    async with BleakClient(target_device.address) as client:
        print(f"Connected to {DEVICE_NAME}!")

        # Subscribing to temperature and proximity notifications
        await client.start_notify(TEMPERATURE_CHARACTERISTIC_UUID, handle_temperature_data)
        await client.start_notify(PROXIMITY_CHARACTERISTIC_UUID, handle_proximity_data)

        print("Receiving data... Press Ctrl+C to exit.")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping notifications...")
            await client.stop_notify(TEMPERATURE_CHARACTERISTIC_UUID)
            await client.stop_notify(PROXIMITY_CHARACTERISTIC_UUID)
            print("Disconnected.")


# Main Function
if __name__ == "__main__":
    threading.Thread(target=launch_gui, daemon=True).start()  # Start the GUI in an external window
    try:
        asyncio.run(connect_to_device())
    except KeyboardInterrupt:
        print("Program stopped manually.")

from playsound import playsound
from tkinter import *
import threading

# should be changed based on whether temperature or proximity sensor activates alarm
activation_info = "Unusual temperature change detected"

# function to play alarm sound on loop
def play_alarm():
    while True:
        playsound("C:\\Users\\lanab\\OneDrive\\Documents\\Audacity\\Alarm.mp3")
# above path will need to be adjusted based on the device that the code is ran on

# function to start the alarm sound
def start_alarm():
    threading.Thread(target=play_alarm, daemon=True).start()

# initialize gui window
gui = Tk(className='Python Examples - Window Color')

# function to close the gui
def close_window():
    gui.destroy()

# set window size
gui.geometry("800x400")

# set window color
gui.configure(bg='red')

# start playing alarm once gui window opens
gui.after(0, start_alarm)
 
# display warning message 
title=Label(gui,text="Break-in Warning",bd=9,relief=GROOVE,
            font=("times new roman",50,"bold"),bg="white",fg="black") 
title.pack(side=TOP,fill=X) 

# display info on what activated the alarm
info=Label(gui,text=activation_info,
           font=("times new roman",10,"bold")).pack(pady=20)

# create button to close gui window
frame = Frame(gui)
frame.pack()
button = Button (frame, text = "Disable Alarm", command = close_window)
button.pack()

gui.mainloop() 
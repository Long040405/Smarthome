# Smarthome Bill Cipher Dashboard

A smart home control application (Smarthome) integrated with Arduino hardware communication, featuring a unique user interface design inspired by the character Bill Cipher (Gravity Falls).

The project is built in Python, using Tkinter/CustomTkinter for the GUI, OpenCV to play the unlock video, Pygame for background music playback, and pySerial to synchronize states with the physical Arduino board.

---

## Main Dashboard UI

Below are the two main dashboard UI styles corresponding to the two themes selectable in the application:

### 1. Dipper Theme
![Dipper Theme Dashboard UI](image/ui_dipper.png)

### 2. Bill Cipher Theme
![Bill Cipher Theme Dashboard UI](image/ui_bill.png)

---

## Key Features

### Security & Authentication
* Requires a passcode for entry (default: 1111) with password masking.
* Automatically triggers verification once 4 digits are typed or Enter is pressed.
* **Security Alerts**: If an incorrect passcode is entered more than 3 times:
  * The hardware LED flashes to signal an alert.
  * A custom Bill Cipher lock screen warning is displayed.
  * An alert email is sent automatically via Gmail to the administrator's inbox.
  * The application exits immediately to secure the system.

### Interactive Unlock Effect
* Upon successful authentication, a short unlocking video (`Video/wc.mp4`) plays on the screen via OpenCV before entering the main control panel.

### Theme-based Background Music
* Background music loops infinitely using `pygame.mixer` and automatically switches based on the selected user interface theme (Dipper Theme & Bill Cipher Theme). Changing the theme updates both the background and button graphics accordingly.

### Room Control & Management
* **Bedroom**: Control the bedroom light (On/Off/Blink), switch the bedroom background according to Day/Night mode, open/close the door, and view the real-time temperature.
* **Living Room**: Control the fan (On/Off), room lighting, flashing lights, and open/close the main door.
* **Garage**: Open/close the garage door (Up/Down) and the connecting door.

### Arduino Integration & Simulation (Dummy Mode)
* Synchronizes commands directly with the Arduino microcontroller via Serial communication.
* **Simulation Mode (DummySerial)**: If no hardware Arduino is connected (e.g., during development or testing on a computer without a serial connection), the app automatically switches to dummy mode. All commands are logged to the console, and room temperature values are randomly simulated between 25-27 °C for a seamless GUI experience without application crashes.

---

## Modular Architecture

The project is structured modularly for easy maintenance and scaling:

* `main.py`: The entry point of the application, managing Tkinter frames and room states inside the `SmartHomeApp` class.
* `config.py`: Stores static configurations, SMTP email credentials, hardware serial settings, and resource paths (images, audio, video).
* `serial_handler.py`: Manages the serial communication connection with Arduino and implements the `DummySerial` simulation fallback.
* `email_sender.py`: A helper utility to connect to the SMTP server and send security alert emails.

---

## Installation & Setup

### 1. System Requirements
* Python 3.10 or higher.
* Necessary dependencies installed.

### 2. Install Dependencies
Open a terminal in the project directory and run:
```bash
pip install customtkinter pillow opencv-python pyserial pygame
```

### 3. Launch the Application
Run the main script:
```bash
python3 main.py
```
> **Tip**: If you don't have the Arduino board connected, the program will log a connection error and automatically launch in simulation mode. Type `1111` as the passcode to unlock and explore the application.
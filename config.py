# Configuration settings for Smarthome application

# Email warning credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "smarthomekhoahocmaytinh2@gmail.com"
SENDER_PASSWORD = "xepg wpss dbhp nddc"
RECIPIENT_EMAIL = "long4th4@gmail.com"

# Serial Connection details
SERIAL_PORT = "COM7"
SERIAL_BAUDRATE = 19200
SERIAL_TIMEOUT = 1

# Password settings
ACCESS_PASSWORD = "1111"
MAX_WRONG_ATTEMPTS = 3

# Paths and Assets
PASSWORD_BG_IMAGE = "image/Bill.png"
RADIO_IMG1 = "image/Dipbo.png"
RADIO_IMG2 = "image/Piu.png"
GARAGE_BG_IMAGE = "image/garage1.jpg"
ERROR_IMAGE_PATH = "image/Lock.jpg"
UNLOCKED_VIDEO_PATH = "Video/wc.mp4"

BUTTON_IMAGES = {
    "Song 1": {
        "hjhj": "image/sim.jpg",
        "sd": "image/shit.jpg",
        "door": "image/Door.jpg",
        "living_room": "image/LivingRoom.jpg",
        "bedroom": "image/Bedroom.jpg",
        "garage": "image/GARAGE.jpg",
    },
    "Song 2": {
        "hjhj": "image/new_sim.jpg",
        "sd": "image/new_shutdown.jpg",
        "door": "image/new_door.jpg",
        "living_room": "image/new_livingroom.jpg",
        "bedroom": "image/new_bedroom.jpg",
        "garage": "image/new_garage.jpg",
    },
}

SONGS = {
    "Song 1": "Sound/opn.mp3",
    "Song 2": "Sound/opn1.mp3"
}

BACKGROUND_IMAGES = {
    "Day": "image/daybr.jpg",
    "Night": "image/nightbr.jpg",
}

BACKGROUND_IMAGES_LVR = {
    "DayLivingroom": "image/daylvr.jpg",
    "NightLivingroom": "image/nightlvr.jpg"
}

BACKGROUND_IMAGES_CONTROL_PANEL = {
    "Song 1": "image/Stanhome.jpg",
    "Song 2": "image/Billhome.jpg"
}

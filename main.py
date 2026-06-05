import tkinter as tk
import tkinter.font as tkfont
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
# Compatibility patch for older Pillow versions (like 9.0.1)
if not hasattr(Image, 'Resampling'):
    Image.Resampling = Image
import cv2
import time
import pygame

import config
from serial_handler import SerialHandler
from email_sender import send_warning_email

class SmartHomeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smarthome Dashboard")
        self.root.geometry('800x600+100+100')

        # Global states
        self.fan_status = False
        self.door_status = False
        self.door_garage = False
        self.bedroom_light_status = False
        self.livingroom_light_status = False
        self.current_song = "opn.mp3"
        self.wrong_attempts = 0
        self.current_bg_key = "Day"
        self.current_bg_livingroom_key = "DayLivingroom"

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Initialize Serial connection
        self.serial = SerialHandler(config.SERIAL_PORT, config.SERIAL_BAUDRATE, config.SERIAL_TIMEOUT)

        # Tkinter variables
        self.song_var = tk.StringVar(value=list(config.SONGS.keys())[0])

        # Setup Styles and Frames
        self.setup_styles()
        self.create_frames()

        # Setup Views
        self.setup_password_frame()
        self.setup_video_frame()
        self.setup_control_panel_frame()
        self.setup_bedroom_frame()
        self.setup_livingroom_frame()
        self.setup_garage_frame()

        # Start background tasks
        self.root.after(1000, self.read_temperature)

        # Show initial view
        self.show_frame(self.password_frame)

        # Window closing handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "Custom.TRadiobutton",
            background="white",
            foreground="black",
            font=("Arial", 12),
            padding=5,
            borderwidth=1,
            relief="flat"
        )

    def create_frames(self):
        self.password_frame = tk.Frame(self.root)
        self.video_frame = tk.Frame(self.root)
        self.control_panel_frame = tk.Frame(self.root)
        self.bedroom_frame = tk.Frame(self.root)
        self.living_room_frame = tk.Frame(self.root)
        self.garage_frame = tk.Frame(self.root)

        for frame in (self.password_frame, self.video_frame, self.control_panel_frame, 
                      self.bedroom_frame, self.living_room_frame, self.garage_frame):
            frame.grid(row=0, column=0, sticky='nsew')

    def setup_password_frame(self):
        bg_image = Image.open(config.PASSWORD_BG_IMAGE).resize((800, 600), Image.Resampling.LANCZOS)
        self.password_photo = ImageTk.PhotoImage(bg_image)

        L1 = tk.Label(self.password_frame, image=self.password_photo)
        L1.pack(pady=20)

        custom_font = tkfont.Font(family="Algerian", size=20)

        label_password = tk.Label(L1, text="Nhập mật khẩu:", bg="black", fg="white", font=custom_font)
        label_password.place(x=50, y=280)

        self.entry = tk.Entry(L1, show="*", bg="black", fg="white", font=custom_font, width=10)
        self.entry.place(x=70, y=330)

        self.entry.focus_set()

        self.entry.bind("<Return>", lambda event: self.check_password())
        self.entry.bind("<KeyRelease>", lambda event: self.on_key_release(event))

    def on_key_release(self, event):
        if len(self.entry.get()) == 4:
            self.check_password()

    def check_password(self):
        password = self.entry.get()
        if password == config.ACCESS_PASSWORD:
            print("Đăng nhập thành công!")
            self.play_song()
            self.show_frame(self.video_frame)
            self.play_unlocked_video(config.UNLOCKED_VIDEO_PATH)
        else:
            self.wrong_attempts += 1
            if self.wrong_attempts >= config.MAX_WRONG_ATTEMPTS:
                self.both_lights_blink()
                self.show_error_image()
                send_warning_email()
                self.root.withdraw()
            else:
                messagebox.showerror("Lỗi", f"Sai mật khẩu! Bạn còn {config.MAX_WRONG_ATTEMPTS - self.wrong_attempts} lần thử.")
                self.entry.delete(0, tk.END)

    def setup_video_frame(self):
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()

    def play_unlocked_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        start_time = time.time()

        def update_frame():
            ret, frame = cap.read()
            if not ret:
                cap.release()
                cv2.destroyAllWindows()
                self.show_frame(self.control_panel_frame)
                return
            resized_frame = cv2.resize(frame, (800, 600))
            cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            if time.time() - start_time >= 16:
                cap.release()
                cv2.destroyAllWindows()
                self.show_frame(self.control_panel_frame)
                return
            self.video_label.after(15, update_frame)

        update_frame()

    def setup_control_panel_frame(self):
        self.control_panel_frame.configure(bg="#F0F0F0")

        # Load radio images
        img1 = Image.open(config.RADIO_IMG1).resize((50, 50))
        img2 = Image.open(config.RADIO_IMG2).resize((50, 50))
        self.photo1 = ImageTk.PhotoImage(img1)
        self.photo2 = ImageTk.PhotoImage(img2)

        # Control panel background
        initial_bg_path = config.BACKGROUND_IMAGES_CONTROL_PANEL["Song 1"]
        bg_image = Image.open(initial_bg_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo_control_panel = ImageTk.PhotoImage(bg_image)

        self.background_label_control_panel = tk.Label(self.control_panel_frame, image=self.bg_photo_control_panel)
        self.background_label_control_panel.place(x=0, y=0)
        self.background_label_control_panel.lower()

        # Control panel buttons
        self.hjhj_button = tk.Button(self.control_panel_frame, command=self.hjhj, relief=tk.RIDGE)
        self.hjhj_button.place(x=590, y=10)

        self.sd_button = tk.Button(self.control_panel_frame, command=self.shjt, relief=tk.RIDGE)
        self.sd_button.place(x=590, y=490)

        self.door_button = tk.Button(self.control_panel_frame, command=self.toggle_door, relief=tk.RIDGE)
        self.door_button.place(x=10, y=485)

        self.living_room_button = tk.Button(self.control_panel_frame, command=self.living_room, relief=tk.RIDGE)
        self.living_room_button.place(x=10, y=10)

        self.bedroom_button = tk.Button(self.control_panel_frame, command=self.bedroom, relief=tk.RIDGE)
        self.bedroom_button.place(x=10, y=120)

        self.garage_button = tk.Button(self.control_panel_frame, command=self.garage, relief=tk.RIDGE)
        self.garage_button.place(x=10, y=230)

        # Packed text radio buttons
        for song_name in config.SONGS.keys():
            radio = tk.Radiobutton(
                self.control_panel_frame,
                text=song_name,
                variable=self.song_var,
                value=song_name,
                command=self.play_song
            )
            radio.pack(anchor=tk.W)

        # Image radio buttons
        radio1 = ttk.Radiobutton(self.control_panel_frame, image=self.photo1, variable=self.song_var, 
                                 value="Song 1", command=self.play_song, style="Custom.TRadiobutton")
        radio1.place(x=620, y=190)

        radio2 = ttk.Radiobutton(self.control_panel_frame, image=self.photo2, variable=self.song_var, 
                                 value="Song 2", command=self.play_song, style="Custom.TRadiobutton")
        radio2.place(x=690, y=190)

        # Initialize button images
        self.update_button_images(self.song_var.get())

    def create_button_image(self, path, size):
        button_image = Image.open(path).resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(button_image)

    def update_button_images(self, song_name):
        images = config.BUTTON_IMAGES.get(song_name, {})

        hjhj_image = self.create_button_image(images.get("hjhj", "image/sim.jpg"), (200, 100))
        self.hjhj_button.config(image=hjhj_image)
        self.hjhj_button.image = hjhj_image

        sd_image = self.create_button_image(images.get("sd", "image/shit.jpg"), (200, 100))
        self.sd_button.config(image=sd_image)
        self.sd_button.image = sd_image

        door_image = self.create_button_image(images.get("door", "image/Door.jpg"), (200, 100))
        self.door_button.config(image=door_image)
        self.door_button.image = door_image

        living_room_image = self.create_button_image(images.get("living_room", "image/LivingRoom.jpg"), (200, 100))
        self.living_room_button.config(image=living_room_image)
        self.living_room_button.image = living_room_image

        bedroom_image = self.create_button_image(images.get("bedroom", "image/Bedroom.jpg"), (200, 100))
        self.bedroom_button.config(image=bedroom_image)
        self.bedroom_button.image = bedroom_image

        garage_image = self.create_button_image(images.get("garage", "image/GARAGE.jpg"), (200, 100))
        self.garage_button.config(image=garage_image)
        self.garage_button.image = garage_image

    def play_song(self):
        selected_song = self.song_var.get()
        if selected_song != self.current_song:
            self.current_song = selected_song
            song_path = config.SONGS[selected_song]
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play(loops=-1)
            self.change_background_control_panel(selected_song)
            self.update_button_images(selected_song)

    def change_background_control_panel(self, song_name):
        image_path = config.BACKGROUND_IMAGES_CONTROL_PANEL[song_name]
        self.load_new_background_control_panel(image_path)

    def load_new_background_control_panel(self, image_path):
        bg_image = Image.open(image_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.bg_photo_control_panel = ImageTk.PhotoImage(bg_image)
        self.background_label_control_panel.config(image=self.bg_photo_control_panel)

    def setup_bedroom_frame(self):
        # Background
        bg_path = config.BACKGROUND_IMAGES[self.current_bg_key]
        bg_image = Image.open(bg_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.bedroom_bg_photo = ImageTk.PhotoImage(bg_image)

        self.bedroom_bg_label = tk.Label(self.bedroom_frame, image=self.bedroom_bg_photo)
        self.bedroom_bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Temperature
        self.temperature_label = tk.Label(self.bedroom_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
        self.temperature_label.place(x=530, y=100)

        # Resize component images
        self.door_img = self.resize_image("image/Door.jpg", 150, 80)
        self.light_on_img = self.resize_image("image/light_on.jpg", 150, 80)
        self.light_off_img = self.resize_image("image/light_off.jpg", 150, 80)
        self.blink_img = self.resize_image("image/blink.jpg", 150, 80)
        self.back_img = self.resize_image("image/back.jpg", 150, 80)

        # Buttons
        door_btn = tk.Button(self.bedroom_frame, image=self.door_img, command=self.toggle_door, bd=0)
        door_btn.place(x=50, y=50)

        self.light_button = tk.Button(
            self.bedroom_frame, 
            image=self.light_on_img if self.bedroom_light_status else self.light_off_img, 
            command=self.toggle_bedroom_light, 
            bd=0
        )
        self.light_button.place(x=50, y=140)

        blink_btn = tk.Button(self.bedroom_frame, image=self.blink_img, command=self.bedroom_light_blink, bd=0)
        blink_btn.place(x=50, y=230)

        back_btn = tk.Button(self.bedroom_frame, image=self.back_img, command=self.back_to_main, bd=0)
        back_btn.place(x=620, y=500)

    def resize_image(self, image_path, width, height):
        image = Image.open(image_path).resize((width, height), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def setup_livingroom_frame(self):
        # Background
        bg_path = config.BACKGROUND_IMAGES_LVR[self.current_bg_livingroom_key]
        bg_image = Image.open(bg_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.livingroom_bg_photo = ImageTk.PhotoImage(bg_image)

        self.background_label_livingroom = tk.Label(self.living_room_frame, image=self.livingroom_bg_photo)
        self.background_label_livingroom.place(x=0, y=0, relwidth=1, relheight=1)

        # Temperature
        self.temperature_label_livingroom = tk.Label(self.living_room_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
        self.temperature_label_livingroom.place(x=140, y=150)

        # Component images
        self.fan_img = self.resize_image("image/Fan.jpg", 150, 80)
        self.light_img = self.resize_image("image/Light.jpg", 150, 80)

        # Buttons
        light_btn = tk.Button(self.living_room_frame, image=self.light_img, command=self.toggle_livingroom_light, bd=0)
        light_btn.place(x=600, y=50)

        blink_btn = tk.Button(self.living_room_frame, image=self.blink_img, command=self.livingroom_light_blink, bd=0)
        blink_btn.place(x=600, y=140)

        fan_btn = tk.Button(self.living_room_frame, image=self.fan_img, command=self.toggle_fan, bd=0)
        fan_btn.place(x=600, y=230)

        door_btn = tk.Button(self.living_room_frame, image=self.door_img, command=self.toggle_door, bd=0)
        door_btn.place(x=600, y=320)

        back_btn = tk.Button(self.living_room_frame, image=self.back_img, command=self.back_to_main, bd=0)
        back_btn.place(x=600, y=500)

    def setup_garage_frame(self):
        # Background
        bg_image = Image.open(config.GARAGE_BG_IMAGE).resize((800, 600), Image.Resampling.LANCZOS)
        self.garage_bg_photo = ImageTk.PhotoImage(bg_image)

        self.background_label_garage = tk.Label(self.garage_frame, image=self.garage_bg_photo)
        self.background_label_garage.place(x=0, y=0, relwidth=1, relheight=1)

        # Temperature
        self.temperature_label_garage = tk.Label(self.garage_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
        self.temperature_label_garage.place(x=280, y=190)

        # Component images
        self.up_img = self.resize_image("image/up.jpg", 150, 80)
        self.down_img = self.resize_image("image/down.jpg", 150, 80)

        # Buttons
        self.btn_door_garage = tk.Button(
            self.garage_frame, 
            image=self.down_img if self.door_garage else self.up_img, 
            command=self.garage_door, 
            bd=0
        )
        self.btn_door_garage.place(x=600, y=30)

        door_btn = tk.Button(self.garage_frame, image=self.door_img, command=self.toggle_door, bd=0)
        door_btn.place(x=600, y=120)

        back_btn = tk.Button(self.garage_frame, image=self.back_img, command=self.back_to_main, bd=0)
        back_btn.place(x=600, y=500)

    def show_frame(self, frame):
        frame.tkraise()

    def back_to_main(self):
        self.show_frame(self.control_panel_frame)

    def living_room(self):
        self.show_frame(self.living_room_frame)

    def bedroom(self):
        self.show_frame(self.bedroom_frame)

    def garage(self):
        self.show_frame(self.garage_frame)

    def show_error_image(self):
        error_window = tk.Toplevel()
        error_window.geometry('800x600+100+100')

        error_image = Image.open(config.ERROR_IMAGE_PATH).resize((800, 600), Image.Resampling.LANCZOS)
        error_photo = ImageTk.PhotoImage(error_image)

        error_label = tk.Label(error_window, image=error_photo)
        error_label.image = error_photo
        error_label.pack()

        error_window.after(5000, error_window.destroy)

    def both_lights_blink(self):
        self.serial.send_cmd(b"6")

    def toggle_door(self):
        if self.door_status:
            if self.serial.send_cmd(b"d"):
                self.door_status = False
        else:
            if self.serial.send_cmd(b"m"):
                self.door_status = True

    def toggle_bedroom_light(self):
        if self.bedroom_light_status:
            if self.serial.send_cmd(b'0'):
                self.bedroom_light_status = False
                self.change_background("Day")
        else:
            if self.serial.send_cmd(b'1'):
                self.bedroom_light_status = True
                self.change_background("Night")
        self.light_button.config(image=self.light_off_img if self.bedroom_light_status else self.light_on_img)

    def bedroom_light_blink(self):
        self.serial.send_cmd(b'2')

    def read_temperature(self):
        temperature_data = self.serial.read_line()
        if temperature_data:
            self.temperature_label.config(text=f"{temperature_data} °C")
            self.temperature_label_livingroom.config(text=f"{temperature_data} °C")
            self.temperature_label_garage.config(text=f"{temperature_data} °C")
        self.root.after(1000, self.read_temperature)

    def hjhj(self):
        self.serial.send_cmd(b"p")

    def shjt(self):
        self.serial.send_cmd(b"f")

    def toggle_livingroom_light(self):
        if self.livingroom_light_status:
            if self.serial.send_cmd(b"4"):
                self.livingroom_light_status = False
                self.change_background_livingroom("DayLivingroom")
        else:
            if self.serial.send_cmd(b"3"):
                self.livingroom_light_status = True
                self.change_background_livingroom("NightLivingroom")
        self.light_button.config(image=self.light_on_img if self.livingroom_light_status else self.light_off_img)

    def garage_door(self):
        if self.door_garage:
            if self.serial.send_cmd(b"g"):
                self.door_garage = False
        else:
            if self.serial.send_cmd(b"e"):
                self.door_garage = True
        self.btn_door_garage.config(image=self.up_img if self.door_garage else self.down_img)

    def livingroom_light_blink(self):
        self.serial.send_cmd(b"5")

    def toggle_fan(self):
        if self.fan_status:
            if self.serial.send_cmd(b"t"):
                self.fan_status = False
        else:
            if self.serial.send_cmd(b"b"):
                self.fan_status = True

    def change_background(self, option):
        self.current_bg_key = option
        image_path = config.BACKGROUND_IMAGES[option]
        bg_image = Image.open(image_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.bedroom_bg_photo = ImageTk.PhotoImage(bg_image)
        self.bedroom_bg_label.config(image=self.bedroom_bg_photo)

    def change_background_livingroom(self, option1):
        self.current_bg_livingroom_key = option1
        image_path = config.BACKGROUND_IMAGES_LVR[option1]
        bg_image = Image.open(image_path).resize((800, 600), Image.Resampling.LANCZOS)
        self.livingroom_bg_photo = ImageTk.PhotoImage(bg_image)
        self.background_label_livingroom.config(image=self.livingroom_bg_photo)

    def on_closing(self):
        self.serial.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartHomeApp(root)
    root.mainloop()
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import cv2
import time
import serial
import pygame
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pygame.mixer.init()

W = tk.Tk()
W.geometry('800x600+100+100')

fan_status = False
door_status = False
door_garage = False
button_images = {
    "Song 1": {
        "hjhj": "sim.jpg",
        "sd": "shit.jpg",
        "door": "Door.jpg",
        "living_room": "LivingRoom.jpg",
        "bedroom": "Bedroom.jpg",
        "garage": "GARAGE.jpg",
    },
    "Song 2": {
        "hjhj": "new_sim.jpg",
        "sd": "new_shutdown.jpg",
        "door": "new_door.jpg",
        "living_room": "new_livingroom.jpg",
        "bedroom": "new_bedroom.jpg",
        "garage": "new_garage.jpg",
    },

}
songs = {
    "Song 1": "opn.mp3",
    "Song 2": "opn1.mp3"
}
current_song = "opn.mp3"
wrong_attempts = 0
unlocked_video_path = 'wc.mp4' 
error_image_path = 'Lock.jpg'  
door_status = False  
bedroom_light_status = False
livingroom_light_status = False 
background_images = {
    "Day": "daybr.jpg",
    "Night": "nightbr.jpg",
}
background_images_lvr = {
    "DayLivingroom": "daylvr.jpg",
    "NightLivingroom": "nightlvr.jpg"
}
background_images_control_panel = {
    "Song 1": "Stanhome.jpg",
    "Song 2": "Billhome.jpg"
}

current_bg_key = "Day" 
current_bg_livingroom_key = "DayLivingroom"  
song_var = tk.StringVar(value=list(songs.keys())[0]) 
radiobutton_font = tkfont.Font(family="Helvetica", size=12)

style = ttk.Style()
style.theme_use('clam')

style.configure("Custom.TRadiobutton",
                background="white",
                foreground="black",
                font=("Arial", 12),
                padding=5,
                borderwidth=1,
                relief="flat")

# Load images for radio buttons
img1 = Image.open("Dipbo.png").resize((50, 50))
img2 = Image.open("Piu.png").resize((50, 50))

photo1 = ImageTk.PhotoImage(img1)
photo2 = ImageTk.PhotoImage(img2)

# Define the SMTP server and port
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Email account credentials
sender_email = "smarthomekhoahocmaytinh2@gmail.com"
sender_password = "xepg wpss dbhp nddc"

# Recipient email
recipient_email = "nhivu.31231020245@st.ueh.edu.vn"

# Create the MIME message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = "Cảnh Báo: Đăng Nhập Quá Nhiều Lần"

# Nội dung email
body = """\
Chào bạn,

Hệ thống đã phát hiện số lượng đăng nhập không hợp lệ quá mức cho phép.

Nếu bạn không thực hiện các hoạt động đăng nhập này, vui lòng liên hệ với bộ phận hỗ trợ ngay lập tức.

Cảm ơn bạn,
~Nhóm LoNi2H~
"""
message.attach(MIMEText(body, "plain"))

# Khung để chứa các nút chọn bài hát
control_panel_frame = tk.Frame(W)
control_panel_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Đặt khung ở giữa

try:
    s1 = serial.Serial('COM7', 19200, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")



def update_button_images(song_name):
    images = button_images.get(song_name, {})
    
    hjhj_image = create_button_image(images.get("hjhj", "sim.jpg"), (200, 100))
    hjhj_button.config(image=hjhj_image)
    hjhj_button.image = hjhj_image
    
    sd_image = create_button_image(images.get("sd", "shit.jpg"), (200, 100))
    sd_button.config(image=sd_image)
    sd_button.image = sd_image
    
    door_image = create_button_image(images.get("door", "Door.jpg"), (200, 100))
    door_button.config(image=door_image)
    door_button.image = door_image
    
    living_room_image = create_button_image(images.get("living_room", "LivingRoom.jpg"), (200, 100))
    living_room_button.config(image=living_room_image)
    living_room_button.image = living_room_image
    
    bedroom_image = create_button_image(images.get("bedroom", "Bedroom.jpg"), (200, 100))
    bedroom_button.config(image=bedroom_image)
    bedroom_button.image = bedroom_image
    
    garage_image = create_button_image(images.get("garage", "GARAGE.jpg"), (200, 100))
    garage_button.config(image=garage_image)
    garage_button.image = garage_image
def play_song():
    global current_song
    selected_song = song_var.get()
    if selected_song != current_song:
        current_song = selected_song
        song_path = songs[selected_song]
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=-1)  # loops=-1 to loop indefinitely
        change_background_control_panel(selected_song)
        update_button_images(selected_song)
def change_background_control_panel(song_name):
    image_path = background_images_control_panel[song_name]
    load_new_background_control_panel(image_path)
def load_new_background_control_panel(image_path):
    background_image = Image.open(image_path)
    # Scale the image to fit the control panel frame dimensions (e.g., 800x600)
    background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label_control_panel.config(image=background_photo)
    background_label_control_panel.image = background_photo  # Keep a reference
for song_name in songs.keys():
    radio = tk.Radiobutton(
        control_panel_frame,
        text=song_name,
        variable=song_var,
        value=song_name,
        command=play_song
      )
    radio.pack(anchor=tk.W)
def check_password():
    global wrong_attempts
    password = entry.get()
    if password == '1111': 
        print("Đăng nhập thành công!")
        play_song()
        show_frame(video_frame) 
        play_unlocked_video(unlocked_video_path)      
    else:
        wrong_attempts += 1
        if wrong_attempts >= 3:
            both_lights_blink()
            show_error_image()
            mail()
            W.withdraw()
        else:
            messagebox.showerror("Lỗi", "Sai mật khẩu! Bạn còn {} lần thử.".format(3 - wrong_attempts))
            entry.delete(0, tk.END)
            
def play_unlocked_video(unlocked_video_path):
    cap = cv2.VideoCapture(unlocked_video_path)
    start_time = time.time()
    def update_frame():
        nonlocal start_time
        ret, frame = cap.read()
        if not ret:
            cap.release()
            cv2.destroyAllWindows()
            show_frame(control_panel_frame) 
            return
        resized_frame = cv2.resize(frame, (800, 600))
        cv2image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        if time.time() - start_time >= 16:
            cap.release()
            cv2.destroyAllWindows()
            show_frame(control_panel_frame)
            return
        video_label.after(15, update_frame)
    update_frame()

def show_error_image():
    error_window = tk.Toplevel()
    error_window.geometry('800x600+100+100')

    error_image = Image.open(error_image_path)
    error_image = error_image.resize((800, 600), Image.Resampling.LANCZOS)
    error_photo = ImageTk.PhotoImage(error_image)

    error_label = tk.Label(error_window, image=error_photo)
    error_label.image = error_photo  
    error_label.pack()

    def close_error_window():
        error_window.destroy()

    error_window.after(5000, close_error_window)

def both_lights_blink():
    try:
        s1.write(b"6")
    except Exception as e:
        print(f"Error: {e}")

def show_frame(frame):
    frame.tkraise()

def toggle_door():
    global door_status
    try:
        if door_status:
            s1.write(b"d") 
            door_status = False
        else:
            s1.write(b"m") 
            door_status = True
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def living_room():
    show_frame(living_room_frame)

def bedroom():
    show_frame(bedroom_frame)

def garage():
    show_frame(garage_frame)

def toggle_bedroom_light():
    global bedroom_light_status
    try:
        if bedroom_light_status:
            s1.write(b'0') 
            bedroom_light_status = False
        else:
            s1.write(b'1')
            bedroom_light_status = True
        light_button.config(image=light_off_img if bedroom_light_status else light_on_img)
        if bedroom_light_status:
            change_background("Night")
        else:
            change_background("Day")
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending command to Arduino: {e}")

def bedroom_light_blink():
    try:
        s1.write(b'2')  
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending command to Arduino: {e}")

def read_temperature():
    try:
        s1.write(b'n')
        temperature_data = s1.readline().decode().strip()
        temperature_label.config(text=f"{temperature_data} °C")
        temperature_label_livingroom.config(text=f"{temperature_data} °C")
        temperature_label_garage.config(text=f"{temperature_data} °C")
        W.after(1000, read_temperature) 
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending request to Arduino: {e}")

def hjhj():
    try:
        s1.write(b"p")
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def shjt():
    try:
        s1.write(b"f")
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")
        
def toggle_livingroom_light():
    global livingroom_light_status, light_on_img, light_off_img
    try:
        if livingroom_light_status:
            s1.write(b"4")
            livingroom_light_status = False
            change_background_livingroom("DayLivingroom")
        else:
            s1.write(b"3") 
            livingroom_light_status = True
            change_background_livingroom("NightLivingroom")
        
        # Cập nhật hình ảnh của nút đèn
        light_button.config(image=light_on_img if livingroom_light_status else light_off_img)
        
    except serial.SerialException as e:
        messagebox.showerror("Error", f"Error sending command to Arduino: {e}")

def garage_door():
    global door_garage
    try:
        if door_garage:
            s1.write(b"g")
            door_garage = False
        else:
            s1.write(b"e")
            door_garage = True
        
        btn_door_garage.config(image=up_img if door_garage else down_img)
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")
def livingroom_light_blink():
    try:
        s1.write(b"5")
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def toggle_fan():
    global fan_status
    try:
        if fan_status:
            s1.write(b"t")
            fan_status = False
        else:
            s1.write(b"b")
            fan_status = True
    except Exception as e:
        messagebox.showwarning("Error", f"Error: {e}")

def change_background_livingroom(option1):
    global current_bg_livingroom_key
    current_bg_livingroom_key = option1
    image_path = background_images_lvr[option1]
    load_new_background_livingroom(image_path)

def load_new_background_livingroom(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label_livingroom.config(image=background_photo)
    background_label_livingroom.image = background_photo  # Keep a reference

def change_background(option):
    global current_bg_key
    current_bg_key = option
    image_path = background_images[option]
    load_new_background(image_path)

def back_to_main():
    show_frame(control_panel_frame)

def load_new_background(image_path):
    background_image = Image.open(image_path)
    background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.config(image=background_photo)
    background_label.image = background_photo  

def mail():
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(sender_email, sender_password)  # Log in to the email account
        server.send_message(message)  # Send the email
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()  # Close the connection to the SMTP server

password_frame = tk.Frame(W)
video_frame = tk.Frame(W)
control_panel_frame = tk.Frame(W)
bedroom_frame = tk.Frame(W)
living_room_frame = tk.Frame(W)
garage_frame = tk.Frame(W)   

for frame in (password_frame, video_frame, control_panel_frame, bedroom_frame, living_room_frame,garage_frame):
    frame.grid(row=0, column=0, sticky='nsew')


A = Image.open('Bill.png') 
A = A.resize((800, 600), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(A)

L1 = tk.Label(password_frame, image=photo)
L1.image = photo  
L1.pack(pady=20)

custom_font = tkfont.Font(family="Algerian", size=20)

label_password = tk.Label(password_frame, text="Nhập mật khẩu:", bg="black", fg="white", font=custom_font)
label_password.place(x=50, y=280)

entry = tk.Entry(password_frame, show="*", bg="black", fg="white", font=custom_font, width=10)
entry.place(x=70, y=330)

entry.bind("<Return>", lambda event: check_password())
entry.bind("<KeyRelease>", lambda event: on_key_release(event))

def on_key_release(event):
    if len(entry.get()) == 4:
        check_password()

video_label = tk.Label(video_frame)
video_label.pack()

control_panel_frame.configure(bg="#F0F0F0")

initial_bg_path_control_panel = background_images_control_panel["Song 1"]
background_image_control_panel = Image.open(initial_bg_path_control_panel)
background_image_control_panel = background_image_control_panel.resize((800, 600), Image.Resampling.LANCZOS)
background_photo_control_panel = ImageTk.PhotoImage(background_image_control_panel)
background_label_control_panel = tk.Label(control_panel_frame, image=background_photo_control_panel)
background_label_control_panel.image = background_photo_control_panel

background_label_control_panel.place(x=0, y=0) 
background_label_control_panel.lower()

def create_button_image(path, size):
    button_image = Image.open(path)
    button_image = button_image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(button_image)

hjhj_button = tk.Button(control_panel_frame, command=hjhj, relief=tk.RIDGE)
hjhj_button.place(x=590, y=10)

sd_button = tk.Button(control_panel_frame, command=shjt, relief=tk.RIDGE)
sd_button.place(x=590, y=490)

door_button = tk.Button(control_panel_frame, command=toggle_door, relief=tk.RIDGE)
door_button.place(x=10, y=485)

living_room_button = tk.Button(control_panel_frame, command=living_room, relief=tk.RIDGE)
living_room_button.place(x=10, y=10)

bedroom_button = tk.Button(control_panel_frame, command=bedroom, relief=tk.RIDGE)
bedroom_button.place(x=10, y=120)

garage_button = tk.Button(control_panel_frame, command=garage, relief=tk.RIDGE)
garage_button.place(x=10, y=230)

background_image_path = background_images[current_bg_key]
background_image = Image.open(background_image_path)
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize to fit window
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(bedroom_frame, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

temperature_label = tk.Label(bedroom_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
temperature_label.place(x=530, y=100)

background_image_path_livingroom = background_images_lvr[current_bg_livingroom_key]
background_image_livingroom = Image.open(background_image_path_livingroom)
background_image_livingroom = background_image_livingroom.resize((800, 600), Image.Resampling.LANCZOS)
background_photo_livingroom = ImageTk.PhotoImage(background_image_livingroom)

background_label_livingroom = tk.Label(living_room_frame, image=background_photo_livingroom)
background_label_livingroom.place(x=0, y=0, relwidth=1, relheight=1)

temperature_label_livingroom = tk.Label(living_room_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
temperature_label_livingroom.place(x=140, y=150)

background_image_path_garage = "garage1.jpg"
background_image_garage = Image.open(background_image_path_garage)
background_image_garage = background_image_garage.resize((800, 600), Image.Resampling.LANCZOS)
background_photo_garage = ImageTk.PhotoImage(background_image_garage)

background_label_garage = tk.Label(garage_frame, image=background_photo_garage)
background_label_garage.place(x=0, y=0, relwidth=1, relheight=1)

temperature_label_garage = tk.Label(garage_frame, text="Nhiệt độ: --", font="Helvetica 12 bold", bg='white')
temperature_label_garage.place(x=280, y=190)

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

door_img = resize_image("door.jpg", 150, 80)
light_on_img = resize_image("light_on.jpg", 150, 80)
light_off_img = resize_image("light_off.jpg", 150, 80)
blink_img = resize_image("blink.jpg", 150, 80)
back_img = resize_image("back.jpg", 150, 80)
fan_img = resize_image("fan.jpg", 150, 80)
return_img = resize_image("back.jpg", 150, 80)
up_img = resize_image("up.jpg", 150, 80)
down_img = resize_image("down.jpg", 150, 80)
light_img = resize_image("Light.jpg",150,80)

door_button_bedroom = tk.Button(bedroom_frame, image=door_img, command=toggle_door, bd=0)
door_button_bedroom.place(x=50, y=50)

light_button = tk.Button(bedroom_frame, image=light_on_img if bedroom_light_status else light_off_img, command=toggle_bedroom_light, bd=0)
light_button.place(x=50, y=140)

blink_button = tk.Button(bedroom_frame, image=blink_img, command=bedroom_light_blink, bd=0)
blink_button.place(x=50, y=230)

back_button = tk.Button(bedroom_frame, image=back_img, command=back_to_main, bd=0)
back_button.place(x=620, y=500)

light_button_livingroom = tk.Button(living_room_frame, image=light_img, command=toggle_livingroom_light, bd=0)
light_button_livingroom.place(x=600, y=50)

btn_livingroom_blink = tk.Button(living_room_frame, image=blink_img, command=livingroom_light_blink, bd=0)
btn_livingroom_blink.place(x=600, y=140)

btn_toggle_fan = tk.Button(living_room_frame, image=fan_img, command=toggle_fan, bd=0)
btn_toggle_fan.place(x=600, y=230)

btn_door = tk.Button(living_room_frame, image=door_img, command=toggle_door, bd=0)
btn_door.place(x=600, y=320)

btn_return = tk.Button(living_room_frame, image=return_img, command=back_to_main, bd=0)
btn_return.place(x=600, y=500)
#Garage
btn_door_garage = tk.Button(garage_frame, image=(down_img if door_garage else up_img), command=garage_door, bd=0)
btn_door_garage.place(x=600, y=30)

btn_door = tk.Button(garage_frame, image=door_img, command=toggle_door, bd=0)
btn_door.place(x=600, y=120)

btn_return = tk.Button(garage_frame, image=return_img, command=back_to_main, bd=0)
btn_return.place(x=600, y=500)

radio1 = ttk.Radiobutton(control_panel_frame, image=photo1, variable=song_var, value="Song 1", command=play_song, style="Custom.TRadiobutton")
radio1.image = photo1  
radio1.place(x=620, y=190)

radio2 = ttk.Radiobutton(control_panel_frame, image=photo2, variable=song_var, value="Song 2", command=play_song, style="Custom.TRadiobutton")
radio2.image = photo2  
radio2.place(x=690, y=190)
    
W.after(1000, read_temperature)

show_frame(password_frame)

def close_serial():
    if s1.is_open:
        s1.close()

def on_closing():
    close_serial()
    W.destroy()

W.protocol("WM_DELETE_WINDOW", on_closing)

W.mainloop()
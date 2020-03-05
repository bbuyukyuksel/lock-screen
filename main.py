import subprocess
import time
import os
import datetime
import threading

from pynput import mouse as Mouse
from pynput import keyboard as Keyboard

from PIL import Image, ImageTk
import cv2
import numpy as np


def show():
    gif = Image.open('trol.gif', 'r')
    frames = []
    try:
        while 1:
            frames.append(gif.copy())
            gif.seek(len(frames))
    except EOFError:
        pass

    cv2.namedWindow("Merhaba :)", cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("win1", 150,150);


    opencvImage = cv2.cvtColor(np.array(frames[0]), cv2.COLOR_RGB2BGR)
    scale_percent = 300 # percent of original size
    width = int(opencvImage.shape[1] * scale_percent / 100)
    height = int(opencvImage.shape[0] * scale_percent / 100)
    dim = (width, height)


    for frame in frames:
        #open_cv_image = np.array(frame) 
        #print(open_cv_image.shape)
        opencvImage = cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR)
        ret,th1 = cv2.threshold(opencvImage,10,255,cv2.THRESH_BINARY)
        resized = cv2.resize(th1, dim, interpolation = cv2.INTER_AREA)
        cv2.imshow("Merhaba :)", resized)
        cv2.waitKey(50)
    
    cv2.destroyAllWindows()

def counter(lock_date, sec):
    diff = datetime.datetime.now() - lock_date
    while diff.seconds > 0:
        print("Kontrol başlatılıyor .. ", datetime.datetime.now() - lock_date, end="\r")
        diff = datetime.datetime.now() - lock_date

def on_move(x, y):
    global time_out_flag, lock_screen

    if time_out_flag:
        lock_screen = True

def on_press(key):
    global time_out_flag, lock_screen
    global m_listener
    global kb_listener

    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
    if key == Keyboard.Key.esc:
        print("ESC")
        kb_listener.stop()
        m_listener.stop()

    if time_out_flag:
        lock_screen = True


if __name__ == '__main__':
    global lock_screen
    global time_out_flag
    global m_listener
    global kb_listener
    
    iter = 0
    time_out_flag = False
    lock_screen = False
    timeout_counter = 0

    mouse = Mouse.Controller()
    keyboard = Keyboard.Controller()

    
    kb_listener = Keyboard.Listener(on_press=on_press)
    m_listener = Mouse.Listener(on_move=on_move)
    
    m_listener.start()
    kb_listener.start()
    
    while True:
        task = subprocess.Popen('ping -n 1 192.168.1.200 -w 500', stdout=subprocess.PIPE, shell=True)
        time.sleep(0.5)
        response = task.stdout.read().decode()

        if "Request timed out." in response or not "Maximum" in response:
            timeout_counter += 1
            print(f"[{timeout_counter}] Alert !", datetime.datetime.now())
            time.sleep(1)

        else:
            print("_"*20)
            print(response)
            print("Cihaz bağlı", datetime.datetime.now(), end="\r")
            timeout_counter = 0

        if timeout_counter == 4:
            time_out_flag = True
            timeout_counter = 0
            print("Kontrol 10 saniye sonra tekrar başlayacak.")

        if lock_screen:
            lock_screen = False
            time_out_flag = False
            show()
            os.system("rundll32.exe user32.dll,LockWorkStation")

        time.sleep(1)

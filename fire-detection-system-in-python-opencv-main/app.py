from flask import Flask, render_template, Response, redirect, url_for
import cv2
import numpy as np
import pygame
import threading

app = Flask(__name__)

# Constants
ALARM_SOUND_FILE = '/Users/sandeshshejwal/Documents/BE PROJECT/fire-detection-system-in-python-opencv-main/alarm-sound.mp3'
LOWER_THRESHOLD = [18, 50, 50]
UPPER_THRESHOLD = [35, 255, 255]
NO_RED_THRESHOLD = 15000

# Global variables
Alarm_Status = False
Fire_Reported = 0
Fire_Detection_Started = False

def play_alarm_sound_function():
    pygame.mixer.init()
    pygame.mixer.music.load(ALARM_SOUND_FILE)
    pygame.mixer.music.play(-1)  # -1 means play indefinitely

    while True:
        pass  # Keep the thread running

def fire_detection():
    global Alarm_Status, Fire_Reported
    video = cv2.VideoCapture("/Users/sandeshshejwal/Documents/BE PROJECT/fire-detection-system-in-python-opencv-main/test1.mp4")  # Use 0 for the default camera

    while True:
        grabbed, frame = video.read()
        if not grabbed:
            break

        frame = cv2.resize(frame, (640, 480))

        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        lower = np.array(LOWER_THRESHOLD, dtype="uint8")
        upper = np.array(UPPER_THRESHOLD, dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)

        output = cv2.bitwise_and(frame, hsv, mask=mask)

        no_red = cv2.countNonZero(mask)

        if int(no_red) > NO_RED_THRESHOLD:
            Fire_Reported = Fire_Reported + 1

        if Fire_Reported >= 1:

            if not Alarm_Status:
                threading.Thread(target=play_alarm_sound_function).start()
                Alarm_Status = True

        _, jpeg = cv2.imencode('.jpg', output)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        if not Fire_Detection_Started:
            break

    video.release()

@app.route('/')
def index():
    background_image_url = "/static/cctvimage.jpeg"
    return render_template('index.html', background_image_url=background_image_url)

@app.route('/start_fire_detection', methods=['POST'])
def start_fire_detection():
    global Fire_Detection_Started, Alarm_Status, Fire_Reported
    Fire_Detection_Started = True
    Alarm_Status = False
    Fire_Reported = 0
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    return Response(fire_detection(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

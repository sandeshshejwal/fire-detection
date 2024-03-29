import cv2
import numpy as np
import pygame
import threading

# Constants
ALARM_SOUND_FILE = '/Users/sandeshshejwal/Documents/BE PROJECT/fire-detection-system-in-python-opencv-main/alarm-sound.mp3'
LOWER_THRESHOLD = [18, 50, 50]
UPPER_THRESHOLD = [35, 255, 255]
NO_RED_THRESHOLD = 15000

# Global variables
Alarm_Status = False
Fire_Reported = 0

def play_alarm_sound_function():
    pygame.mixer.init()
    pygame.mixer.music.load(ALARM_SOUND_FILE)
    pygame.mixer.music.play(-1)  # -1 means play indefinitely

    while True:
        pass  # Keep the thread running

def main():
    global Alarm_Status, Fire_Reported  
    video = cv2.VideoCapture("/Users/sandeshshejwal/Documents/BE PROJECT/fire-detection-system-in-python-opencv-main/test1.mp4") 

    while True:
        (grabbed, frame) = video.read()
        if not grabbed:
            break

        frame = cv2.resize(frame, (960, 540))

        blur = cv2.GaussianBlur(frame, (21, 21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        lower = np.array(LOWER_THRESHOLD, dtype="uint8")
        upper = np.array(UPPER_THRESHOLD, dtype="uint8")

        mask = cv2.inRange(hsv, lower, upper)

        output = cv2.bitwise_and(frame, hsv, mask=mask)

        no_red = cv2.countNonZero(mask)

        if int(no_red) > NO_RED_THRESHOLD:
            Fire_Reported = Fire_Reported + 1

        cv2.imshow("output", output)

        if Fire_Reported >= 1:

            if not Alarm_Status:
                threading.Thread(target=play_alarm_sound_function).start()
                Alarm_Status = True

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    main()

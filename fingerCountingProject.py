import cv2
import time
import sys
import os
from keras.utils import img_to_array



# Adjust the system path to include the Emotion and Volume folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), r'D:\Python Files\MEDIBOT_FINAL\Emotion')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), r'D:\Python Files\MEDIBOT_FINAL\Volume')))


import handTrackingModule as htm
from test import Emomain
from main import volmain
z=[]
def getNumber(ar):
    s = ""
    for i in ar:
        s += str(ar[i]) 
    if s == "00000":
        return 0
    elif s == "01000": 
        # Call Emomain function from the emotion module
        return 1
    elif s == "01100":
        # Call VolMain function from the hand module
        return 2
    elif s == "01110":
        return 3
    elif s == "01111":
        return 4
    elif s == "11111":
        return 5

def main():
    wcam, hcam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wcam)
    cap.set(4, hcam)
    pTime = 0
    lastDetectionTime = 0
    detectionInterval = 5  # seconds

    detector = htm.handDetector(detectionCon=0.75)

    while True:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=False)
        
        tipId = [4, 8, 12, 16, 20]
        cTime = time.time()

        if len(lmList) != 0 and cTime - lastDetectionTime >= detectionInterval:
            fingers = []
            # Thumb
            if lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # 4 fingers
            for id in range(1, len(tipId)):
                if lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            number = getNumber(fingers)
            z.append(number)
            print(z)  # Print the number value in the output
            lastDetectionTime = cTime  # Update last detection time

            if number == 1:
                cap.release()  # Release the camera
                cv2.destroyAllWindows()  # Close any OpenCV windows
                Emomain()  # Call Emomain function from the emotion module
                cap = cv2.VideoCapture(0)  # Re-initialize the camera
                cap.set(3, wcam)
                cap.set(4, hcam)
                detector = htm.handDetector(detectionCon=0.75)
            elif number == 2:
                cap.release()  # Release the camera
                cv2.destroyAllWindows()  # Close any OpenCV windows
                volmain()  # Call VolumeMain function from the volume module
                cap = cv2.VideoCapture(0)  # Re-initialize the camera
                cap.set(3, wcam)
                cap.set(4, hcam)
                detector = htm.handDetector(detectionCon=0.75)

            cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(number), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 20)

        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return z
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

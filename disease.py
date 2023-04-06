import cv2
import numpy as np

rp_mode = True

#if rp_mode :
#    import RPi.GPIO as GPIO
#    GPIO.setmode(GPIO.BCM)
#    GPIO.setup(23, GPIO.OUT)
#    GPIO.setwarnings(False)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.putText(frame, 'Disease Detection', 
                        (10, height-10),font,1,(0,0,255),
                        3, cv2.LINE_AA)
    
    frame = cv2.GaussianBlur(frame, (5,5), 0)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lower_sehat = np.array([39,225,20])
    upper_sehat = np.array([60,255,255])
    mask_sehat = cv2.inRange(hsv,lower_sehat,upper_sehat)
    result_sehat = cv2.bitwise_and(frame,frame,mask=mask_sehat)

    lower_kursehat = np.array([32,225,20])
    upper_kursehat = np.array([39,255,255])
    mask_kursehat = cv2.inRange(hsv,lower_kursehat,upper_kursehat)
    result_kursehat = cv2.bitwise_and(frame,frame,mask=mask_kursehat)

    lower_tidsehat = np.array([25,225,20])
    upper_tidsehat = np.array([31,255,255])
    mask_tidsehat = cv2.inRange(hsv,lower_tidsehat,upper_tidsehat)
    result_tidsehat = cv2.bitwise_and(frame,frame,mask=mask_tidsehat)

    contours, hierarchy = cv2.findContours(mask_sehat,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (82,168,50),3)
                cv2.putText(frame, "Sehat", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (82,168,50), 3, cv2.LINE_AA)
                cv2.imwrite("image_color.jpg", frame)
                print ("Tanaman terdeteksi Sehat")
                file = open("color.txt", "w")
                file.write("Sehat")
                file.close()
    
    contours, hierarchy = cv2.findContours(mask_kursehat,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (88,214,166),3)
                cv2.putText(frame, "Kurang Sehat", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (88,214,166), 3, cv2.LINE_AA)
                cv2.imwrite("image_color.jpg", frame)
                print ("Tanaman terdeteksi kurang sehat")
                file = open("color.txt", "w")
                file.write("Kurang Sehat")
                file.close()

    contours, hierarchy = cv2.findContours(mask_tidsehat,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x,y), (x+w,y+h), (26,234,237),3)
                cv2.putText(frame, "Tidak Sehat", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (26,234,237), 3, cv2.LINE_AA)
                cv2.imwrite("image_color.jpg", frame)
                print ("Terdeteksi Penyakit")
                file = open("color.txt", "w")
                file.write("Tidak Sehat")
                file.close()

    cv2.imshow("Disease Detection",frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

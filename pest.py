import cv2
import numpy as np
import time 


rp_mode=True
insectDetected = 0

def nothing(x):
    pass

cap = cv2.VideoCapture(0)

#cv2.namedWindow('Frame')
#cv2.createTrackbar("Scale","Frame",11,20,nothing)
#cv2.createTrackbar("Neighbours","Frame",0,20,nothing)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    pest_classifer = cv2.CascadeClassifier("dataset\classifier\cascade.xml")

    font = cv2.FONT_HERSHEY_SIMPLEX
    frame = cv2.putText(frame, 'Pest Detection', 
                        (10, height-10),font,1,(0,0,255),
                        3, cv2.LINE_AA)
    
    #scale = cv2.getTrackbarPos("Scale","Frame")
    #neighbours = cv2.getTrackbarPos("Neighbours","Frame")

    pests = pest_classifer.detectMultiScale(gray,1.4,14)

    for rect in pests:
        (x,y,w,h) = rect
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)
        cv2.putText(frame, "Hama Terdeteksi", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,255), 3, cv2.LINE_AA)
        cv2.imwrite("image_insects.jpg", frame)
        print ("image insects saved")
        #if rp_mode :
        #    GPIO.output(23, GPIO.LOW)
        insectDetected = time.time()

        file = open("insect.txt", "w")
        file.write("Terdeteksi Adanya Hama")
        file.close()


    if time.time() - insectDetected > 3 :
        #if rp_mode :
        #    GPIO.output(23, GPIO.HIGH)
        file = open("insect.txt", "w")
        file.write("Tidak Terdeteksi Adanya Hama")
        file.close()

    cv2.imshow("Pest Detection",frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

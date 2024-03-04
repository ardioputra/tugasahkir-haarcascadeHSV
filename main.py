import cv2
import numpy as np
import time 

rp_mode=True

pestDetected = 0


cap = cv2.VideoCapture(0)


while True:
    ret, frameDisease = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    font = cv2.FONT_HERSHEY_SIMPLEX
    frameDisease = cv2.putText(frameDisease, 'Disease Detection', 
                        (10, height-10),font,1,(42,23,255),
                        3, cv2.LINE_AA)
    
    frameDisease = cv2.GaussianBlur(frameDisease, (5,5), 0)
    hsv = cv2.cvtColor(frameDisease,cv2.COLOR_BGR2HSV)

    lower_sehat = np.array([30,60,20])
    upper_sehat = np.array([60,255,255])
    mask_sehat = cv2.inRange(hsv,lower_sehat,upper_sehat)
    result_sehat = cv2.bitwise_and(frameDisease,frameDisease,mask=mask_sehat)

    lower_kursehat = np.array([29,60,20])
    upper_kursehat = np.array([25,255,255])
    mask_kursehat = cv2.inRange(hsv,lower_kursehat,upper_kursehat)
    result_kursehat = cv2.bitwise_and(frameDisease,frameDisease,mask=mask_kursehat)

    lower_tidsehat = np.array([24,60,20])
    upper_tidsehat = np.array([20,255,255])
    mask_tidsehat = cv2.inRange(hsv,lower_tidsehat,upper_tidsehat)
    result_tidsehat = cv2.bitwise_and(frameDisease,frameDisease,mask=mask_tidsehat)

    contours, hierarchy = cv2.findContours(mask_sehat,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frameDisease, (x,y), (x+w,y+h), (82,168,50),3)
                cv2.putText(frameDisease, "Sehat", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (82,168,50), 3, cv2.LINE_AA)
                cv2.imwrite("image_color.jpg", frameDisease)
                print ("Tanaman terdeteksi Sehat")
                file = open("color.txt", "w")
                file.write("Sehat")
                file.close()
    
    contours, hierarchy = cv2.findContours(mask_kursehat,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frameDisease, (x,y), (x+w,y+h), (88,214,166),3)
                cv2.putText(frameDisease, "Kurang Sehat", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (88,214,166), 3, cv2.LINE_AA)
                cv2.imwrite("image_color.jpg", frameDisease)
                print ("Tanaman terdeteksi kurang sehat")
                file = open("color.txt", "w")
                file.write("Kurang Sehat")
                file.close()

    contours, hierarchy = cv2.findContours(mask_tidsehat,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        for contour in contours:
            if cv2.contourArea(contour)>1000:
                x,y,w,h = cv2.boundingRect(contour)
                cv2.rectangle(frameDisease, (x,y), (x+w,y+h), (26,234,237),3)
                cv2.putText(frameDisease, "Tidak Sehat", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1, (26,234,237), 3, cv2.LINE_AA)
                cv2.imwrite("image_color.jpg", frameDisease)
                print ("Terdeteksi Penyakit")
                file = open("color.txt", "w")
                file.write("Tidak Sehat")
                file.close()

    ret, framePest = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    gray = cv2.cvtColor(framePest, cv2.COLOR_BGR2GRAY)

    font = cv2.FONT_HERSHEY_SIMPLEX
    framePest = cv2.putText(framePest, 'Pest Detection', 
                        (10, height-10),font,1,(17,135,0),
                        3, cv2.LINE_AA)
    
    pest_classifer = cv2.CascadeClassifier("dataset_terbaru\classifier\cascade.xml")
    pests = pest_classifer.detectMultiScale(gray,1.1,5)

    for rect in pests:
        (x,y,w,h) = rect
        framePest = cv2.rectangle(framePest, (x,y), (x+w, y+h), (0,0,255), 2)
        cv2.putText(framePest, "Hama Terdeteksi", (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0,0,255), 3, cv2.LINE_AA)
        cv2.imwrite("image_pests.jpg", framePest)
        print ("image pests saved")
        #if rp_mode :
        #    GPIO.output(23, GPIO.LOW)
        pestDetected = time.time()

        file = open("pest.txt", "w")
        file.write("Terdeteksi Adanya Hama")
        file.close()


    if time.time() - pestDetected > 3 :
        #if rp_mode :
        #    GPIO.output(23, GPIO.HIGH)
        file = open("pest.txt", "w")
        file.write("Tidak Terdeteksi Adanya Hama")
        file.close()

    cv2.imshow("Pest Detection",framePest)
    cv2.imshow("Disease Detection",frameDisease)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import requests
import time
import serial

rp_mode = True
if rp_mode :
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)

DASH_URL = 'https://iotprojectku.my.id/dashboard/add_image'
HIS_URL = 'https://iotprojectku.my.id/history/add_history'
# DASH_URL = 'http://192.168.167.51:8080/dashboard/add_image'
# HIS_URL = 'http://192.168.167.51:8080/history/add_history'
print ("Project Ready To Use")  

if rp_mode :
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    ser.reset_input_buffer()

myTimes = time.time()
print (time.time())
value1 = 0
value2 = 0
value3 = 0
value4 = 0
statustds = "-"

def dashboard():
    print ("dashboard update")

    with open('pest.txt', 'r') as f:
        insectData = f.read()
        if insectData == "Terdeteksi Adanya Hama":
            dataInsect = "Sudah Ditangani"
        else :
            dataInsect = "Tidak Perlu Ditangani"
    print(insectData)

    with open('color.txt', 'r') as f:
        colorData = f.read()
        if colorData == "Sehat":
            dataColor = "Tidak Perlu Penanganan"
        else:
            dataColor = "Perlu Penanganan"
    print(colorData)

    data = {
        'abc': 'xyz',
        'temp': value1,
        'hum': value2,
        'tds': value3,
        'statushama': insectData,
        'statuspenyakit' : colorData,
        'penangananhama' : dataInsect,
        'penangananpenyakit' : dataColor,
        'statustds' : statustds
    }
    files = {
        'image': ('image_color.jpg', open('image_color.jpg', 'rb'), 'image/jpg'),
        'image_insect': ('image_pests.jpg', open('image_pests.jpg', 'rb'), 'image/jpg')
    }

    response = requests.post(DASH_URL, data=data, files=files)
    print(response.json())

def history():
    print ("histories update")
    with open('pest.txt', 'r') as f:
        insectData = f.read()
        if insectData == "Terdeteksi Adanya Hama":
            dataInsect = "Sudah Ditangani"
        else :
            dataInsect = "Tidak Perlu Ditangani"
    print(insectData)

    with open('color.txt', 'r') as f:
        colorData = f.read()
        if colorData == "Sehat":
            dataColor = "Tidak Perlu Penanganan"
        else:
            dataColor = "Perlu Penanganan"
    print(colorData)

    data = {
        'abc': 'xyz',
        'temp': value1,
        'hum': value2,
        'tds': value3,
        'statushama': insectData,
        'statuspenyakit' : colorData,
        'penangananhama' : dataInsect,
        'penangananpenyakit' : dataColor,
        'statustds' : statustds
    }
    files = {
        'image': ('image_color.jpg', open('image_color.jpg', 'rb'), 'image/jpg'),
        'image_insect': ('image_pests.jpg', open('image_pests.jpg', 'rb'), 'image/jpg')
    }

    response = requests.post(HIS_URL, data=data, files=files)
    print(response.json())
    print()

while True:
    if rp_mode :
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            values = line.split('#')
            
            value1 = (values[1])
            value2 = (values[2])
            value3 = (values[0])
            value4 = (values[3])

            if value4 == "tidakbaikdibawah":
                statustds = "Tidak Baik"
            elif value4 == "baik":
                statustds = "Baik"
            elif value4 == "tidakbaikdiatas":
                statustds = "Tidak Baik"

            if rp_mode:
                if value4 == "tidakbaikdiatas":
                    GPIO.output(24, GPIO.LOW)
                else :
                    GPIO.output(24, GPIO.HIGH)

    if (time.time() - myTimes > 20):
        history()
        myTimes = time.time()

    dashboard()
    time.sleep(1)

from picamera.array import PiRGBArray
from picamera import PiCamera
from socketIO_client import SocketIO, LoggingNamespace
from envirophat import light, motion, weather, analog, leds
import time
import base64
import json
from io import BytesIO
from PIL import Image

time.sleep(10)
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)

def run():
        with SocketIO('4d36143b.ngrok.io', 80, LoggingNamespace) as socketIO:
                print 'got connection'
                # capture frames from the camera
                for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                        time.sleep(0.5)
                        # grab the raw NumPy array representing the image, then initialize the timestamp
                        # and occupied/unoccupied text
                        image = frame.array
                        pil_img = Image.fromarray(image)
                        buff = BytesIO()
                        pil_img.save(buff, format="JPEG")
                        base64_image = base64.b64encode(buff.getvalue()).decode('utf-8')
                        # clear the stream in preparation for the next frame
                        rawCapture.truncate(0)
                        # print base64_image
                        temperature = 32 + round(weather.temperature())
                        air_pressure = weather.pressure()
                        altitude = weather.altitude()
                        output = json.dumps({'image': base64_image, 'username':'mscarn', 'business':'1', 'temperature': temperature, 'air_pressure': air_pressure, 'altitude': altitude})
                        socketIO.emit('stream', output)

run()

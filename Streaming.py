import time
import cv2 
from flask import Flask, render_template, Response

import numpy as np 
from PIL import ImageGrab

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen():
    """Video streaming generator function."""
    # Read until video is completed
    while(True):
      # Capture frame-by-frame
        # capture computer screen
        img = ImageGrab.grab()
        # convert image to numpy array
        img_np = np.array(img)
        # convert color space from BGR to RGB
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)


        img2 = cv2.resize(frame, (0,0), fx=0.5, fy=0.5) 
        frame2 = cv2.imencode('.jpg', img2)[1].tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame2 + b'\r\n')
        time.sleep(0.1)
        

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

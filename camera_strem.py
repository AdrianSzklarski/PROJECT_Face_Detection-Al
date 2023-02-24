import tkinter as tk
import logging as logger
import cv2
from datetime import datetime
import PIL.Image, PIL.ImageTk

import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import time
import logging as log
import datetime as dt
import moviepy.editor as moviepy


class CameraStrem:
    def __init__(self, root, camera=0):
        self.root = root
        self.delay = 15
        self.video_source = camera  # commit 1
        self.capture = CaptureAvi(self.video_source)

        # Create Canvas for *.*avi
        self.canvas = tk.Canvas(self.root, width=self.capture.width, height=self.capture.height)
        self.canvas.pack()

        self.get_set_window()
        self.update()

    def get_set_window(self):
        '''Set window of *.*avi'''
        self.root.title("Face Detection create by A.Szklarski 02.2023")
        self.root.geometry('640x480')

    def update(self):
        # Get a frame from the video source
        ret, frame = self.capture.get_frames()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.root.after(self.delay, self.update)


class CaptureAvi:
    def __init__(self, camera=0):
        self.capture = cv2.VideoCapture(camera)  # commit 2
        if not self.capture.isOpened():
            raise ValueError("Attention, video failed to open", camera)

        self.get_dimensions()

    def get_dimensions(self):
        '''Download window dimensions *.*avi'''
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frames(self):
        '''Video opening, image analysis'''
        anterior = 0
        self.dataXML = "data.xml"

        # https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
        self.classifier = cv2.CascadeClassifier(self.dataXML)

        # https://zetcode.com/python/logging/
        logger.basicConfig(filename='infoCamera.log', level=logger.INFO)

        # open camera
        if self.capture.isOpened():
            # https://pythonprogramming.net/loading-video-python-opencv-tutorial/
            self.ret, self.frame = self.capture.read()
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            if self.ret:
                # https://opencv-tutorial.readthedocs.io/en/latest/face/face.html
                faces = self.classifier.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                for (x, y, w, h) in faces:
                    # https://docs.opencv.org/4.x/dc/da5/tutorial_py_drawing_functions.html
                    cv2.rectangle(self.frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    if anterior != len(faces):
                        logger.info("faces: " + str(len(faces)) + " at " + str(datetime.now()))

                    return (self.ret, cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB))
                else:
                    return (self.ret, None)
            else:
                return (self.ret, None)

    def __del__(self):
        if self.capture.isOpened():
            self.capture.release()


# Test run, after delete
if __name__ == '__main__':
    app = tk.Tk()
    CameraStrem(app)
    app.mainloop()
#  My commits:

#  no 1:
#  definition of 'cv2.VideoCapture(0)', camera=0 so:
'''This is the camera index, which is used to select different cameras if you have more 
than one connected. By default, 0 is your primary. if I had two cameras, my index = 1'''

#  no 2: define a video capture object

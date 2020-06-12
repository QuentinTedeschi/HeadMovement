from imutils import face_utils
import numpy as np
import dlib
import cv2
import os
import csv

videolist = ["Head_Nodding", "Head_Sideways_Shake", "Head_Tilt_(left_right)", "nod", "shake"]
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

source = "./Videos/"

for folder in os.listdir(source):
    faillist = []
    if folder in videolist:
        for video in os.listdir(source + folder):
            cap = cv2.VideoCapture(source + folder + "/" + video)
            name = "./LandmarksCSV/" + video[:-4] + ".csv"
            csvfile = open(name, "w+", newline = "")
            writer = csv.writer(csvfile, delimiter = ';')
            counter = 0
            while(True):
                ret, frame = cap.read()
                if ret == False:
                    break
                marklist = []
                
                height, width, _ = frame.shape
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
    
                rects = detector(gray, 1)
                for (i, rect) in enumerate(rects):

                    marks = predictor(gray, rect)
                    marks = face_utils.shape_to_np(marks)
        
                    (x, y, w, h) = face_utils.rect_to_bb(rect)

                    for (x, y) in marks[0]:
                        if height != 640:
                            x = x * height / 640
                            x = int(x)
                        if width != 480:
                            y = y * width / 480
                            y = int(y)
                        marklist.append(x)
                        marklist.append(y)
                    
                if marklist == []:
                    continue    
                writer.writerow(marklist)
                counter = counter + 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            csvfile.close()
            cap.release()
            cv2.destroyAllWindows()
            if counter == 0:
                os.remove(name)
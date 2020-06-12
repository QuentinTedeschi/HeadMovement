from imutils import face_utils
import numpy as np
import dlib
import cv2
import os

videolist = ["Head_Nodding", "Head_Sideways_Shake", "Head_Tilt_(left_right)"]
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

for folder in os.listdir("./Videos"):
    if folder in videolist:
        for video in os.listdir("./Videos/" + folder):
            cap = cv2.VideoCapture("./Videos/" + folder + "/" + video)
            count = 0
            try:
                if not os.path.exists("./Landmarks/" + video[:-4] + "/"):
                    os.makedirs("./Landmarks/" + video[:-4] + "/")
            except OSError:
                ("Error creating path")
                
            while(True):
                ret, frame = cap.read()
                if ret == False:
                    break
                name = "./Landmarks/" + video[:-4] + "/" + str(count).zfill(5) + ".jpg"
                
                height, width, _ = frame.shape
                
                blank = np.zeros((height,width,1), np.uint8)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
    
                rects = detector(gray, 1)
                for (i, rect) in enumerate(rects):

                    marks = predictor(gray, rect)
                    marks = face_utils.shape_to_np(marks)
        
                    (x, y, w, h) = face_utils.rect_to_bb(rect)

                    for (x, y) in marks:
                        cv2.circle(blank, (x, y), 1, 255, -1)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                cv2.imwrite(name, blank)
                count += 1
            cap.release()
            cv2.destroyAllWindows()
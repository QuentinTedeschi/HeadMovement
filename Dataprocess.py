from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2

width = 500

cap = cv2.VideoCapture('Data/Videos/Head_Nodding/P1_P2_1402_C15501157849.mp4')

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Data/shape_predictor_68_face_landmarks.dat")

processed = []

while(cap.isOpened()):
    ret, image = cap.read()
    
    image = imutils.resize(image, width)
    
    blank = np.zeros((width,width,3), np.uint8)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    rects = detector(gray, 1)
    for (i, rect) in enumerate(rects):

        marks = predictor(gray, rect)
        marks = face_utils.shape_to_np(marks)
        
        (x, y, w, h) = face_utils.rect_to_bb(rect)

        for (x, y) in marks:
            cv2.circle(blank, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("Output", blank)
        
        processed.append(marks)
        

    if cv2.waitKey(1) & 0xFF == ord('q'):
        processed = np.stack(processed)
        np.save('test.npy', processed)
        print(processed.shape)
        break

cap.release()
cv2.destroyAllWindows()
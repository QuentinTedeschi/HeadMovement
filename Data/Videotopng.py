import cv2
import os
import csv

train_file = "./Annotations/TrainequalAMI.csv"
valid_file = "./Annotations/ValidequalAMI.csv"
video_folder = "./VideosAMI/"

validfile = csv.reader(open(valid_file, "r"), delimiter = ";")

for row in validfile:
    print(row)
    cap = cv2.VideoCapture(video_folder + row[1] + "/" + row[0] + ".mp4")
    count = 0
    try:
        if not os.path.exists("./Videos/" + row[0] + "/"):
            os.makedirs("./Videos/" + row[0] + "/")
    except OSError:
        ("Error creating path")
        
    while(True):
        ret, frame = cap.read()
        if ret == False:
            break
        name = "./Videos/" + row[0] + "/" + str(count).zfill(5) + ".jpg"
        print(name)
        cv2.imwrite(name, frame)
        count += 1
    cap.release()
    cv2.destroyAllWindows()
    

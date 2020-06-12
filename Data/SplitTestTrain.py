import os
import csv
import random

viddict = {}
trainlist = []
validlist = []
    
for folder in os.listdir("./VideosAMI/"):
    folderlist = []
    for file in os.listdir("./VideosAMI/" + folder):
        file = file[:-4]
        if not os.path.exists("./LandmarksCSV/AMI/" + file + ".csv"):
            continue
        test = open("./LandmarksCSV/AMI/" + file + ".csv")
        testread = csv.reader(test)
        lines = len(list(testread))
        if lines == 1:
            continue
        folderlist.append(file)
        viddict[file] = folder
    random.shuffle(folderlist)
    folderlist = folderlist[:750]
    trainindex = int(len(folderlist) * 0.8)
    training, valid = folderlist[:trainindex], folderlist[-(len(folderlist)-trainindex):]
    trainlist = trainlist + training
    validlist = validlist + valid
    
random.shuffle(trainlist)
random.shuffle(validlist)

with open("./Annotations/TrainequalAMI.csv", "w", newline = "") as csvfile:
    writer = csv.writer(csvfile, delimiter = ';')
    for file in trainlist:
        writer.writerow([file, viddict[file]])

with open("./Annotations/ValidequalAMI.csv", "w", newline = "") as csvfilebis:
    writer = csv.writer(csvfilebis, delimiter = ';')
    for file in validlist:
        writer.writerow([file, viddict[file]])
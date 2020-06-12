import os
import csv
import pandas as pd
import numpy as np

train_file = "../../Data/Annotations/Train.csv"
valid_file = "../../Data/Annotations/Valid.csv"
video_folder = "../../Data/LandmarksCSV/"
input_shape = (100, 136, 1)
class_nbr = 3

class CSV_Data_Loader():
    def __init__(self, Train_File, Valid_File, Video_Folder, inputshape, class_nbr, deriv, point):
        self.trainfile = open(Train_File, "r")
        self.validfile = open(Valid_File, "r")
        self.videofolder = Video_Folder
        self.inputshape = inputshape
        self.class_nbr = class_nbr
        self.deriv = deriv
        self.point = point
    def trainreader(self):
        labellist = []
        csvlist = []
        read = csv.reader(self.trainfile, delimiter = ";")
        for row in read:
            csvlist.append(row[0])
            if row[1] in ["Head_Nodding", "nod"]:
                if self.class_nbr == 3:
                    labellist.append([1,0,0])
                elif self.class_nbr == 2:
                    labellist.append([1,0])
            if row[1] in ["Head_Sideways_Shake", "shake"]:
                if self.class_nbr == 3:
                    labellist.append([0,1,0])
                elif self.class_nbr == 2:
                    labellist.append([0,1])
            if row[1] == "Head_Tilt_(left_right)":
                if self.class_nbr == 3:
                    labellist.append([0,0,1])
                elif self.class_nbr == 2:
                    labellist.append([0,1])
        labellist = np.asarray(labellist)
        return csvlist, labellist
    
    def validreader(self):
        labellist = []
        csvlist = []
        read = csv.reader(self.validfile, delimiter = ";")
        for row in read:
            csvlist.append(row[0])
            if row[1] in ["Head_Nodding", "nod"]:
                if self.class_nbr == 3:
                    labellist.append([1,0,0])
                elif self.class_nbr == 2:
                    labellist.append([1,0])
            if row[1] in ["Head_Sideways_Shake", "shake"]:
                if self.class_nbr == 3:
                    labellist.append([0,1,0])
                elif self.class_nbr == 2:
                    labellist.append([0,1])
            if row[1] == "Head_Tilt_(left_right)":
                if self.class_nbr == 3:
                    labellist.append([0,0,1])
                elif self.class_nbr == 2:
                    labellist.append([0,1])
        labellist = np.asarray(labellist)
        return csvlist, labellist
    
    def csvtonumpy(self, csv):
        csvlist = []
        for file in csv:
            path = self.videofolder + file + ".csv"
            df = pd.read_csv(path, usecols = [i for i in range(136)], sep = ";", index_col = False)
            df = df.values.tolist()
            # csvlist.append(list(np.genfromtxt(path, delimiter = ";")))
            if not df:
                print("Problem?")
                print(path)
            csvlist.append(df)
        if self.deriv == False:
            zeroes = [0] * 136
        if self.deriv == True:
            zeroes = [0] * 272
        if self.deriv == True:
            csvlist = self.differential(csvlist)
        paddedlist = []
        for element in csvlist:
            while len(element) < self.inputshape[0]:
                element.append(zeroes)
            if len(element) > self.inputshape[0]:
                element = element[:self.inputshape[0]]
            paddedlist.append(element)
        if self.point:
            paddedlist = self.take_points(paddedlist)
        numpy_array = np.asarray(paddedlist)
        if len(self.inputshape) == 3:
            if self.inputshape[2] == 1:
                numpy_array = numpy_array[..., np.newaxis]
            if self.inputshape[2] == 2:
                x = numpy_array[:, :, 0::2]
                y = numpy_array[:, :, 1::2]
                numpy_array = np.stack((x, y), axis = 3)
        print(numpy_array.shape)
        return numpy_array
    
    def take_points(self, padlist):
        new_padlist = []
        for file in padlist:
            new_file = []
            for row in file:
                new_row = []
                for i in self.point:
                    new_row.append(row[2*i])
                    new_row.append(row[2*i +1])
                if self.deriv == True:
                    for i in self.point:
                        new_row.append(row[2*i + 135])
                        new_row.append(row[2*i + 136])
                new_file.append(new_row)
            new_padlist.append(new_file)
        return new_padlist
    
    def differential(self, data):
        newdata = []
        for file in data:
            newfile = []
            prev = file[0]
            for row in file[1:]:
                diff = [np.subtract(r, p) for (r, p) in zip(row, prev)]
                prev = row
                row = row + diff
                newfile.append(row)
            newdata.append(newfile)
        return newdata
        
if __name__ == "__main__":
    point = [0, 65, 67]
    test = CSV_Data_Loader(train_file, valid_file, video_folder, input_shape, class_nbr, True, point)
    csvlist, labellist = test.trainreader()
    numpy = test.csvtonumpy(csvlist)
    print(numpy.shape, labellist.shape)
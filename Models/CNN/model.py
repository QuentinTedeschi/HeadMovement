from configparser import ConfigParser
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, BatchNormalization
import matplotlib.pyplot as plt
from CSVreader import CSV_Data_Loader
from ast import literal_eval
import os
from shutil import copyfile

def Register(model, modelname):
    if not os.path.exists(modelname):
        os.mkdir(modelname)
    # summarize history for accuracy
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy ' + str(max(history.history['val_accuracy'])))
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(modelname + "/" + modelname + "_accurary.png")
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig(modelname + "/" + modelname + "_loss.png")
    copyfile("config.ini", modelname + "/" + "config.ini")
    
parser = ConfigParser()
parser.read('config.ini')

train_file = parser.get("Files", "train_file")

valid_file = parser.get("Files", "valid_file")

video_folder = parser.get("Files", "video_folder")

kernelsize = parser.get("Model", "kernel_size")
kernelsize = literal_eval(kernelsize)

inputshape = parser.get("Model", "input_size")
inputshape = list(literal_eval(inputshape))

class_nbr = parser.get("Model", "class_nbr")
class_nbr = int(class_nbr)

batch_size = parser.get("Training", "batchsize")
batch_size = int(batch_size)

epoch = parser.get("Training", "epoch")
epoch = int(epoch)

name = parser.get("Register", "name")

deriv = parser.get("Landmarks", "derivative")
deriv = literal_eval(deriv)

point = parser.get("Landmarks", "points")
point = literal_eval(point)
if point:
    if len(inputshape) == 3:
        if inputshape[2] == 2:
            inputshape[1] = len(point)
        if inputshape[2] == 1:
            inputshape[1] = len(point) * 2
    else:
        inputshape[1] = len(point) * 2

if deriv == True:
    inputshape[1] = inputshape[1] * 2

#create model
model = Sequential()

#add model layers
model.add(Conv2D(32, kernel_size=kernelsize, padding = "same", activation='relu', input_shape=inputshape))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='same'))
model.add(Conv2D(32, kernel_size=kernelsize, padding = "same", activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(class_nbr, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

test = CSV_Data_Loader(train_file, valid_file, video_folder, inputshape, class_nbr, deriv, point)

X_train, y_train = test.trainreader()
X_test, y_test = test.validreader()

X_train = test.csvtonumpy(X_train)
X_test = test.csvtonumpy(X_test)

history = model.fit(X_train, y_train, validation_data=(X_test, y_test), batch_size = batch_size, epochs=epoch)

Register(history, name)
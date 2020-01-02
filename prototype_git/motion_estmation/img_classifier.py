import os
import urllib.request
import argparse
import cv2
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import keras
from keras import optimizers
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import Conv2D, MaxPooling2D, Embedding, Activation
from keras.layers import LSTM, Bidirectional
from keras.layers import concatenate
from keras import Model, Sequential, layers
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import StratifiedKFold
from keras.callbacks import EarlyStopping

import pandas as pd
import numpy as np
from pandas import DataFrame as df

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import seaborn as sns
from IPython.display import SVG, display
from keras.utils.vis_utils import model_to_dot


file_path = "./data/outputs_11-26/"
COUNT_MAX = 80
EMBEDDING_DIM = (360, 240)

image_data = []
label_data = []

for i in range(1, COUNT_MAX):
    true_input_file = file_path + "True" + str(i) + ".png"
    false_input_file = file_path + "False" + str(i) + ".png"

    true_image = cv2.imread(true_input_file, cv2.IMREAD_GRAYSCALE)
    false_image = cv2.imread(false_input_file, cv2.IMREAD_GRAYSCALE)

    image_data.append(true_image); label_data.append(1)
    image_data.append(false_image); label_data.append(0)   

# split data train : test (8:2)
train_X, test_X, train_Y, test_Y = train_test_split(X_data, Y_data, test_size = 0.2, random_state = 5159)
train_X = train_X.reshape(train_X.shape[0], 360, 240, 1).astype('float32') / 255
train_Y = np_utils.to_categorical(train_Y, 2)

print(train_X.shape, train_Y.shape)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), input_shape=(360, 240, 1), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy',optimizer='adam', metrics=['accuracy'])

batch_size = 32
num_epochs = 25

history = model.fit(train_X, train_Y,
                    epochs = num_epochs,
                    #callbacks = callbacks_list,
                    validation_split = 0.25,
                    shuffle = True,
                    batch_size = batch_size,
                    verbose=1
                   )
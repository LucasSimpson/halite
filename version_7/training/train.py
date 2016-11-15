from keras.models import Sequential
from keras.layers import Dense, Activation

import numpy as np

# input shape

# Tile: Vector[owner, strength, production]
# Input: 7x7 grid centered around tile in question
# input size = 7*7*3 = 147

# output: OneHotVector[NORTH, EAST, SOUTH, WEST, STILL]


# create model
model = Sequential([
    Dense(32, batch_input_shape=(None, 147)),
    Activation('relu'),
    Dense(5),
    Activation('softmax'),
])

# compile model
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# dummy data
from keras.utils.np_utils import to_categorical

input_data = np.random.randint(255, size=(1000, 147))
labels = np.random.randint(5, size=(1000, 1))
labels = to_categorical(labels, 5)

print(labels)


# fit data
model.fit(input_data, labels, nb_epoch=10, batch_size=32, validation_split=0.1)
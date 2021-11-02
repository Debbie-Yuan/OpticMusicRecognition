from tensorflow.keras.layers import Dense, MaxPooling2D, Flatten, Convolution2D, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Sequential
from tensorflow.python.keras.layers import BatchNormalization


def SVML(num_class, weights_path=None, has_fc=True):
    model = Sequential()
    model.add(Convolution2D(64, (3, 3), activation='relu', padding='same', input_shape=(224, 224, 3)))
    model.add(Convolution2D(64, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Convolution2D(128, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(128, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Convolution2D(256, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(256, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(256, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Convolution2D(512, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(512, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(512, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    model.add(Convolution2D(512, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(512, (3, 3), activation='relu', padding='same'))
    model.add(Convolution2D(512, (3, 3), activation='relu', padding='same'))
    model.add(MaxPooling2D((2, 2), strides=(2, 2)))

    if weights_path:
        model.load_weights(weights_path)
    if has_fc:
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(num_class, activation='sigmoid'))
    else:
        model.add(GlobalAveragePooling2D())
        model.add(Dense(num_class, activation='sigmoid'))
    # model.summary()
    return model

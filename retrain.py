import numpy as np
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
from keras.layers import Dropout, Flatten, Dense
from keras import applications

# dimensions of our images.
img_width, img_height = 299, 299

top_model_weights_path = 'model_files/bottleneck_fc_model.h5'
train_data_dir = 'dataset/train'
validation_data_dir = 'dataset/test'
nb_train_samples = 400
nb_validation_samples = 200
epochs = 50
batch_size = 20


def save_bottlebeck_features():
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the Inception network
    model = applications.InceptionResNetV2(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)
    np.save(open('model_files/bottleneck_features_train.npy', 'w'),
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    np.save(open('model_files/bottleneck_features_validation.npy', 'w'),
            bottleneck_features_validation)


def train_top_model():
    train_data = np.load(open('model_files/bottleneck_features_train.npy'))
    datagen = ImageDataGenerator(rescale=1. / 255)
    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    train_labels = np.array([int(id.split('/')[0]) for id in generator.filenames])

    validation_data = np.load(open('model_files/bottleneck_features_validation.npy'))

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    validation_labels = np.array([int(id.split('/')[0]) for id in generator.filenames])

    print np.shape(validation_data), np.shape(validation_labels)

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)
    model.save('model_files/model.h5')


# in progress
def predict(imgpaths):
    model = load_model('model_files/model.h5')

    imgs_data = np.empty(np.array((1,299,299,3)))

    for imgpath in imgpaths:

        img = load_img(imgpath, target_size=(299, 299))
        img_data = img_to_array(img)
        img_data = img_data.reshape(-1,299,299,3)
        print '*'*80
        append_data = np.array(img_data)
        print np.shape(append_data), np.shape(imgs_data)
        imgs_data = np.append(imgs_data, append_data, axis=0)

    print np.shape(imgs_data)
    features_test = applications.InceptionResNetV2(include_top=False, weights='imagenet').predict(imgs_data)
    print "-"*100
    print (model.predict(features_test), model.predict_classes(features_test))


save_bottlebeck_features()
train_top_model()

import time
import os

list = []
for fname in os.listdir('dataset_bk'):
    if fname.endswith('.jpg') and 'back' not in fname:
        list.append(os.path.join('dataset_bk', fname))

predict(list)

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
    train_labels = np.array(
        [0] * (nb_train_samples / 2) + [1] * (nb_train_samples / 2))

    validation_data = np.load(open('model_files/bottleneck_features_validation.npy'))
    validation_labels = np.array(
        [0] * (nb_validation_samples / 2) + [1] * (nb_validation_samples / 2))

    print np.shape(validation_data), np.shape(validation_labels)

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam',
                  loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)
    model.save('model_files/model.h5')


# in progress
def predict(imgpath):
    model = load_model('model_files/model.h5')
    img = load_img(imgpath, target_size=(299, 299))
    img_data = img_to_array(img)
    img_data = img_data.reshape(-1,299,299,3)
    print model.predict(img_data)


save_bottlebeck_features()
train_top_model()
# predict('dataset/test/1/001_front_ear.jpg')

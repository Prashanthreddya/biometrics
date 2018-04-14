from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array
from keras import activations
import numpy as np
from time import time
import os

def predict_inceptionv4(img_path):
    start = time()

    image = load_img(img_path, target_size=(299, 299))
    image = preprocess_input(img_to_array(image))
    image = image.reshape(-1,299,299,3)
    y = model.predict(image)

    end = time()

    print img_path + " processed, time = %d seconds" % int(end - start)

    return [int(os.path.basename(img_path).split('_')[0]), y]

if __name__ == "__main__":
    img_dir = 'dataset/'

    y_train = []
    y_test = []
    X_train = []
    X_test = []

    results = []

    train_count = {}

    total_start_time = time()
    print "Creating model..."
    model = InceptionResNetV2()
    print "Model created."

    print "Testing in progress..."
    for filename in sorted(os.listdir(img_dir)):
        if filename.endswith('.jpg') and 'back' not in filename:
            id = int(filename.split('_')[0])
            filepath = os.path.join(img_dir, filename)
            results.append(predict_inceptionv4(filepath))

    #Organise results into two np arrays
    features = []
    for result in results:
        if train_count.get(result[0],0) < 2:
            if result[0] in train_count:
                train_count[result[0]] += 1
            else:
                train_count[result[0]] = 1
            y_train.append(result[0])
            X_train.append(result[1])
        else:
            y_test.append(result[0])
            X_test.append(result[1])

    total_end_time = time()

    X_train = np.squeeze(np.array(X_train))
    y_train = np.array(y_train)
    X_test = np.squeeze(np.array(X_test))
    y_test = np.array(y_test)

    print '-'*80
    print "X_train: " + str(np.shape(X_train))
    print "y_train: " + str(np.shape(y_train))
    print "\nX_test: " + str(np.shape(X_test))
    print "y_test: " + str(np.shape(y_test))
    np.savez('model_files/inceptionv4_results.npz', X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
    print "Results saved in model_files/inceptionv4_results.npz"
    print "Total processing time: " + str((total_end_time - total_start_time)) + " seconds"

from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input, decode_predictions
from keras.preprocessing.image import load_img, img_to_array
from keras.models import Model
from keras import activations
import numpy as np
from time import time
import os

from tqdm import tqdm

def predict_inceptionv4(img_path, layer_name):
    start = time()

    image = load_img(img_path, target_size=(299, 299))
    image = preprocess_input(img_to_array(image))
    image = image.reshape(-1,299,299,3)
    # y = model.predict(image)

    intermediate_layer_model = Model(inputs=model.input,
                                     outputs=model.get_layer(layer_name).output)
    y1 = intermediate_layer_model.predict(image)

    end = time()

    id = int(os.path.basename(img_path).split('_')[0])
    return [id, y1]

if __name__ == "__main__":
    img_dir = 'dataset_bk/'

    layers = ['avg_pool']
    total_start_time = time()
    print "Creating model..."
    model = InceptionResNetV2()
    print "Model created."

    filepaths = []
    for filename in sorted(os.listdir(img_dir)):
        if filename.endswith('.jpg') and 'back' not in filename:
            id = int(filename.split('_')[0])
            filepaths.append(os.path.join(img_dir, filename))

    for layer_name in layers:
        y_train = []
        y_test = []
        X_train = []
        X_test = []

        results = []

        train_count = {}
        print "Testing in progress for layer " + layer_name + "..."
        for filepath in tqdm(filepaths):
            results.append(predict_inceptionv4(filepath, layer_name))

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

        fname = 'model_files/inceptionv4_results_'+layer_name+'.npz'
        np.savez(fname, X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test)
        print "Results saved in %s" % fname
        print "Total processing time: " + str((total_end_time - total_start_time)) + " seconds"

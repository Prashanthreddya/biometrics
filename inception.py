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
    features = np.empty((1,1000))
    classes = []
    class_count = {}
    temp = 0
    results = []
    filepaths = []
    total_start_time = time()
    i=0
    print "Getting results..."
    model = InceptionResNetV2()
    for filename in sorted(os.listdir(img_dir)):
        if filename.endswith('.jpg') and 'back' not in filename:
            id = int(filename.split('_')[0])

            # Get paths of 3 images per ear ID
            if id in class_count and class_count[id] < 3 or id not in class_count:
                filepath = os.path.join(img_dir, filename)
                if id not in class_count:
                    class_count[id] = 1
                else:
                    class_count[id] += 1
                results.append(predict_inceptionv4(filepath))

        # Get total of 75 images from the set
        if np.sum(np.array(class_count.values())) == 75:
            break


    if len(set(class_count.values())) != 1:
        print "This logic doesn't quite work"
        exit()


    #Organise results into two np arrays
    for result in results:
        classes.append(result[0])
        np.append(features, result[1])

    total_end_time = time()

    classes = np.array(classes)
    print '-'*80
    print "Classes: " + str(np.shape(classes))
    print "Features: " + str(np.shape(features))
    np.savez('inceptionv4_results.npz', classes=classes, features=features)
    print "Results saved in inceptionv4_results.npz"
    print "Total processing time: " + str((total_end_time - total_start_time)) + " seconds"

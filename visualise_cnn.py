from keras.applications.inception_resnet_v2 import InceptionResNetV2, preprocess_input, decode_predictions
from vis.utils import utils
from keras import activations
from matplotlib import pyplot as plt
from vis.visualization import visualize_saliency, overlay
from vis.visualization import visualize_cam

import numpy as np
import matplotlib.cm as cm
from time import time

times = [
    ["creating model",0],
    ['getting predictions layer index',0],
    ['swap softmax predictions with linear', 0],
    ['load images', 0],
    ['preprocess images', 0],
    ['visualize gradients', 0],
    ['visualise heatmap', 0]
]

# Build the VGG16 network with ImageNet weights
print times[0][0]
start = time()
model = InceptionResNetV2(input_shape=(299,299,3), include_top=False)
end = time()
times[0][1] = end-start

# Utility to search for layer index by name.
# Alternatively we can specify this as -1 since it corresponds to the last layer.
print times[1][0]
start = time()
layer_idx = utils.find_layer_idx(model, 'conv_7b')
end = time()
times[1][1] = end-start
print str(times[1][1]) + " seconds"

# Swap softmax with linear
# print times[2][0]
# start = time()
# model.layers[layer_idx].activation = activations.linear
# model = utils.apply_modifications(model)
# end = time()
# times[2][1] = end-start
# print str(times[2][1]) + " seconds"


plt.rcParams['figure.figsize'] = (18, 6)

print times[3][0]
start = time()
img1 = utils.load_img('dataset/019_right_ear.jpg', target_size=(299, 299))
img2 = utils.load_img('dataset/001_left_ear.jpg', target_size=(299, 299))
end = time()
times[3][1] = end-start
print str(times[3][1]) + " seconds"


# print times[4][0]
# start = time()
# img1 = preprocess_input(img1)
# img2 = preprocess_input(img2)
# end = time()
# times[4][1] = end-start

print times[5][0]
start = time()
modifier = 'guided'
plt.figure()
f, ax = plt.subplots(1, 2)
plt.suptitle(modifier)
for i, img in enumerate([img1, img2]):
    grads = visualize_saliency(model, layer_idx, filter_indices=None,
                               seed_input=img, backprop_modifier=modifier)
    # Lets overlay the heatmap onto original image.
    ax[i].imshow(grads, cmap='jet')
end = time()
times[5][1] = end-start
print str(times[5][1]) + " seconds"


print times[6][0]
start = time()
plt.figure()
f, ax = plt.subplots(1, 2)
plt.suptitle(modifier)
for i, img in enumerate([img1, img2]):
    grads = visualize_cam(model, layer_idx, filter_indices=None,
                          seed_input=img, backprop_modifier=modifier)
    # Lets overlay the heatmap onto original image.
    ax[i].imshow(overlay(grads, img))
end = time()
times[6][1] = end-start
print str(times[6][1]) + " seconds"

print

plt.show()

print "\nTimes:"
import pprint
pprint.pprint(times)

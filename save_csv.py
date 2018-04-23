import numpy as np

data = np.load('model_files/inceptionv4_results.npz')

test_data = np.empty(np.array((1,1001)))
train_data = np.empty(np.array((1,1001)))

for idx, val in enumerate(data['X_train']):
    val = np.array(np.append(val,data['y_train'][idx]))
    val = val.reshape(1,1001)
    test_data = np.append(test_data, val, axis=0)

for idx, val in enumerate(data['X_test']):
    val = np.array(np.append(val,data['y_test'][idx]))
    val = val.reshape(1,1001)
    train_data = np.append(train_data, val, axis=0)

np.savetxt("model_files/test.csv", test_data, delimiter=",")
np.savetxt("model_files/train.csv", train_data, delimiter=',')

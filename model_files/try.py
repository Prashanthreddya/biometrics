import numpy as np
data=np.load('inceptionv4_results_avg_pool.npz')
#['X_test', 'X_train', 'y_train', 'y_test']

train_x=data['X_train'] 
test_x=data['X_test']
train_y=data['y_train']
test_y=data['y_test']

print len(train_x)



print random_names
#!/usr/bin/env python
# multinomial_logistic_regression.py
# Author : Saimadhu Polamuri
# Date: 05-May-2017
# About: Multinomial logistic regression model implementation
 
import numpy as np
from sklearn import linear_model
from sklearn import metrics

def main():
    data=np.load('model_files/inceptionv4_results_avg_pool.npz')
    #['X_test', 'X_train', 'y_train', 'y_test']

    train_x=data['X_train'] 
    test_x=data['X_test']
    train_y=data['y_train']
    test_y=data['y_test']

    # Train multinomial logistic regression model
    mul_lr = linear_model.LogisticRegression(multi_class='ovr', solver='liblinear').fit(train_x, train_y)
 
    #print "Multinomial Logistic regression Train Accuracy :: ", metrics.accuracy_score(train_y, mul_lr.predict(train_x))
    
    predicted_class=mul_lr.predict(test_x)
    actual_class=test_y

    for i in range(len(predicted_class)):
        print "Predicted Class - ", predicted_class[i], "; Actual Class - ", actual_class[i]
    print "Multinomial Logistic regression Test Accuracy :: ", metrics.accuracy_score(test_y, mul_lr.predict(test_x))
 
 
if __name__ == "__main__":
    main()
#!/usr/bin/env python
# multinomial_logistic_regression.py
# About: Multinomial logistic regression model implementation

import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.externals import joblib

import time
import os

model_dir = os.path.abspath('../trained_models')
model_name = 'model_%d.pkl'

def get_latest_model():
    latest = 0
    for fname in os.listdir(model_dir):
        timestamp = int(fname.split('.')[0].split('_')[-1])
        if timestamp > latest:
            latest = timestamp

    if latest == 0:
        return None
    else:
        model_path = os.path.abspath(os.path.join(model_dir, model_name%latest))
        model = joblib.load(model_path)
        return model


def predict(x_test):
    model = get_latest_model()

    if model == None:
        model = train_new_model()

    predicted_class = model.predict(x_test)
    score = model.decision_function(x_test)
    return (predicted_class[0], score[0])


def train(x_train, y_train):
    y_train = [y_train]*len(x_train)
    model = get_latest_model()
    model = model.partial_fit(x_train, y_train)
    save_model(model)

def save_model(model):
    timestamp = int(time.time())
    joblib.dump(model, os.path.join(model_dir, model_name%timestamp))

def train_new_model():
    data=np.load('../model_files/inceptionv4_results_avg_pool.npz')

    train_x=data['X_train']
    train_y=data['y_train']

    # Train multinomial logistic regression model
    mul_lr = linear_model.LogisticRegression(multi_class='ovr', solver='liblinear').fit(train_x, train_y)
    save_model(mul_lr)
    return mul_lr

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# multinomial_logistic_regression.py
# About: Multinomial logistic regression model implementation

import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.externals import joblib

import ML_from_DB as mongo

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

    score = model.predict_proba(x_test)
    return (model.classes_, score[0])


def validate():

    x_test, y_test = mongo.get_lists('test')

    model = get_latest_model()

    if model == None:
        model = train_new_model()

    preds = model.predict(x_test)

    progress = []
    for i in range(len(preds)):
        message = "Predicted Class - %d; Actual Class - %d" % (preds[i], y_test[i])
        print message
        progress.append(message)

    score = metrics.accuracy_score(y_test, model.predict(x_test))
    message = "Multinomial Logistic regression Test Accuracy :: %f" % score
    print message
    progress.append(message)

    return score, progress


def save_model(model):
    timestamp = int(time.time())
    joblib.dump(model, os.path.join(model_dir, model_name%timestamp))

def retrain_model(x_train, y_train):
    y_train = [y_train]*len(x_train)
    model = get_latest_model()
    return create_model(x_train, y_train)


def train_new_model():
    train_x, train_y = mongo.get_lists('train')

    # Train multinomial logistic regression model
    return create_model(train_x, train_y)

def create_model(train_x, train_y):
    mul_lr = linear_model.LogisticRegression(multi_class='ovr', solver='liblinear').fit(train_x, train_y)
    score = metrics.accuracy_score(train_y, mul_lr.predict(train_x))
    save_model(mul_lr)
    return score

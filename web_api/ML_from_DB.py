import numpy as np
from sklearn import linear_model
from sklearn import metrics
import pymongo
from pymongo import MongoClient
from config import *

client = MongoClient(host=CONNECTION_STRING)

def get_lists(s):
    if s=="train":
        train=list(client.biometric.train_set.find())
        x_train=[]
        y_train=[]
        for sample in train:
            x_train.append(sample['sample_feature'])
            y_train.append(sample['sample_class'])
        return x_train,y_train
    if s=="test":
        test=list(client.biometric.test_set.find())
        x_test=[]
        y_test=[]
        for sample in test:
            x_test.append(sample['sample_feature'])
            y_test.append(sample['sample_class'])
        return x_test, y_test


def get_name_from_id(id):
    return client.biometric.train_set.find_one({'sample_class': id})["sample_name"]

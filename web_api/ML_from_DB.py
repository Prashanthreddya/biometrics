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

def mongo_add(dataset, s_class, features=None, name=None):
    if dataset=='train':
        collection = client.biometric.train_set
    else:
        collection = client.biometric.test_set

    if features is not None:
        for feature_array in features:
            d={}
            d['sample_class']=s_class
            d['sample_feature']=feature_array
            d['sample_name']='unknown'
            collection.insertOne(d)
            pass

    if name is not None:
        collection.update({sample_class:s_class},{sample_name:name},{multi: True})
        pass


def get_next_class():
    collection=client.biometric.train_set
    next_class=collection.find_one(sort=[("sample_class",pymongo.DESCENDING)])["sample_class"]+1
    return next_class
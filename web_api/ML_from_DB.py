
# coding: utf-8

# In[21]:


import numpy as np
from sklearn import linear_model
from sklearn import metrics
import pymongo
from pymongo import MongoClient


# In[85]:


client = MongoClient(host='mongodb://prashanth:biometric@ds157089.mlab.com:57089/biometric')


# In[86]:


train=list(client.biometric.train_set.find())
test=list(client.biometric.test_set.find())


# In[87]:


def get_lists(s):
    if s=="train":
        x_train=[]
        y_train=[]
        for sample in train:
            x_train.append(sample['sample_feature'])
            y_train.append(sample['sample_class'])
        return x_train,y_train
    if s=="test": 
        x_test=[]
        y_test=[]
        for sample in test:
            x_test.append(sample['sample_feature'])
            y_test.append(sample['sample_class'])
        return x_test, y_test


# In[88]:


x_train,y_train=get_lists("train")
x_test,y_test=get_lists("test")


# In[89]:


mul_lr = linear_model.LogisticRegression(multi_class='ovr', solver='liblinear').fit(x_train, y_train)
print "LR Test Accuracy :: ", metrics.accuracy_score(y_test, mul_lr.predict(x_test))


"""
Given directory of images, create mongodb collection of ear features and person_id
"""

import cv2
import numpy as np
import os
from pymongo import MongoClient

IMG_DIR = '~/biometrics/dataset/subset/'

client = MongoClient()
db = client.biometry
collection = db.ear_data_09_01_18

for f in os.listdir(IMG_DIR):
    if f.endswith('.jpg'):
        data = cv2.imread(IMG_DIR+f,cv2.IMREAD_GRAYSCALE)
        label = int(f[:3]) #ID of person in img, obtained from filename

        #TODO: detect_features

        #TODO: Insert detected features into img_data instead of flattened image
        result = collection.insert_one({"img_data":data.flatten().tolist()},{"person_id":label})

        print f + " inserted"

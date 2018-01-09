import cv2
import numpy as np
import os
from pymongo import MongoClient

IMG_DIR = '/Users/krupahebbar/Downloads/dataset/ear/raw/'

client = MongoClient()
db = client.biometry
collection = db.ear_data_19_12_17

#TODO: fix syntax
for f in os.listdir(IMG_DIR):
    if f.endswith('.bmp'):
        data = cv2.imread(IMG_DIR+f,cv2.IMREAD_GRAYSCALE)
        label = int(f[:3]) #ID of person in img, obtained from filename

        result = collection.insert_one({"img_data":data.flatten().tolist()},{"person_id":label})

        print f + " inserted"

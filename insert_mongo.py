"""
Given directory of images, create mongodb collection of ear features and person_id
"""

import numpy as np
import os
from pymongo import MongoClient
import argparse
from config import connection_string, ami_img_dir
from tqdm import tqdm

def store_data(IMG_DIR=ami_img_dir):
    client = MongoClient(host=connection_string)
    db = client.biometrics
    collection = db.ear_data_ami

    for f in tqdm(os.listdir(os.path.abspath(IMG_DIR))):
        if f.endswith('.jpg'):
            fname = os.path.basename(f).split('.')[0]
            id, orientation, _ = fname.split('_')
            id = int(id)

            result = collection.insert_one({"img_local_path":os.path.join(IMG_DIR,fname),"id":id, "orientation": orientation})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--imgdir", help="Directory of source images")
    args = parser.parse_args()

    IMG_DIR = args.imgdir
    if IMG_DIR is not None and os.path.exists(IMG_DIR):
        store_data(IMG_DIR)
    else:
        store_data()

from logi import *
from extract_features import *

path = '/Users/krupahebbar/biometrics/dataset/test/13/013_zoom_ear.jpg'

id, features = extract_features(path)
pred, score = predict(features)

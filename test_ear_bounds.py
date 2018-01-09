import numpy as np
import cv2
import argparse
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("img", help="detect corners in img")
img = parser.parse_args().img

IMG_DIR = '/Users/krupahebbar/Downloads/dataset/ear/raw/'

img = cv2.imread(IMG_DIR+img+'.bmp')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)

plt.imshow(img),plt.show()

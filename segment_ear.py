import cv2
import numpy as np

right_ear_cascade = cv2.CascadeClassifier('./cascade-files/haarcascade_mcs_leftear.xml')
left_ear_cascade = cv2.CascadeClassifier('./cascade-files/haarcascade_mcs_rightear.xml')

if left_ear_cascade.empty():
  raise IOError('Unable to load the left ear cascade classifier xml file')

if right_ear_cascade.empty():
  raise IOError('Unable to load the right ear cascade classifier xml file')

img = cv2.imread('dataset_bk/999_front_ear.jpg')  #dormer, down, front, left, right, up

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

left_ear = left_ear_cascade.detectMultiScale(gray, 1.3, 5)
right_ear = right_ear_cascade.detectMultiScale(gray, 1.3, 5)

print left_ear
print right_ear

for (x,y,w,h) in left_ear:
    cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 10)

for (x,y,w,h) in right_ear:
    cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 10)

cv2.imshow('Ear Detector', img)
cv2.waitKey()
cv2.destroyAllWindows()

import cv2
import numpy as np
import os
import json

def find_all(photo_name, folderName, path_):
    # print('inside find_all')

    # print('photo_name: ', photo_name)
    # print('folderName: ', folderName)
    # print('path_: ', path_)
    # print(folderName + photo_name + '.png')
    
    img = cv2.imread(folderName + photo_name + '.png')
    (h, w) = img.shape[:2]
    image_size = h*w
    mser = cv2.MSER_create()
    mser.setMaxArea(int(image_size/2))
    mser.setMinArea(10)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converting to GrayScale
    _, bw = cv2.threshold(gray, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    regions, rects = mser.detectRegions(bw)

    # ordinare sulle y e poi sulle x le rects
    rects = sorted(rects, key=lambda x: (x[1], x[0]))

    # print(rects)

    with open(path_  + photo_name.split('.')[0] + '\\rects.txt', 'w+') as file_:
        # file_.write(str([rec.tolist() for rec in rects]))
        # print([(rec[2] ,rec[3])  for rec in rects])
        # [rec.tolist() for rec in rects if (rec[2] > 10 and rec[3] > 10)]
        json.dump([rec.tolist() for rec in rects], file_) 

    for (x, y, w, h) in rects:
        cv2.rectangle(img, (x, y), (x+w, y+h), color=(255, 0, 255), thickness=1)

    cv2.imwrite( path_ + '\\' + photo_name.split('.')[0] + '\\' +  photo_name.split('.')[0]  + '_Comp.png', img)
# -*- coding: utf-8 -*-
"""cap_seated_new_md.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ErBcjkdwCBwxjlz0f4vOlC-mt7ayrffv
"""

import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate

import PIL
from PIL import ImageEnhance
from PIL import Image

import cv2
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from skimage.draw import ellipse
from skimage.measure import label, regionprops, regionprops_table
from skimage.transform import rotate

import PIL
from PIL import ImageEnhance
from PIL import Image

def cap_seated_md(img_name):

    size = "md"
    path = img_name

    image_c = cv2.imread(path)
    print(image_c)
    image_c = np.rot90(np.rot90(image_c))

    image = cv2.imread(path,0)
    image = np.rot90(np.rot90(image))

    # print(type(image))
    # print(image.shape)

    # plt.figure(figsize=(10,10))
    # plt.imshow(cv2.cvtColor(image_c,cv2.COLOR_BGR2RGB))

    # crop image
    # crop image

    if size == "lg":
        image_c = image_c[1000:,800:2500]
        image = image[1000:,800:2500]
    elif  size == "md":
        image_c = image_c[1000:,800:2500]
        image= image[1000:,800:2500]
    elif  size == "sm":
        image_c = image_c[500:,800:2500]
        image = image[500:,800:2500]
        
    # plt.imshow(cv2.cvtColor(image_c,cv2.COLOR_BGR2RGB))

    img = image
    img = cv2.medianBlur(img,5)

    ret,th1 = cv2.threshold(img,80,255,cv2.THRESH_BINARY)

    titles = ['org','Global Thresholding (v = 127)'
                ]
    images = [img, th1]
    # assert len(titles)==len(images)
    # for i in range(len(titles)):
    #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])
    # plt.show()

    bbox = cv2.boundingRect(th1)
    x, y, w, h = bbox

    if size == "lg":
        cropped = cv2.cvtColor(image_c[y-30:y+h+30, x:x+w], cv2.COLOR_BGR2RGB)

    if size == "md":
        cropped = cv2.cvtColor(image_c[y-160:y+h+30, x:x+w], cv2.COLOR_BGR2RGB)

    if size == "sm":
        cropped = cv2.cvtColor(image_c[y-160:y+h+30, x:x+w], cv2.COLOR_BGR2RGB)

    # cropped = cv2.cvtColor(image_c[y:y+h, x:x+w], cv2.COLOR_BGR2RGB)
        
    # plt.figure(figsize=(10,10))
    # plt.imshow(cropped,'gray',vmin=0,vmax=255)
    # plt.show()

    h,w, _ = cropped.shape
    md_crop_ratio =  0.65
    sm_crop_ratio = 0.8
    lg_crop_ratio = 0.5

    # h1 = int(h * 0.24)
    if size == "lg":
        h1 = int(h * lg_crop_ratio)
    elif  size == "md":
        h1 = int(h * md_crop_ratio)
    elif  size == "sm":
        h1 = int(h * sm_crop_ratio)
    # h1 = int(h * 0.55)
    cap_only = cropped[0:h1,:]
    # plt.imshow(cap_only)

    blurred = cv2.medianBlur(cap_only,7) # increase kernel size to remove white edges
    cap_left = blurred[600:750,100:400]
    cap_right = blurred[400:600,400:800]
    # plt.subplot(1,2,1)
    # plt.imshow(cap_left)
    # plt.subplot(1,2,2)
    # plt.imshow(cap_right)

    grayl = cv2.cvtColor(cap_left, cv2.COLOR_RGB2GRAY)
    grayr = cv2.cvtColor(cap_right, cv2.COLOR_RGB2GRAY)
    # plt.subplot(1,2,1)
    # plt.imshow(grayl,"gray")
    # plt.subplot(1,2,2)
    # plt.imshow(grayr,"gray")

    lc = grayl>240
    lc = sum(sum(lc))
    print("lc ----------------------"+str(lc))

    # not seated = 7070,7620,7162
    #threshold = 4000
    #seated = 3915,2023,958,2626,5152,647,945,79,777

    result_status = ""
    if lc >=4000:
        result_status = "Unacceptable"
    else:
        result_status = "Acceptable"


    return result_status






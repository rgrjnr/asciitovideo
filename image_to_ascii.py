# Python code to convert an image to ASCII image.
import sys
import random
import argparse
import numpy as np
import math
import os
import os.path
import json

from PIL import Image

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray

# 10 levels of gray
gscale2 = '@%#*+=-:. '


def getAverageL(image):
    """ 
    Given PIL Image, return average value of grayscale value 
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w*h))


def convertImageToAscii(fileName, cols, scale, level):
    """ 
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]
    #print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W/cols

    # compute tile height based on aspect ratio and scale
    h = w/scale

    # compute number of rows
    rows = int(H/h)

    #print("cols: %d, rows: %d" % (cols, rows))
    #print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # correct last tile
        if j == rows-1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # correct last tile
            if i == cols-1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # configuração da escala de cinza
            gsval = level[int((avg*(len(level)-1))/255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg


def convert_video(video_name, scale=0.43, cols=80, level=' .:-=+*#%@'):

    video = []

    # List all files in a directory using scandir()
    basepath = f'frames/{video_name}'
    with os.scandir(basepath) as entries:

        DIR = basepath
        length = len([name for name in os.listdir(
            DIR) if os.path.isfile(os.path.join(DIR, name))])
        count = 1
        for entry in entries:
            if entry.is_file():
                # Cada frame
                imgFile = f"{basepath}/{entry.name}"
                aimg = convertImageToAscii(imgFile, cols, scale, level)

                image_string = ""
                for row in aimg:
                    image_string += row + '\n'

                print('{0:.2f}'.format(count/length))
                count += 1

                video.append(image_string)

    with open(f'converted/{video_name}.json', 'w') as outfile:
        json.dump(video, outfile)

    os.remove(f'videos/{video_name}.mp4')

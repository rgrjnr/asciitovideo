import cv2
import os
import Dither
import numpy as np


def minmax(v):
    if v > 255:
        v = 255
    if v < 0:
        v = 0
    return v


def dithering_gray(inMat, samplingF):
    # https://en.wikipedia.org/wiki/Floyd–Steinberg_dithering
    # https://www.youtube.com/watch?v=0L2n8Tg2FwI&t=0s&list=WL&index=151
    # input is supposed as color
    # grab the image dimensions
    h = inMat.shape[0]
    w = inMat.shape[1]

    # loop over the image
    for y in range(0, h-1):
        for x in range(1, w-1):
            # threshold the pixel
            old_p = inMat[y, x]
            new_p = np.round(samplingF * old_p/255.0) * (255/samplingF)
            inMat[y, x] = new_p

            quant_error_p = old_p - new_p

            inMat[y, x+1] = minmax(inMat[y, x+1] + quant_error_p * 7 / 16.0)
            inMat[y+1, x-1] = minmax(inMat[y+1, x-1] +
                                     quant_error_p * 3 / 16.0)
            inMat[y+1, x] = minmax(inMat[y+1, x] + quant_error_p * 5 / 16.0)
            inMat[y+1, x+1] = minmax(inMat[y+1, x+1] +
                                     quant_error_p * 1 / 16.0)
    return inMat


def video_to_frames(video_name):
    vidcap = cv2.VideoCapture(f'videos/{video_name}.mp4')
    count = 0
    success = True
    fps = int(vidcap.get(cv2.CAP_PROP_FPS))

    if os.path.exists(f'frames/{video_name}') == False:
        os.mkdir(f'frames/{video_name}')

    while success:
        success, image = vidcap.read()
        if count % 1 == 0:
            print(count)
            try:
                count += 1
                grayMat = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                outMat_gray = dithering_gray(grayMat.copy(), 1)
                cv2.imwrite(f'frames/{video_name}/%09d.jpg' %
                            count, outMat_gray)

            except Exception:
                pass

    return True

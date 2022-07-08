import os
import numpy as np
import cv2 as cv


def get_filename(img_path, is_png=True):
    pure_img_name = os.path.basename(img_path)
    if is_png:
        pure_img_name = pure_img_name.split('.')[-2] + ".png"
    else:
        pure_img_name = pure_img_name.split('.')[-2] + ".jpg"
    return pure_img_name


def get_sobel(gray_img):
    image_sobel_x = cv.Sobel(gray_img, cv.CV_64F, 1, 0, ksize=3)
    image_sobel_y = cv.Sobel(gray_img, cv.CV_64F, 0, 1, ksize=3)
    image_sobel_xy = np.abs(image_sobel_x) + np.abs(image_sobel_y)
    image_sobel_xy = cv.convertScaleAbs(image_sobel_xy)
    return image_sobel_xy

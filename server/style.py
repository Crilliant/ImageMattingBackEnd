import cv2 as cv
import numpy as np
from server.utils import *


# 水彩化
def watercolor(img_path, save_dir):
    pure_img_name = get_filename(img_path)
    print(pure_img_name)
    img = cv.imread(img_path)
    result = cv.stylization(img, sigma_s=200, sigma_r=0.6)
    print(save_dir)
    cv.imwrite(os.path.join(save_dir, pure_img_name), result)
    print(pure_img_name + " is finished.")


# 素描化
def sketch(img_path, save_dir):
    gray_img = cv.cvtColor(cv.imread(img_path), cv.COLOR_BGR2GRAY)
    filename = get_filename(img_path)
    gray_img = cv.GaussianBlur(gray_img, (5, 5), 0)
    image_sobel_x = cv.Sobel(gray_img, cv.CV_64F, 1, 0, ksize=3)
    image_sobel_y = cv.Sobel(gray_img, cv.CV_64F, 0, 1, ksize=3)
    image_sobel_xy = np.abs(image_sobel_x) + 1.5 * np.abs(image_sobel_y)
    image_sobel_xy = cv.convertScaleAbs(image_sobel_xy)
    cv.imwrite(os.path.join(save_dir, filename), np.abs(128 * np.ones(image_sobel_xy.shape) - image_sobel_xy))
    print(filename + 'is finished.')

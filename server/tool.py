# -*- coding: utf-8 -*-
# @Time : 2022/6/22 9:15
# @Author : Cao Yuxin
# @File : tool.py

import os
import numpy as np
from PIL import Image
import glob
import cv2 as cv
import server.u2net_test as u2net


def get_filename(img_path):
    pure_img_name = os.path.basename(img_path)
    pure_img_name = pure_img_name.split('.')[-2] + ".png"
    return pure_img_name


def get_img_and(img_path, mask_path):
    img = cv.imread(os.path.join(img_path))
    mask = cv.imread(mask_path)
    result = cv.bitwise_and(img, mask)  # 必须是相同通道数
    mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)  # 灰度图
    result = cv.cvtColor(result, cv.COLOR_BGR2BGRA)  # 4通道
    return result, mask


# 切割主要部分
def get_main_body(image, mask):
    th, mask = cv.threshold(mask, 100, 255, cv.THRESH_BINARY)
    (borders, features) = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    border = sorted(borders, key=cv.contourArea, reverse=True)[0]

    rect = cv.minAreaRect(border)
    box = np.int0(cv.boxPoints(rect))

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x_min = min(Xs)
    x_max = max(Xs)
    y_min = min(Ys)
    y_max = max(Ys)
    return image[y_min:y_max, x_min:x_max]


# 识别单张图片（路径imp_path）显著物体，并保存到meetter_dir
# mask_dir为黑白掩码保存的目录
def img_matting(img_path, mask_dir, matted_dir):
    u2net.inference_img(img_path, mask_dir)
    print("finish the inference")
    if not os.path.exists(matted_dir):
        os.makedirs(matted_dir)

    pure_img_name = get_filename(img_path)

    if not os.path.exists(os.path.join(mask_dir, pure_img_name)):
        print("no exist" + os.path.join(mask_dir, pure_img_name))

    print(pure_img_name + " is being met...")
    result, mask = get_img_and(img_path, os.path.join(mask_dir, pure_img_name))
    for i in range(0, result.shape[0]):  # 访问所有行
        for j in range(0, result.shape[1]):  # 访问所有列
            if mask[i][j] < 100:
                result[i, j, 3] = 0
    result = get_main_body(result, mask)
    cv.imwrite(os.path.join(matted_dir, pure_img_name), result)
    print(pure_img_name + " is finished.")


# 根据mask将背景色换为value值
def change_backcolor(image, mask, value):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if mask[i, j] < 100:
                image[i, j] = value
    return image


# 证件照功能
def get_identification_image(img_path, mask_dir, matted_dir):
    u2net.inference_img(img_path, mask_dir)
    pure_img_name = get_filename(img_path)
    result, mask = get_img_and(img_path, os.path.join(mask_dir, pure_img_name))

    result = change_backcolor(result, mask, value=[0, 0, 255, 255])
    cv.imwrite(os.path.join(matted_dir, pure_img_name), result)
    print(pure_img_name + "color changed.")


# met一个文件夹的图片
def img_matting_dir(img_dir, mask_dir, matted_dir):
    if not os.path.exists(matted_dir):
        os.makedirs(matted_dir)

    for file in os.listdir(img_dir):
        pure_img_name = file.split('.')[-2] + '.png'

        if not os.path.exists(os.path.join(mask_dir, pure_img_name)):
            print("no exist" + os.path.join(mask_dir, pure_img_name))
            continue
        print(pure_img_name + " is being met...")
        img = cv.imread(os.path.join(img_dir, file))
        mask = cv.imread(os.path.join(mask_dir, pure_img_name))

        result = cv.bitwise_and(img, mask)  # 必须是相同通道数
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)  # 灰度图
        result = cv.cvtColor(result, cv.COLOR_BGR2BGRA)  # 4通道

        for i in range(0, result.shape[0]):  # 访问所有行
            for j in range(0, result.shape[1]):  # 访问所有列
                if mask[i][j] < 100:
                    result[i, j, 3] = 0
        cv.imwrite(os.path.join(matted_dir, pure_img_name), result)
        print(file + " is finished.")


# 水彩
def watercolor(img_dir, mask_dir, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for file in os.listdir(img_dir):
        pure_img_name = file.split('.')[-2] + '.png'
        if not os.path.exists(os.path.join(mask_dir, pure_img_name)):
            print("no exist" + os.path.join(mask_dir, pure_img_name))
            continue
        img = cv.imread(os.path.join(img_dir, file))
        result = cv.stylization(img, sigma_s=60, sigma_r=0.6)
        mask = cv.imread(os.path.join(mask_dir, pure_img_name))
        result = cv.bitwise_and(result, mask)
        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)  # 灰度图
        result = cv.cvtColor(result, cv.COLOR_BGR2BGRA)  # 4通道

        for i in range(0, result.shape[0]):  # 访问所有行
            for j in range(0, result.shape[1]):  # 访问所有列
                if mask[i][j] < 100:
                    result[i, j, 3] = 1
        cv.imwrite(os.path.join(save_dir, pure_img_name), result)
        print(file + " is finished.")


# 油画，弃用
def oilpainting(img_dir, mask_dir, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for file in os.listdir(img_dir):
        pure_img_name = file.split('.')[-2] + '.png'
        if not os.path.exists(os.path.join(mask_dir, pure_img_name)):
            print("no exist" + os.path.join(mask_dir, pure_img_name))
            continue

        img = cv.imread(os.path.join(img_dir, file))
        result = cv.xphoto.oilPainting(img, 7, 1)
        mask = cv.imread(os.path.join(mask_dir, pure_img_name))
        result = cv.bitwise_and(result, mask)

        mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)  # 灰度图
        result = cv.cvtColor(result, cv.COLOR_BGR2BGRA)  # 4通道

        for i in range(0, result.shape[0]):  # 访问所有行
            for j in range(0, result.shape[1]):  # 访问所有列
                if mask[i][j] < 100:
                    result[i, j, 3] = 1
        cv.imwrite(os.path.join(save_dir, pure_img_name), result)
        print(file + " is finished.")


def overlap(top_path, btm_path, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    img_name = top_path.split('/')[-1]

    top = cv.imread(top_path, cv.IMREAD_UNCHANGED)  # 读取四通道
    btm = cv.imread(btm_path)

    btm = cv.resize(btm, (top.shape[1], top.shape[0]))
    print("top and btm shapes:")
    print(top.shape)
    print(btm.shape)
    for i in range(0, top.shape[0]):  # 访问所有行
        for j in range(0, top.shape[1]):  # 访问所有列
            if (top[i][j][3] == 0):
                top[i][j][:3] = btm[i][j][:3]
                top[i][j][3] = 255

    cv.imwrite(os.path.join(save_dir, img_name), top)


if __name__ == "__main__":
    filename_test = 'wallpaper.png'
    '/home/mloser/Program/Python/ImageMatting/back/static/'
    file_path = os.path.join('/home/mloser/Program/Python/ImageMatting/back/static/Upload', filename_test)
    mask_path = os.path.join('/home/mloser/Program/Python/ImageMatting/back/static/Mask')
    save_path = os.path.join('/home/mloser/Program/Python/ImageMatting/back/static/Download')
    # executor.submit(img_metting, file_path, mask_path, save_path)
    get_identification_image(file_path, mask_path, save_path)

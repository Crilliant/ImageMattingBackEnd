# -*- coding: utf-8 -*-
# @Time : 2022/7/1 15:08
# @Author : Cao Yuxin
# @File : test.py
import style
import os

def neno_dir(img_dir, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for file in os.listdir(img_dir):
        style.neno(os.path.join(img_dir, file), save_dir)


if __name__ == "__main__":
    img_dir = r"E:\Code\u2_net\U-2-Net\test_data\test_images"
    neno_dir(img_dir, r"E:\Code\u2_net\U-2-Net\test_data\mytest\neno/enlarge_difference")
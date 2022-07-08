# -*- coding: utf-8 -*-
# @Time : 2022/7/7 19:31
# @Author : Cao Yuxin
# @File : test.py
# 使用MAE(mean absolute erro)和miou 评估u-2-net模型准确率
import cv2 as cv
import numpy as np
import os
import time

# 计算一张的MAE(mean absolute erro)
def get_MAE(prediction, ground_truth):
    prediction = prediction/255
    ground_truth = ground_truth/255
    shape = prediction.shape

    mae = sum(sum(abs(prediction-ground_truth)))/(shape[0]*shape[1])
    return mae

# 计算miou
def get_miou(prediction, ground_truth):
    _, prediction = cv.threshold(prediction, 127, 255, cv.THRESH_BINARY)
    FP = sum(sum(ground_truth-prediction == -255))
    TP = sum(sum((ground_truth == prediction) & (ground_truth == 255)))
    FN = sum(sum(ground_truth-prediction == 255))
    return TP/(TP + FP + FN)

# 评估一个文件夹的mae, miou
def evaluate_dir(pre_dir, ground_truth_dir):
    mae = []
    miou = []
    for img_name in os.listdir(pre_dir):
        prediction = cv.imread(os.path.join(pre_dir, img_name), cv.IMREAD_GRAYSCALE)
        ground_truth = cv.imread(os.path.join(ground_truth_dir, img_name), cv.IMREAD_GRAYSCALE)
        img_mae = get_MAE(prediction, ground_truth)
        mae.append(img_mae)

        img_miou = get_miou(prediction, ground_truth)
        miou.append(img_miou)
        del prediction, ground_truth

        print(img_name + "'s mean absolute erro : " + str(img_mae))
        print("\tmiou : " + str(img_miou))

    print("total image number is : " + str(len(mae)))
    print("total mean absolution erro is : "+str(sum(mae)/len(mae)))
    print("total Mean Intersection over Union in is : " + str(sum(miou) / len(miou)))



def main():
    pre_dir = r'E:\Code\u2_net\U-2-Net\train_data\predict'
    gt_dir = r'E:\Code\u2_net\U-2-Net\train_data\mask'
    evaluate_dir(pre_dir, gt_dir)

if __name__ == "__main__":
    cpu_start = time.clock()
    main()
    cpu_end = time.clock()
    print('cpu:', cpu_end - cpu_start)

# -*- coding: utf-8 -*-
# @Time : 2022/6/22 9:15
# @Author : Cao Yuxin
# @File : tool.py

import server.u2net_test as u2net
from server.utils import *


# 切割主要部分
def get_main_body(image, mask):
    th, mask = cv.threshold(mask, 100, 255, cv.THRESH_BINARY)
    (borders, features) = cv.findContours(mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    border = sorted(borders, key=cv.contourArea, reverse=True)[0]

    rect = cv.minAreaRect(border)
    box = np.int0(cv.boxPoints(rect))

    # noinspection PyTypeChecker
    xs = [i[0] for i in box]
    # noinspection PyTypeChecker
    ys = [i[1] for i in box]
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)
    return image[y_min:y_max, x_min:x_max]


# 识别单张图片（路径imp_path）显著物体
# mask_dir为黑白掩码保存的目录
def img_matting(img_path, mask_dir, matted_dir):
    print('---------------------start----------------')
    try:
        img = cv.imread(img_path)
        mask = u2net.inference_img(img_path, mask_dir)
        print("finish the inference")

        pure_img_name = get_filename(img_path)

        print(pure_img_name + " is being met...")
        mask_1 = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)
        result = cv.bitwise_and(img, mask_1)  # 必须是相同通道数
        result = cv.cvtColor(result, cv.COLOR_BGR2BGRA)  # 4通道
        for i in range(0, result.shape[0]):  # 访问所有行
            for j in range(0, result.shape[1]):  # 访问所有列
                if mask[i][j] < 100:
                    result[i, j, 3] = 0
        # result = get_main_body(result, mask)
        cv.imwrite(os.path.join(matted_dir, pure_img_name), result)
        print(pure_img_name + " is finished.")
    except Exception as err:
        raise err

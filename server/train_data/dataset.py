# 用于将supervisely的json转换为png并保存
import numpy as np
import cv2 as cv
import os
import supervisely_lib as sly  # Supervisely Python SDK
import json                    # Add Python JSON module for pretty-printing.
import time

# supervisely工程路径
# project = sly.Project(r'E:\Code\u2_net\U-2-Net\datasets\Supervisely Person Dataset',
#                       sly.OpenMode.READ)


# 保存一张掩码图片
def save_mask(img_name, ann, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    path = os.path.join(save_dir, img_name)

    cv.imwrite(path+".png", ann)
    # print(img_name+" is finished.")

# 生成一张掩码
def draw_ann(ann_path):
    ann = sly.Annotation.load_json_file(ann_path, project.meta)
    ann_render = np.zeros(ann.img_size + (3,), dtype=np.uint8)  # 变成3通道
    ann.draw(ann_render)  # 画出mask
    return ann_render

# 处理working_dir文件夹的图片，并保存到save_dir
def json2png(working_dir, save_dir):
    for file in os.listdir(working_dir):
        img_name = file.split('.')[-3]
        ann = draw_ann(os.path.join(working_dir, file))
        save_mask(img_name, ann, save_dir)
    print(str(os.path.basename(working_dir))+" is finished.")

# 将图片处理成白色前景
def whiten_foreground(img):
    img = cv.threshold(img, 0, 255, cv.THRESH_BINARY)
    return img

def main():
    # project_dir = r'E:\Code\u2_net\U-2-Net\datasets\Supervisely Person Dataset'
    save_dir = r'E:\Code\u2_net\U-2-Net\train_data/mask'
    dir = r'E:\Code\u2_net\U-2-Net\train_data\mask1'
    # for i in range(1, 14):
    #     working_dir = os.path.join(project_dir, "ds"+str(i), "ann")
    #     print("========\nworking in "+str(working_dir))
    #     ds_save_dir = os.path.join(save_dir, "ds"+str(i))
    #     json2png(working_dir, ds_save_dir)
    

    for file in os.listdir(dir):       
        img = cv.imread(os.path.join(dir, file), cv.IMREAD_GRAYSCALE)            
        whiten_img = whiten_foreground(img)[1]
        whiten_img_rgb = cv.cvtColor(whiten_img, cv.COLOR_GRAY2BGR)
        cv.imwrite(os.path.join(save_dir, file), whiten_img_rgb)




if __name__ == "__main__":
    starttime = time.time()
    main()
    endtime = time.time()
    print('总共的时间为:', round(endtime - starttime, 4), 'secs')


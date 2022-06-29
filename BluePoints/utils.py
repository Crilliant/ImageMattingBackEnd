import datetime
import random
from config import *
from threading import Thread
import time


ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}


# 判断是否是允许的文件类型
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1) in ALLOWED_EXTENSIONS


# 产生随机数作为文件名
def generate_image_name():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand = random.randint(0, 1000)
    if rand < 10:
        rand = str(00) + str(rand)
    elif rand < 100:
        rand = str(0) + str(rand)
    else:
        rand = str(rand)

    return now_time + rand + '.png'


# 删除已处理的图片的线程目标
def delete_download(filename, thread_maps):
    while True:
        if os.path.exists(os.path.join(image_download_path, filename)):
            os.remove(os.path.join(image_download_path, filename))
            thread_maps.pop(filename)
            return
        time.sleep(5)


def delete_image(filename, thread_maps):
    feature = thread_maps.get(filename)
    if feature.cancel():
        os.remove(os.path.join(image_upload_path, filename))
        thread_maps.pop(filename)
    else:
        Thread(target=delete_download, args=(filename, thread_maps)).start()

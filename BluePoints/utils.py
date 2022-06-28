import datetime
import random

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

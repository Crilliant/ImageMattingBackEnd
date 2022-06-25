import datetime
import random


def generate_image_name():
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    rand = random.randint(0, 1000)
    if rand < 10:
        rand = str(00) + str(rand)
    elif rand < 100:
        rand = str(0) + str(rand)
    else:
        rand = str(rand)

    return now_time + rand

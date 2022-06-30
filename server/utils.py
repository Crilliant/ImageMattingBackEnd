import os


def get_filename(img_path):
    pure_img_name = os.path.basename(img_path)
    pure_img_name = pure_img_name.split('.')[-2] + ".png"
    return pure_img_name

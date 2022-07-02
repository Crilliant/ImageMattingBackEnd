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
    gray_img = cv.GaussianBlur(gray_img, (9, 9), 0)
    image_sobel_xy = get_sobel(gray_img)
    cv.imwrite(os.path.join(save_dir, filename), np.abs(128 * np.ones(image_sobel_xy.shape) - image_sobel_xy))
    print(filename + 'is finished.')


# 霓虹化
def neno(img_path, save_dir):
    filename = get_filename(img_path)
    b, g, r = cv.split(cv.imread(img_path))
    b = get_sobel(cv.GaussianBlur(b, (9, 9), 0))
    g = get_sobel(cv.GaussianBlur(g, (9, 9), 0))
    r = get_sobel(cv.GaussianBlur(r, (9, 9), 0))
    cv.imwrite(os.path.join(save_dir, filename), cv.merge([b, g, r]))

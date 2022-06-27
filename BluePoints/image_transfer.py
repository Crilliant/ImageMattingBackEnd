from flask import Blueprint, request, jsonify
from config import *
from concurrent.futures import ThreadPoolExecutor
from server.tool import *
import datetime
import random


bp = Blueprint('transfer', __name__, url_prefix='/api/image')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}
executor = ThreadPoolExecutor()


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


@bp.route('/identification', methods=['POST'])
def get_id_image():
    try:
        img = request.files.get('file')
        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        img.save(image_path)
        executor.submit(get_identification_image, image_path, image_mask_path, image_download_path)
        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


@bp.route('/segmentation', methods=['POST'])
def get_segmentation_image():
    try:
        img = request.files.get('file')
        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        img.save(image_path)
        executor.submit(img_matting, image_path, image_mask_path, image_download_path)
        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


@bp.route('/download', methods=['POST', 'GET'])
def download_image():
    try:
        filename = request.get_json().get('filename')
        filepath = os.path.join(image_download_path, filename)
        if os.path.exists(filepath):
            url = 'http://' + request.headers.get('host') + '/static/Download/' + filename
            print(url)
            return jsonify({'status': 'success', 'url': url})
        else:
            return jsonify({'status': 'wait', 'time': 5})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


@bp.route('/delete', methods=['POST'])
def delete_image():
    filename = request.get_json().get('filename')
    try:
        if os.path.exists(os.path.join(image_upload_path, filename)):
            os.remove(os.path.join(image_upload_path, filename))
        if os.path.exists(os.path.join(image_mask_path, filename)):
            os.remove(os.path.join(image_mask_path, filename))
        if os.path.exists(os.path.join(image_download_path, filename)):
            os.remove(os.path.join(image_download_path, filename))
        return jsonify({'status': 'success'})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


if __name__ == '__main__':
    test_filename = 'wallpaper.png'
    file_path = os.path.join(image_upload_path, test_filename)
    print(image_mask_path)
    executor.submit(img_matting(file_path, image_mask_path, image_download_path))

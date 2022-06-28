import time

from flask import Blueprint, request, jsonify
from config import *
from concurrent.futures import ThreadPoolExecutor
from server.tool import *
from threading import Thread
from BluePoints.utils import *


bp = Blueprint('segmentation_transfer', __name__, url_prefix='/api/image')
executor = ThreadPoolExecutor(2)
thread_maps = dict()


# 线程池中线程的回调函数
def call_back(feature):
    filename = [k for k, v in thread_maps.items() if v == feature][0]
    print('==================' + str(filename) + '-----------------------------------------------')
    if os.path.exists(os.path.join(image_upload_path, str(filename))):
        os.remove(os.path.join(image_upload_path, str(filename)))
        print('--------------------remove upload----------------------')
    if os.path.exists(os.path.join(image_mask_path, str(filename))):
        os.remove(os.path.join(image_mask_path, str(filename)))
        print('--------------------remove mask-------------------')


# 删除已处理的图片的线程目标
def delete_download(filename):
    while True:
        if os.path.exists(os.path.join(image_download_path, filename)):
            os.remove(os.path.join(image_download_path, filename))
            thread_maps.pop(filename)
            return
        time.sleep(5)


@bp.route('/identification', methods=['POST'])
def get_id_image():
    try:
        img = request.files.get('file')
        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        img.save(image_path)
        feature = executor.submit(get_identification_image, image_path, image_mask_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})
        print('----------------------------add maps---------------------')
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
        feature = executor.submit(img_matting, image_path, image_mask_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})
        print('----------------------------add maps---------------------')
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
    feature = thread_maps.get(filename)
    try:
        if feature.cancel():
            os.remove(os.path.join(image_upload_path, filename))
            thread_maps.pop(filename)
        else:
            Thread(target=delete_download, args=(filename, )).start()

        return jsonify({'status': 'success'})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


if __name__ == '__main__':
    test_filename = 'wallpaper.png'
    file_path = os.path.join(image_upload_path, test_filename)
    print(image_mask_path)
    executor.submit(img_matting(file_path, image_mask_path, image_download_path))

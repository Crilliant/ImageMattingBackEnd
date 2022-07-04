from flask import Blueprint, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from server.tool import *
from BluePoints.utils import *


bp = Blueprint('segmentation_transfer', __name__, url_prefix='/api/image')
executor = ThreadPoolExecutor(2)


# 线程池中线程的回调函数
def call_back(feature):
    from BluePoints.utils import thread_maps
    filename = [k for k, v in thread_maps.items() if v == feature][0]
    print('==================' + str(filename) + '-----------------------------------------------')
    if os.path.exists(os.path.join(image_upload_path, str(filename))):
        os.remove(os.path.join(image_upload_path, str(filename)))
        print('--------------------remove upload----------------------')
    if os.path.exists(os.path.join(image_mask_path, str(filename))):
        os.remove(os.path.join(image_mask_path, str(filename)))
        print('--------------------remove mask-------------------')


@bp.route('/segmentation', methods=['POST'])
def get_segmentation_image():
    from BluePoints.utils import thread_maps
    try:
        img = request.files.get('file')
        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        img.save(image_path)
        feature = executor.submit(img_matting, image_path, image_mask_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})
        print('----------------------------add maps---------------------' + new_filename)
        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


@bp.route('/download', methods=['POST', 'GET'])
def download_image():
    from BluePoints.utils import thread_maps
    try:
        filename = request.get_json().get('filename')
        feature = thread_maps[filename]
        if feature.done() and feature.exception() is None:
            url = 'http://' + request.headers.get('host') + '/static/Download/' + filename
            print(url)
            return jsonify({'status': 'success', 'url': url})
        elif feature.done() and feature.exception():
            return jsonify({'status': 'failed', 'message': str(feature.exception())})
        else:
            return jsonify({'status': 'wait', 'time': 5})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


@bp.route('/delete', methods=['POST'])
def delete():
    from BluePoints.utils import thread_maps
    try:
        filename = request.get_json().get('filename')
        print('------------------delete ' + filename + '----------------------')
        Thread(target=delete_image, args=(filename, thread_maps)).start()
        return jsonify({'status': 'success'})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})

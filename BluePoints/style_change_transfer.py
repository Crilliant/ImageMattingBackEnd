from flask import Blueprint, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from server.style import *
from BluePoints.utils import *


bp = Blueprint('style_change_transfer', __name__, url_prefix='/api/style')
executor = ThreadPoolExecutor()


# 线程池中线程的回调函数
def call_back(feature):
    from BluePoints.utils import thread_maps
    filename = [k for k, v in thread_maps.items() if v == feature][0]
    if os.path.exists(os.path.join(image_upload_path, str(filename))):
        os.remove(os.path.join(image_upload_path, str(filename)))


# 水彩效果
@bp.route('/watercolor', methods=['POST'])
def change_to_watercolor():
    from BluePoints.utils import thread_maps
    try:
        image = request.files.get('file')
        if not allowed_file(image.filename):
            return jsonify({'status': 'failed', 'message': 'file type error'})
        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        image.save(image_path)
        feature = executor.submit(watercolor, image_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})

        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


# 素描效果
@bp.route('/sketch', methods=['POST'])
def change_to_sketch():
    from BluePoints.utils import thread_maps
    try:
        image = request.files.get('file')
        if not allowed_file(image.filename):
            return jsonify({'status': 'failed', 'message': 'file type error'})

        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        image.save(image_path)
        feature = executor.submit(sketch, image_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})

        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


# 霓虹效果
@bp.route('/neno', methods=['POST'])
def change_to_neno():
    from BluePoints.utils import thread_maps
    try:
        image = request.files.get('file')
        if not allowed_file(image.filename):
            return jsonify({'status': 'failed', 'message': 'file type error'})

        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        image.save(image_path)
        feature = executor.submit(neno, image_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})

        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})

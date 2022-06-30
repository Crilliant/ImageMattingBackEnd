from flask import Blueprint, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from server.tool import watercolor
from BluePoints.utils import *


bp = Blueprint('style_change_transfer', __name__, url_prefix='/api/style')
executor = ThreadPoolExecutor()
thread_maps = dict()


# 线程池中线程的回调函数
def call_back(feature):
    filename = [k for k, v in thread_maps.items() if v == feature][0]
    if os.path.exists(os.path.join(image_upload_path, str(filename))):
        os.remove(os.path.join(image_upload_path, str(filename)))


# 水彩效果
@bp.route('/watercolor', methods=['POST'])
def change_to_watercolor():
    try:
        image = request.files.get('file')
        new_filename = generate_image_name()
        image_path = os.path.join(image_upload_path, new_filename)
        image.save(image_path)
        feature = executor.submit(watercolor, image_path, image_download_path)
        feature.add_done_callback(call_back)
        thread_maps.update({new_filename: feature})
        return jsonify({'status': 'success', 'message': new_filename})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})


@bp.route('/delete', methods=['POST'])
def delete():
    try:
        filename = request.get_json().get('filename')
        delete_image(filename, thread_maps)
        return jsonify({'status': 'success'})
    except Exception as err:
        return jsonify({'status': 'failed', 'message': str(err)})

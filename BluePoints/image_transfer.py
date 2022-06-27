from flask import Blueprint, request, jsonify
from config import *
from BluePoints.utils import generate_image_name
from concurrent.futures import ThreadPoolExecutor
from server.tool import *

bp = Blueprint('transfer', __name__, url_prefix='/api/image')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'JPG', 'PNG'}
executor = ThreadPoolExecutor()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1) in ALLOWED_EXTENSIONS


@bp.route('/identification', methods=['POST'])
def get_id_image():
    try:
        img = request.files.get('file')
        file_extension = '.' + img.filename.split('.')[1]
        new_filename = generate_image_name() + file_extension
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
        file_extension = '.' + img.filename.split('.')[1]
        new_filename = generate_image_name() + file_extension
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


@bp.route('/delete')
def delete_image():
    filename = request.get_json().get('filename')
    try:
        if os.path.exists(os.path.join(image_upload_path, filename)):
            os.remove(os.path.join(image_upload_path, filename))
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

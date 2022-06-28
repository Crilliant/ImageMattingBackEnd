import os

from flask import Blueprint, request, jsonify
from config import background_image_path


bp = Blueprint('back_ground_transfer', __name__, url_prefix='/api/background')


@bp.route('/load', methods=['GET'])
def get_background_images():
    urls = []
    for filename in os.listdir(background_image_path):
        url = 'http://' + request.headers.get('host') + '/static/Background/' + filename
        urls.append(url)

    return jsonify({'urls': urls})
